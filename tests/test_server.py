from flask import Flask
test_server = Flask(__name__)

@test_server.route("/")
def index():
  return "Hello World!"

if __name__ == "__main__":
    test_server.run()
