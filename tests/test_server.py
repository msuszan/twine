from flask import Flask, render_template
test_server = Flask(__name__)

@test_server.route("/")
def index():
  return render_template("index.html")

@test_server.route("/link")
def link():
  return render_template("link.html")

if __name__ == "__main__":
    test_server.run()
