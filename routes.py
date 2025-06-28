from flask import Blueprint, render_template, request
import pandas as pd
import json

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
    table_data = None
    chart_labels = None
    chart_values = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename:
            try:
                df = pd.read_csv(uploaded_file)
                # try to find a city or country column
                city_col = None
                for col in df.columns:
                    if col.lower() in ['city', 'country']:
                        city_col = col
                        break
                if not city_col:
                    message = 'No city column found'
                else:
                    counts = df[city_col].value_counts()
                    total = counts.sum()
                    table_data = [
                        {'city': city, 'customers': int(count),
                         'percent': count / total * 100}
                        for city, count in counts.items()
                    ]
                    chart_labels = json.dumps(list(counts.index))
                    chart_values = json.dumps(list(counts.values))
                    message = f"Processed {uploaded_file.filename}"
            except Exception as e:
                message = f"Error processing file: {e}"
    return render_template('pages/one_hour_report.html',
                           title='1-Hour Report',
                           message=message,
                           table_data=table_data,
                           chart_labels=chart_labels,
                           chart_values=chart_values)

@bp.route('/greet/<name>')
def greet(name):
    return f"<p>Hello, {name}!</p>"

@bp.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"
