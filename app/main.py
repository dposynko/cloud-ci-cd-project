import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "CI/CD Pipeline is working!"

@app.route("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.route("/version")
def version():
    # This will be set at deploy time (GitHub SHA)
    return jsonify(version=os.getenv("APP_VERSION", "unknown")), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
