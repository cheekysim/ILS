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
    elif br == 0 and cg == 0:
        return jsonify("No Credentials Provided")
    return jsonify(data)

@app.route('creds')
def creds():
    return render_templa("creds.html")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)