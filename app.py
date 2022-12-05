from flask import Flask, render_template, jsonify
from datetime import datetime
from main import getData

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def date():
    cg, br = getData()
    if cg > br:
        data = f"We are {cg-br} points ahead!"
    elif br > cg:
        data = f"We are {br-cg} points behind!"
    elif br == cg:
        data = f"We are tied at {cg} points!"
    return jsonify(data)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)