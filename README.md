# ⚙️ Whitney API Collection

A collection of modular RESTful APIs built with **Flask** to showcase backend architecture, clean code, and versatile design.

---

## 🌐 Overview

WhitLabs is a multi-API backend project featuring **three distinct APIs**:
- 📚 **Bookify API** — Manage and explore book collections  
- ✅ **TaskFlow API** — Organize and track tasks efficiently  
- 📝 **NoteNest API** — Store, search, and manage personal notes  

Each API demonstrates full CRUD functionality, advanced filters, analytics, and bulk operations — all under a single Flask app.

---

## 🧱 Project Structure
project-api/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
│
├── bookify/
│ ├── init.py
│ ├── routes.py
│ └── models.py
│
├── taskflow/
│ ├── init.py
│ ├── routes.py
│ └── models.py
│
└── notenest/
├── init.py
├── routes.py
└── models.py


---

## 🚀 Live Deployment (Render)

### Step 1. Push to GitHub
```bash ```
git init
git add .
git commit -m "WhitLabs API initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/project-api.git
git push -u origin main  

### Step 2. Deploy on Render

Go to Render.com

Click New Web Service

Connect your GitHub repo

Choose:

Environment: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Deploy and wait for it to build 🌱

### 🌍 API Endpoints Overview
API	Prefix	Example Routes
Bookify	/bookify	/books, /books/search, /books/stats, /books/export
TaskFlow	/taskflow	/tasks, /tasks/completed, /tasks/stats, /tasks/export
NoteNest	/notenest	/notes, /notes/recent, /notes/summary, /notes/export

### Each API supports:

✅ CRUD operations

🔍 Searching & Filtering

📊 Statistics & Analytics

🧹 Bulk Actions

💾 Data Export

### 🧠 Tech Stack
Category	Tools
Language	Python
Framework	Flask
Database	SQLite (SQLAlchemy ORM)
Server	Gunicorn
Deployment	Render
✨ Example Responses

GET /bookify/books/stats

{
  "total_books": 12,
  "read": 5,
  "not_read": 7
}


POST /taskflow/tasks

{
  "title": "Finish API Portfolio",
  "description": "Complete the WhitLabs API project and deploy it",
  "completed": false
}

### 💡 Why This Project Rocks

✅ Multi-API structure in a single Flask app
✅ Clean modular blueprints
✅ Database-powered CRUD & advanced routes
✅ Ready-to-deploy on Render
✅ Perfect for portfolios or interview demos

### Author

 Whitney Shisia
🚀 Backend Developer | Python & Flask Enthusiast

