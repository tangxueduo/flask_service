from flask import Flask,request, abort, redirect, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route("/login/<name>")
def hello_world(name):
    return f"Hello, {escape(name)}!"


# ---------------
@app.route('/login')
def login():
    abort(401)

@app.route('/')
def index():
    return redirect(url_for('login'))
# -----------------


