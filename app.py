from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.cameras import cameras_bp
    from routes.logs import logs_bp
    from routes.inference import inference_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(cameras_bp, url_prefix='/api/cameras')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
    app.register_blueprint(inference_bp, url_prefix='/api/inference')
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default admin user if not exists
            if not User.query.filter_by(username='admin').first():
                admin_user = User(username='admin', email='admin@example.com')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Default admin user created!")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)