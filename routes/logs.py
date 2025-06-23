from flask import Blueprint, request, jsonify
from models import db, Log
from utils.decorators import token_required

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('', methods=['GET'])
@token_required
def get_logs(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    logs = Log.query.order_by(Log.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': page
    }), 200

@logs_bp.route('', methods=['POST'])
@token_required
def create_log(current_user):
    data = request.get_json()
    
    if not data or not data.get('camera_id') or not data.get('action'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    log = Log(
        camera_id=data['camera_id'],
        user_id=current_user.id,
        action=data['action'],
        description=data.get('description'),
        image_data=data.get('image_data'),
        prediction_result=data.get('prediction_result'),
        confidence_score=data.get('confidence_score')
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify(log.to_dict()), 201

@logs_bp.route('/<int:log_id>', methods=['GET'])
@token_required
def get_log(current_user, log_id):
    log = Log.query.get_or_404(log_id)
    log_dict = log.to_dict()
    
    # Include image data if requested
    if request.args.get('include_image') == 'true' and log.image_data:
        log_dict['image_data'] = log.image_data
    
    return jsonify(log_dict), 200

@logs_bp.route('/<int:log_id>', methods=['DELETE'])
@token_required
def delete_log(current_user, log_id):
    log = Log.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Log deleted successfully'}), 200