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

@bp.route('/greet/<name>')
def greet(name):
    return f"<p>Hello, {name}!</p>"

@bp.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
