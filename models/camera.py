from datetime import datetime, timezone
from . import db

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(45), default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }