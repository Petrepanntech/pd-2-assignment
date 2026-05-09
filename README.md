# Pandas 2 Assignment - Supply Chain & Data Analytics

A comprehensive Flask-based application for supply chain management, data analytics, and educational course management with integrated gaming features.

## 🚀 Quick Start

### Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run app: `python app.py`

### Access the Application
- Home: http://localhost:5000
- Login: http://localhost:5000/login
- Admin: http://localhost:5000/admin

## 📁 Project Structure

```
├── app.py                  # Flask application entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── routes/                # API endpoints
│   ├── auth.py           # Authentication
│   ├── courses.py        # Course management
│   ├── games.py          # Gaming features
│   ├── tournaments.py    # Tournament system
│   ├── admin.py          # Admin panel
│   └── search.py         # Search functionality
├── templates/            # HTML files
├── static/               # CSS and JavaScript
└── global_logistics_manifest.csv  # Sample supply chain data
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
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** JWT
- **Features:** RESTful API, Search, Admin Panel, Gaming System

## 📝 License

Educational project
