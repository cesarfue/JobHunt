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
    Config.PROMPTS_DIR.mkdir(exist_ok=True)

    print(f"Server starting...")
    print(f"Applications folder: {Config.APPLICATIONS_DIR}")
    print(f"Prompts folder: {Config.PROMPTS_DIR}")
    print(f"Excel file: {Config.EXCEL_FILE}")
    print(f"Resume script: {Config.RESUME_SCRIPT}")

    app.run(debug=True, port=5000)
