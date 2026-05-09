# Pandas 2 Assignment - Supply Chain & Data Analytics

A comprehensive Flask-based application for supply chain management, data analytics, and educational course management with integrated gaming features.

## 🚀 Quick Start

### Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment values (example):
   - `JWT_SECRET_KEY=dev-only-secret`
   - `DATABASE_URL=sqlite:///app.db`
   - `RUN_DB_CREATE_ALL=true`
6. Run app: `python app.py`

### Access the Application
- Home: http://localhost:5000
- Login: http://localhost:5000/login
- Admin: http://localhost:5000/admin

## 🌐 Vercel Deployment (Production)

1. Keep `vercel.json` pointing all requests to `api/index.py`.
2. In Vercel Project Settings → Environment Variables, set:
   - `APP_ENV=production` (or `FLASK_ENV=production`)
   - `JWT_SECRET_KEY=<strong-random-secret>`
   - `DATABASE_URL=<postgresql://...>`
   - `RUN_DB_CREATE_ALL=false`
3. Deploy.
4. Initialize schema once against the production database from your local machine/CI:
   ```bash
   APP_ENV=production JWT_SECRET_KEY=... DATABASE_URL=postgresql://... flask --app "app:create_app()" init-db
   ```

> In production, SQLite is rejected and a persistent `DATABASE_URL` is required.

## 📁 Project Structure

```
├── app.py                  # Flask app factory + routes + init-db command
├── api/index.py            # Vercel Python runtime entrypoint
├── config.py               # Configuration settings
├── models.py               # Database models
├── auth.py                 # JWT helpers
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel routing/build config
└── VERCEL_DEPLOYMENT_GUIDE.md
```

## 🔒 Security

See SECURITY_REVIEW_REPORT.md for security audit findings and fixes.

## 📚 Documentation

- **SETUP_GUIDE.md** - Detailed setup instructions
- **SECURITY_REVIEW_REPORT.md** - Security audit details
- **RESPONSIVE_DESIGN_REPORT.md** - UI/UX responsive design
- **Assignment_Supply_Chain.md** - Assignment specifications

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite (local), PostgreSQL via `DATABASE_URL` (production)
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** JWT
- **Features:** RESTful API, Search, Admin Panel, Gaming System

## 📝 License

Educational project
