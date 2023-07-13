from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime
from main import getData
import json

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def data():
    cg, br = getData()
    data = {"cg": cg, "br": br}
    return jsonify(data)

@app.route('/creds-invalid', methods=['GET'])
def creds_invalid():
    return render_template("creds-invalid.html")

@app.route('/creds', methods=['GET', 'POST'])
def creds():
    if request.method == 'POST':
        data = getData()
        print(data)
        if data == ({'points': 0, 'position': 0}, {'points': 0, 'position': 0}):
            return redirect('/creds-invalid')
        else:
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
