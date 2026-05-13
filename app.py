from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CS665 Project 3 is running!"

if __name__ == "__main__":
    app.run(debug=True)
