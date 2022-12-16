from flask import Flask, render_template, jsonify, request, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from main import getData
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

with open('auth.json', "r") as f:
    logins = json.load(f)
    print(logins)

users = {username: generate_password_hash(password) for username, password in logins.items()}

@auth.verify_password
def veify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/data', methods=['GET'])
def date():
    cg, br = getData()
    data = {"cg": cg, "br": br}
    return jsonify(data)

@app.route('/creds', methods=['GET', 'POST'])
@auth.login_required
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
