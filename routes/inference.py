import os
import cv2
import time
import base64
import numpy as np
import datetime
from flask import Blueprint, request, jsonify
from models import db, Log
from utils.motion import detect_motion_score, preprocess
from utils.classifier import predict_pose_class
from utils.telegram_alert import send_telegram_alert
from utils.decorators import token_required
from config import Config

MOTION_THRESHOLD = Config.MOTION_THRESHOLD
MAX_MOTION_THRESHOLD = Config.MAX_MOTION_THRESHOLD
COOLDOWN_SECONDS = Config.COOLDOWN_SECONDS
START_HOUR = Config.START_HOUR
END_HOUR = Config.END_HOUR

inference_bp = Blueprint('inference', __name__)

@inference_bp.route('', methods=['POST'])
@token_required
def run_inference(current_user):
    try:
        if 'current_frame' not in request.files or 'previous_frame' not in request.files:
            return jsonify({'message': 'Missing image files'}), 400
        if not request.form.get('camera_id'):
            return jsonify({'message': 'Missing required fields'}), 400

        current_file = request.files['current_frame']
        previous_file = request.files['previous_frame']
        current_bytes = current_file.read()
        previous_bytes = previous_file.read()
        current_frame_array = cv2.imdecode(np.frombuffer(current_bytes, np.uint8), cv2.IMREAD_COLOR)
        previous_frame_array = cv2.imdecode(np.frombuffer(previous_bytes, np.uint8), cv2.IMREAD_COLOR)

        cooldown_seconds = int(request.form.get('cooldown_seconds', Config.COOLDOWN_SECONDS))
        start_hour = int(request.form.get('start_hour', START_HOUR))
        start_minute = int(request.form.get('start_minute', 0))
        end_hour = int(request.form.get('end_hour', END_HOUR))
        end_minute = int(request.form.get('end_minute', 0))

        last_alert_time = 0
        alerted = False

        prev_gray = preprocess(previous_frame_array)
        motion_score, mask, roi, curr_gray = detect_motion_score(prev_gray, current_frame_array)
        prev_pose = predict_pose_class(previous_frame_array)
        current_pose = predict_pose_class(current_frame_array)

        now = time.time()
        if (
            MOTION_THRESHOLD <= motion_score <= MAX_MOTION_THRESHOLD
            and prev_pose == "sleep"
            and current_pose == "sit"
            and now - last_alert_time > cooldown_seconds
        ):
            send_telegram_alert(current_frame_array, f"Detected risk to falling off the bed. \npose: {current_pose}, motion score: {motion_score:.0f}")
            last_alert_time = now
            alerted = True
        
        # Encode current frame as base64 for logging
        _, buffer = cv2.imencode('.jpg', current_frame_array)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        log = Log(
            camera_id=request.form['camera_id'],
            alerted=alerted,
            prediction_result=current_pose,
            motion_score=float(motion_score),
            image_data=image_base64
        )
        db.session.add(log)
        db.session.commit()

        now_dt = datetime.datetime.now()
        now_hour = now_dt.hour
        now_minute = now_dt.minute
        # คำนวณเวลาเป็นนาที
        current_time_in_minutes = now_hour * 60 + now_minute
        start_time_in_minutes = start_hour * 60 + start_minute
        end_time_in_minutes = end_hour * 60 + end_minute
        if start_time_in_minutes <= end_time_in_minutes:
            in_time = start_time_in_minutes <= current_time_in_minutes <= end_time_in_minutes
        else:
            in_time = current_time_in_minutes >= start_time_in_minutes or current_time_in_minutes <= end_time_in_minutes

        if in_time:
            return jsonify({'message': 'Inference completed', 'alerted': alerted, 'pose': current_pose, 'motion_score': motion_score}), 200
        else:
            return jsonify({'message': 'Inference completed', 'alerted': False, 'pose': current_pose, 'motion_score': motion_score}), 200

    except Exception as e:
        return jsonify({'message': f'Inference failed: {str(e)}'}), 500