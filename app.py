from flask import Flask
from bookify.routes import bookify_bp
from taskflow.routes import taskflow_bp
from notenest.routes import notenest_bp
from bookify import init_app as init_bookify
from bookify.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whitlabs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize Bookify-specific setup
    init_bookify(app)
    init_taskflow(app)
    init_notenest(app)

    # Register Blueprints
    app.register_blueprint(bookify_bp, url_prefix='/bookify')
    app.register_blueprint(taskflow_bp, url_prefix='/taskflow')
    app.register_blueprint(notenest_bp, url_prefix='/notenest')

    @app.route('/')
    def home():
        return {
            "message": "Welcome to WhitLabs API Collection 🚀",
            "available_apis": ["/bookify", "/taskflow", "/notenest"]
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
