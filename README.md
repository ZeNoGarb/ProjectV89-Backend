echo '# ProjectV89 Backend API

Flask-based REST API for Camera Management and AI Inference System

## Quick Start

1. Copy environment file:
```bash
cp .env.example .env
```

2. Edit .env with your credentials

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/login` - User login
- `GET /api/users` - Get users (requires token)
- `GET /api/cameras` - Get cameras (requires token)
- `POST /api/inference` - AI inference (requires token)

## Default Login
- Username: admin
- Password: admin123' > README.md