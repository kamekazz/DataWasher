from flask import Flask
from models import db, login_manager
from routes import bp
from dotenv import load_dotenv
import os

# Load environment variables from a .env file before the application is created
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    database_uri = os.getenv("DATABASE_URL", "sqlite:///datawasher.db")
    if database_uri.startswith("postgres://"):
        database_uri = database_uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT", 5000))
