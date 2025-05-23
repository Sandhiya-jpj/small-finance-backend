import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this env variable
    app.run(host="0.0.0.0", port=port)        # Bind to all interfaces
