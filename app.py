from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/<path:filename>")
def static_files(filename):
  return send_from_directory('.', filename)

@app.route("/sounds/<path:filename>")
def sounds(filename):
  return send_from_directory("sounds", filename)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)
