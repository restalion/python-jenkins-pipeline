from flask import Blueprint, request, render_template

module_one = Blueprint("auth", __name__, url_prefix="/auth")

@module_one.route("/hello")
def hello():
    return render_template("module_one/hello.html")