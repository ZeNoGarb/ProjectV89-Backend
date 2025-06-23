# สร้างไฟล์ test_db.py
from app import app
from models import db

with app.app_context():
    try:
        db.create_all()
        print('✅ Connected to PostgreSQL successfully!')
        print(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    except Exception as e:
        print(f'❌ Connection failed: {e}')