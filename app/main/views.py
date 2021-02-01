from flask import render_template, request, Response
from . import main
from ..models import User
from .utils import *
from .realtime_face_swapping import *


@main.route('/', methods = ['GET'])
def index():
    user = User(name="Daniel", lastname="Limas", lastname_2="Palma", email="a@gmail.com", procedure="Teeth whitening")
    global option
    """Video streaming"""
    if request.method == 'GET':
        result = request.form
        option = result
        return render_template('index.html', option = result, user=user)
    else:
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


@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')
