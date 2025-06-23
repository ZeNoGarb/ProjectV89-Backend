from flask import Blueprint, request, jsonify
from models import db, Log
from utils.decorators import token_required
from utils.ml_model import SimpleModel

inference_bp = Blueprint('inference', __name__)
model = SimpleModel()

@inference_bp.route('', methods=['POST'])
@token_required
def run_inference(current_user):
    data = request.get_json()
    
    if not data or not data.get('image_data'):
        return jsonify({'message': 'Image data is required'}), 400
    
    try:
        # Decode base64 image
        image_data = data['image_data']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Run inference
        results = model.predict(image_data)
        
        # Save log if camera_id is provided
        if data.get('camera_id'):
            log = Log(
                camera_id=data['camera_id'],
                user_id=current_user.id,
                action='inference',
                description=f"Detected: {results['prediction']}",
                image_data=data['image_data'],
                prediction_result=str(results),
                confidence_score=results['confidence']
            )
            db.session.add(log)
            db.session.commit()
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({'message': f'Inference failed: {str(e)}'}), 500