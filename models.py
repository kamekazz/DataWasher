from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'



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


class WorkType(db.Model):
    __tablename__ = "work_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    # description = db.Column(db.String(256), nullable=True)


class Labor(db.Model):
    __tablename__ = "labors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    work_type_id = db.Column(db.Integer, db.ForeignKey("work_types.id"), nullable=False)

    work_type = db.relationship("WorkType", backref=db.backref("labors", lazy=True))


class StagedInventory(db.Model):
    """Inventory sitting on the floor waiting to be processed."""

    __tablename__ = "staged_inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    labor_id = db.Column(
        db.Integer, db.ForeignKey("labors.id"), nullable=False
    )

    labor = db.relationship("Labor", backref=db.backref("staged_items", lazy=True))

