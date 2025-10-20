from flask import Flask
from database import db  # ✅ import the single shared db
from bookify.routes import bookify_bp
from taskflow.routes import taskflow_bp
from notenest.routes import notenest_bp

def create_app():
    app = Flask(__name__)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whitlabs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # ✅ Initialize the shared db once

    # Register Blueprints
    app.register_blueprint(bookify_bp, url_prefix='/bookify')
    app.register_blueprint(taskflow_bp, url_prefix='/taskflow')
    app.register_blueprint(notenest_bp, url_prefix='/notenest')

    @app.route('/')
    def home():
        return {
            "message": "Welcome to Whitney API Collection 🚀",
            "available_apis": ["/bookify", "/taskflow", "/notenest"]
        }

    return app


if __name__ == "__main__":
    app = create_app()

    # Create tables once before running
    with app.app_context():
        db.create_all()

    app.run(debug=True)
