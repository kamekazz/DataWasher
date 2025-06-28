from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)

@bp.route('/')
def greeting():
    return render_template('greeting.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/greet/<name>')
def greet(name):
    return f"<p>Hello, {name}!</p>"

@bp.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
