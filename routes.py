from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)

@bp.route('/')
def greeting():
    return render_template('pages/greeting.html', title='Greeting')

@bp.route('/login')
def login():
    return render_template('pages/login.html', title='Login')

@bp.route('/home')
def home():
    return render_template('pages/home.html', title='Home')

@bp.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html', title='Dashboard')

@bp.route('/1-hour-report', methods=['GET', 'POST'])
def one_hour_report():
    message = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename:
            message = f"Uploaded {uploaded_file.filename}"
    return render_template('pages/one_hour_report.html',
                           title='1-Hour Report',
                           message=message)

@bp.route('/greet/<name>')
def greet(name):
    return f"<p>Hello, {name}!</p>"

@bp.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
