from flask import render_template, request
from . import main
from ..models import User
from .utils import *

@main.route('/')
def index():
    user = User(name="Daniel", lastname="Limas", lastname_2="Palma", email="a@gmail.com", procedure="Teeth whitening")
    return render_template('index.html', user=user)


@main.route('/email', methods=['POST'])
def email():
    pname = request.form['name']
    plastname = request.form['lastname']
    pemail = request.form['email']
    pphone = request.form['phone']
    pprocedure = request.form['procedure']

    sbj = 'Nueva Solicitud: '+ pname + ' ' +plastname
    cnt =  'Hola soy '+pname+' '+plastname+' me gustaría saber mas sobre el procedimiento: '+pprocedure+'<br>Esta es mi información: <br><strong>Correo: </strong>'+pemail+'<br><strong>Telefono: </strong>'+pphone

    send_email(sbj, cnt)

    return ('Your message has been sent. Thank you!')
