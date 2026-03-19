import os
from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, CYOM 569! CI Pipeline is running."


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    # Host/port from env (default localhost; Docker sets HOST=0.0.0.0).
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port)
