import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from logic.one_hour_report import count_assigned_tasks
from logic.tracking_status import (
    process_tracking_csv,
    process_single_tracking_number,
)
from models import db, User, Driver

bp = Blueprint("main", __name__)


@bp.route("/")
def greeting():
    return render_template("pages/greeting.html", title="Greeting")


@bp.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_url = request.args.get("next") or url_for("main.dashboard")
            return redirect(next_url)
        message = "Invalid credentials"
    return render_template("pages/login.html", title="Login", message=message)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/create-user", methods=["GET", "POST"])
def create_user():
    message = None
    if request.method == "POST" and os.getenv("DEBUG") == "True":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            message = "Username and password are required"
        elif User.query.filter_by(username=username).first():
            message = "User already exists"
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            message = f"Created user {username}"
    return render_template(
        "pages/create_user.html", title="Create User", message=message
    )


@bp.route("/home")
def home():
    return render_template("pages/home.html", title="Home")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("pages/dashboard.html", title="Dashboard")


@bp.route("/1-hour-report", methods=["GET", "POST"])
@login_required
def one_hour_report():
    message = None
    assign_count = None
    ready_for_assignment = None
    transaction_summary = None
    assigned_transaction_summary = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        (
            message,
            assign_count,
            ready_for_assignment,
            transaction_summary,
            assigned_transaction_summary,
        ) = count_assigned_tasks(uploaded_file)
    return render_template(
        "pages/one_hour_report.html",
        title="1-Hour Report",
        message=message,
        assign_count=assign_count,
        ready_for_assignment=ready_for_assignment,
        transaction_summary=transaction_summary,
        assigned_summary=assigned_transaction_summary,
    )


@bp.route("/track-shipments", methods=["GET", "POST"])
@login_required
def track_shipments():
    message = None
    error = None
    rows = None
    status = None
    tracking_number = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename:
            message, rows = process_tracking_csv(uploaded_file)
            if not rows:
                error = message
        else:
            tracking_number = request.form.get("tracking_number")
            message, status = process_single_tracking_number(tracking_number)
            if not status:
                error = message
    return render_template(
        "pages/track_shipments.html",
        title="Shipment Tracking",
        message=message if (rows or status) else None,
        error=error,
        rows=rows,
        tracking_number=tracking_number,
        status=status,
    )


@bp.route("/drivers", methods=["GET", "POST"])
@login_required
def drivers():
    """Create a new driver record and list all existing records."""
    message = None
    if request.method == "POST":
        driver_type = request.form.get("driver_type")
        count = request.form.get("count")
        if not driver_type or not count:
            message = "Type and count are required"
        else:
            try:
                count_int = int(count)
            except ValueError:
                message = "Count must be an integer"
            else:
                driver = Driver(driver_type=driver_type, count=count_int)
                db.session.add(driver)
                db.session.commit()
                message = f"Added driver type {driver_type}"
    all_drivers = Driver.query.all()
    return render_template(
        "pages/drivers.html",
        title="Drivers",
        message=message,
        drivers=all_drivers,
    )


@bp.route("/greet/<name>")
def greet(name):
    return f"<p>Hello, {name}!</p>"


@bp.route("/handle_url_params")
def handle_url_params():
    greeting = request.args.get("greeting", "default_value1")
    name = request.args.get("name", "default_value2")
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
