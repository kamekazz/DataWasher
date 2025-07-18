from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from models import db, login_manager
from routes import bp
import os


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datawasher.db"

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=os.getenv("DEBUG", "False"), # type: ignore
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT", 5000)),
    )
