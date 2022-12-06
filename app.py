from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime
from main import getData
import json

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def date():
    cg, br = getData()
    if cg > br:
        data = f"We are {cg-br} points ahead!"
    elif br > cg:
        data = f"We are {br-cg} points behind!"
    elif br == 0 and cg == 0:
        return jsonify("No Credentials Provided")
    elif br == cg:
        data = f"We are tied at {cg} points!"
    return jsonify(data)

@app.route('/creds', methods=['GET', 'POST'])
def creds():
    if request.method == 'POST':
        with open('creds.json', 'w') as f:
            json.dump(request.form, f, indent=4)
        return redirect('/')
    elif request.method == 'GET':
        return render_template("creds.html")
    else:
        return jsonify("Invalid Method")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)