from flask import Blueprint, request, jsonify
from models import db, Camera
from utils.decorators import token_required

cameras_bp = Blueprint('cameras', __name__)

@cameras_bp.route('', methods=['GET'])
@token_required
def get_cameras(current_user):
    cameras = Camera.query.all()
    return jsonify([camera.to_dict() for camera in cameras]), 200

@cameras_bp.route('', methods=['POST'])
@token_required
def create_camera(current_user):
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('url') or not data.get('status'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    camera = Camera(
        name=data['name'],
        url=data['url'],
        status=data['status'],
    )
    
    db.session.add(camera)
    db.session.commit()
    
    return jsonify(camera.to_dict()), 201

@cameras_bp.route('/<int:camera_id>', methods=['GET'])
@token_required
def get_camera(current_user, camera_id):
    camera = Camera.query.get_or_404(camera_id)
    return jsonify(camera.to_dict()), 200

@cameras_bp.route('/<int:camera_id>', methods=['PUT'])
@token_required
def update_camera(current_user, camera_id):
    camera = Camera.query.get_or_404(camera_id)
    data = request.get_json()
    
    if data.get('name'):
        camera.name = data['name']
    if data.get('url'):
        camera.url = data['url']
    
    db.session.commit()
    return jsonify(camera.to_dict()), 200

@cameras_bp.route('/<int:camera_id>', methods=['DELETE'])
@token_required
def delete_camera(current_user, camera_id):
    camera = Camera.query.get_or_404(camera_id)
    db.session.delete(camera)
    db.session.commit()
    return jsonify({'message': 'Camera deleted successfully'}), 200