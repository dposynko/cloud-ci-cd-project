from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CI/CD Pipeline is working!"

@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # Dev only. In production prefer gunicorn:
    # gunicorn -w 2 -b 0.0.0.0:5000 main:app
    app.run(host="0.0.0.0", port=5000, debug=False)
