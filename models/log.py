from datetime import datetime
from . import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_data = db.Column(db.Text)  # Base64 encoded image
    prediction_result = db.Column(db.Text)  # JSON string of inference results
    confidence_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'user_id': self.user_id,
            'action': self.action,
            'description': self.description,
            'prediction_result': self.prediction_result,
            'confidence_score': self.confidence_score,
            'timestamp': self.timestamp.isoformat(),
            'has_image': bool(self.image_data)
        }