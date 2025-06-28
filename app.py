from flask import Flask
from routes import bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "change-me"  # simple secret for session management
    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
