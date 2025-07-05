from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


class Driver(db.Model):
    """Represents a driver type and how many workers use it."""

    id = db.Column(db.Integer, primary_key=True)
    driver_type = db.Column(db.String(80), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Driver {self.driver_type}: {self.count}>"


class Labor(db.Model):
    """Represents a unit of labor available for assignments."""

    id = db.Column(db.Integer, primary_key=True)
    labor_type = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Labor {self.labor_type}: {self.amount}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        hashed = generate_password_hash(password)
        self.password_hash = hashed

    def check_password(self, password: str) -> bool:
        valid = check_password_hash(self.password_hash, password)
        return valid


@login_manager.user_loader
def load_user(user_id: str):
    user_id_int = int(user_id)
    user = User.query.get(user_id_int)
    return user
