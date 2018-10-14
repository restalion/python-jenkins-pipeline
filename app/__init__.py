from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config")

from app.module_one.controllers import module_one

app.register_blueprint(module_one)