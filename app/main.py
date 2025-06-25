from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Yes, you have internet!", 200

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
