from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from logic.one_hour_report import process_one_hour_report_file

bp = Blueprint('main', __name__)


def login_required(view_func):
    """Simple decorator to require authentication."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('main.login', next=request.path))
        return view_func(*args, **kwargs)

    return wrapped_view

@bp.route('/')
def greeting():
    return render_template('pages/greeting.html', title='Greeting')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'secret':
            session['logged_in'] = True
            next_url = request.args.get('next') or url_for('main.dashboard')
            return redirect(next_url)
        message = 'Invalid credentials'
    return render_template('pages/login.html', title='Login', message=message)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@bp.route('/create-user', methods=['GET', 'POST'])
def create_user():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        message = f"Created user {username}"
    return render_template('pages/create_user.html', title='Create User', message=message)

@bp.route('/home')
def home():
    return render_template('pages/home.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html', title='Dashboard')

@bp.route('/1-hour-report', methods=['GET', 'POST'])
@login_required
def one_hour_report():
    message = None
    table_data = None
    chart_labels = None
    chart_values = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        (message,
         table_data,
         chart_labels,
         chart_values) = process_one_hour_report_file(uploaded_file)
    return render_template(
        'pages/one_hour_report.html',
        title='1-Hour Report',
        message=message,
        table_data=table_data,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )

@bp.route('/greet/<name>')
def greet(name):
    return f"<p>Hello, {name}!</p>"

@bp.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
