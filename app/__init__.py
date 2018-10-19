from flask import Flask
from app.module_one.controllers import module_one


app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(module_one)
