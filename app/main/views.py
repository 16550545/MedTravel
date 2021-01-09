from flask import render_template
from . import main
from ..models import User

@main.route('/')
def index():
    user = User(name="Daniel", lastname="Limas", lastname_2="Palma", email="a@gmail.com", procedure="Teeth whitening")
    return render_template('index.html', user=user)