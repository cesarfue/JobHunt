from config import Config
from flask import Flask
from flask_cors import CORS
from routes import job_routes

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

app.register_blueprint(job_routes.bp)

if __name__ == "__main__":
    Config.APPLICATIONS_DIR.mkdir(exist_ok=True)

    app.run(debug=True, port=5000)
