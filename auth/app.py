from flask import Flask
from auth_api import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

