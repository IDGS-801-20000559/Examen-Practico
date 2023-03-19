#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, render_template
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required, roles_accepted
#Importamos el objeto de la BD desde __init__.py
from . import db
from .models import Bike

main = Blueprint('main',__name__)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    # Para poder realizar una consulta usando SQLAlchemy
    bikes = Bike.query.all()
    return render_template('index.html',
                           bikes = bikes)
    
@main.route('/contacto')
def contacto():
    
    return render_template('contactanos.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
# El usuario tiene que pertenecer a TODOS los roles
# @roles_required('admin')
# El usuario tiene que pertenecer a al menos UNO de los roles
@roles_accepted('admin', 'vendedor')
def profile():
    return render_template('profile.html', name=current_user.name)
