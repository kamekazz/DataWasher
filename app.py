from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/greet/<name>")
def greet(name):
    return f"<p>Hello, {name}!</p>"

@app.route('/handle_url_params')
def handle_url_params():
    greeting = request.args.get('greeting', 'default_value1')
    name = request.args.get('name', 'default_value2')
    return f"<h2>greeting: {greeting}, name: {name}</h2>"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)