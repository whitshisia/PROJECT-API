import os
from flask import Flask
from database import db
from bookify.routes import bookify_bp
from taskflow.routes import taskflow_bp
from notenest.routes import notenest_bp


def create_app():
    app = Flask(__name__)

    # ✅ Choose PostgreSQL if DATABASE_URL exists, else fallback to SQLite locally
    db_url = os.environ.get("DATABASE_URL", "sqlite:///whitlabs.db")
    if db_url.startswith("postgres://"):
        # Render sometimes uses old-style postgres:// URIs, SQLAlchemy wants postgresql://
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(bookify_bp, url_prefix="/bookify")
    app.register_blueprint(taskflow_bp, url_prefix="/taskflow")
    app.register_blueprint(notenest_bp, url_prefix="/notenest")

    @app.route("/")
    def home():
        return {
            "message": "Welcome to Whitney API Collection 🚀",
            "available_apis": ["/bookify", "/taskflow", "/notenest"]
        }

    return app


# ✅ Expose app for Gunicorn
app = create_app()

# ✅ Create tables automatically on startup (lightweight apps)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
