import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_user, logout_user, login_required
from logic.one_hour_report import count_assigned_tasks
from logic.eod_report import count_total_pick
from logic.tracking_status import (
    process_tracking_csv,
    process_single_tracking_number,
)
from models import db, User, WorkType, Labor, StagedInventory

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

@bp.route("/eod-report", methods=["GET", "POST"])
@login_required
def eod_report():
    message = None
    units_picked = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        units_picked, message = count_total_pick(uploaded_file)
    return render_template(
        "pages/eod_report.html",
        title="EOD Report",
        message=message,
        units_picked=units_picked,
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



@bp.route("/greet/<name>")
def greet(name):
    return f"<p>Hello, {name}!</p>"


@bp.route("/work-types")
@login_required
def list_work_types():
    work_types = WorkType.query.order_by(WorkType.name).all()
    return render_template(
        "pages/work_type_list.html", title="Work Types", work_types=work_types
    )


@bp.route("/work-types/new", methods=["GET", "POST"])
@login_required
def create_work_type():
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            message = "Name is required"
        elif WorkType.query.filter_by(name=name).first():
            message = "Work Type already exists"
        else:
            wt = WorkType(name=name)
            db.session.add(wt)
            db.session.commit()
            return redirect(url_for("main.list_work_types"))
    return render_template(
        "pages/work_type_form.html",
        title="Create Work Type",
        message=message,
        work_type=None,
    )


@bp.route("/work-types/<int:work_type_id>/edit", methods=["GET", "POST"])
@login_required
def edit_work_type(work_type_id):
    work_type = WorkType.query.get_or_404(work_type_id)
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            message = "Name is required"
        elif WorkType.query.filter_by(name=name).first() and name != work_type.name:
            message = "Work Type already exists"
        else:
            work_type.name = name
            db.session.commit()
            return redirect(url_for("main.list_work_types"))
    return render_template(
        "pages/work_type_form.html",
        title="Edit Work Type",
        message=message,
        work_type=work_type,
    )


@bp.route("/work-types/<int:work_type_id>/delete", methods=["POST"])
@login_required
def delete_work_type(work_type_id):
    work_type = WorkType.query.get_or_404(work_type_id)
    db.session.delete(work_type)
    db.session.commit()
    return redirect(url_for("main.list_work_types"))


@bp.route("/labors")
@login_required
def list_labors():
    labors = Labor.query.order_by(Labor.name).all()
    return render_template(
        "pages/labor_list.html", title="Labor", labors=labors
    )


@bp.route("/labors/new", methods=["GET", "POST"])
@login_required
def create_labor():
    work_types = WorkType.query.order_by(WorkType.name).all()
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        num_people = request.form.get("num_people")
        work_type_id = request.form.get("work_type_id")
        if not name or not num_people or not work_type_id:
            message = "All fields are required"
        else:
            try:
                num_people_int = int(num_people)
            except ValueError:
                message = "Number of People must be an integer"
            else:
                wt = WorkType.query.get(work_type_id)
                if not wt:
                    message = "Invalid Work Type"
                else:
                    labor = Labor(
                        name=name,
                        num_people=num_people_int,
                        work_type=wt,
                    )
                    db.session.add(labor)
                    db.session.commit()
                    return redirect(url_for("main.list_labors"))
    return render_template(
        "pages/labor_form.html",
        title="Create Labor",
        message=message,
        labor=None,
        work_types=work_types,
    )


@bp.route("/labors/<int:labor_id>/edit", methods=["GET", "POST"])
@login_required
def edit_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    work_types = WorkType.query.order_by(WorkType.name).all()
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        num_people = request.form.get("num_people")
        work_type_id = request.form.get("work_type_id")
        if not name or not num_people or not work_type_id:
            message = "All fields are required"
        else:
            try:
                num_people_int = int(num_people)
            except ValueError:
                message = "Number of People must be an integer"
            else:
                wt = WorkType.query.get(work_type_id)
                if not wt:
                    message = "Invalid Work Type"
                else:
                    labor.name = name
                    labor.num_people = num_people_int
                    labor.work_type = wt
                    db.session.commit()
                    return redirect(url_for("main.list_labors"))
    return render_template(
        "pages/labor_form.html",
        title="Edit Labor",
        message=message,
        labor=labor,
        work_types=work_types,
    )


@bp.route("/labors/<int:labor_id>/delete", methods=["POST"])
@login_required
def delete_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    db.session.delete(labor)
    db.session.commit()
    return redirect(url_for("main.list_labors"))


@bp.route("/staged-items")
@login_required
def list_staged_items():
    items = StagedInventory.query.order_by(StagedInventory.name).all()
    return render_template(
        "pages/staged_inventory_list.html", title="Staged Inventory", items=items
    )


@bp.route("/staged-items/new", methods=["GET", "POST"])
@login_required
def create_staged_item():
    labors = Labor.query.order_by(Labor.name).all()
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        labor_id = request.form.get("labor_id")
        if not name or not amount or not labor_id:
            message = "All fields are required"
        else:
            try:
                amount_int = int(amount)
            except ValueError:
                message = "Amount must be an integer"
            else:
                labor = Labor.query.get(labor_id)
                if not labor:
                    message = "Invalid Job"
                else:
                    item = StagedInventory(name=name, amount=amount_int, labor=labor)
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for("main.list_staged_items"))
    return render_template(
        "pages/staged_inventory_form.html",
        title="Create Inventory",
        message=message,
        item=None,
        labors=labors,
    )


@bp.route("/staged-items/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_staged_item(item_id):
    item = StagedInventory.query.get_or_404(item_id)
    labors = Labor.query.order_by(Labor.name).all()
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        labor_id = request.form.get("labor_id")
        if not name or not amount or not labor_id:
            message = "All fields are required"
        else:
            try:
                amount_int = int(amount)
            except ValueError:
                message = "Amount must be an integer"
            else:
                labor = Labor.query.get(labor_id)
                if not labor:
                    message = "Invalid Job"
                else:
                    item.name = name
                    item.amount = amount_int
                    item.labor = labor
                    db.session.commit()
                    return redirect(url_for("main.list_staged_items"))
    return render_template(
        "pages/staged_inventory_form.html",
        title="Edit Inventory",
        message=message,
        item=item,
        labors=labors,
    )


@bp.route("/staged-items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_staged_item(item_id):
    item = StagedInventory.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("main.list_staged_items"))


@bp.route("/handle_url_params")
def handle_url_params():
    greeting = request.args.get("greeting", "default_value1")
    name = request.args.get("name", "default_value2")
    return f"<h2>greeting: {greeting}, name: {name}</h2>"


