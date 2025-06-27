from datetime import datetime, timezone
from . import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    alerted = db.Column(db.String(100), nullable=False)
    prediction_result = db.Column(db.Text)  # JSON string of inference results
    motion_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    image_data = db.Column(db.Text)  # Base64 encoded image

    def to_dict(self):
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'alerted': self.alerted,
            'prediction_result': self.prediction_result,
            'motion_score': self.motion_score,
            'timestamp': self.timestamp.isoformat(),
            'has_image': bool(self.image_data)
        }