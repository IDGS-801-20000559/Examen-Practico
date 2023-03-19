from flask import Blueprint, flash, redirect, render_template, request
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from .. import db
from ..models import Bike

bikes = Blueprint('bikes',__name__)

@bikes.route("/comprar")
def comprar():
    flash('Esta función esta en desarrollo')
    bikes = Bike.query.all()    
    return render_template('index.html', bikes=bikes)

@bikes.route("/moduloBici")
@login_required
@roles_accepted('vendedor')
def moduloBici():
    bikes = Bike.query.all()
    return render_template('bikes.html', bikes=bikes)

@bikes.route("/insertarBici", methods=['GET', 'POST'])
@login_required
@roles_accepted('vendedor')
def insertarBici():
    if request.method=='POST':
        nombreBici = request.form.get('name')
        descrip = request.form.get('descripcion')
        precio = request.form.get('precio')
        tipo = request.form.get('tipoBici')
        user_id = current_user.get_id()

        newBike = Bike(nombre = nombreBici,
                        descripcion = descrip,
                        precio = precio,
                        tipo = tipo,
                        idUsuario=user_id)
        
        db.session.add(newBike)
        db.session.commit()
        bikes = Bike.query.all()
        return render_template('bikes.html', bikes=bikes)
    
    return render_template('insert-bike.html')

@bikes.route("/update-bike", methods=['GET', 'POST'])
@login_required
@roles_accepted('vendedor')
def updateBike():
    id = request.args.get('id')
    bike = db.session.query(Bike).filter(Bike.id == id).first()

    if request.method=='POST':
        id = request.form.get('idBike')
        modifBike = db.session.query(Bike).filter(Bike.id == id).first()
        modifBike.nombre = request.form.get('name')
        modifBike.descripcion = request.form.get('descripcion')
        modifBike.precio = request.form.get('precio')
        modifBike.tipo = request.form.get('tipoBici')

        db.session.add(modifBike)
        db.session.commit()
        
        return redirect('moduloBici')
    
    return render_template('update-bike.html', idBike = bike.id,
                                               nombreBike=bike.nombre, 
                                               descBike=bike.descripcion,
                                               precioBike=bike.precio,
                                               tipoBike = bike.tipo)

@bikes.route("/delete-bike", methods=['GET', 'POST'])
@login_required
@roles_accepted('vendedor')
def deleteBike():
    id = request.args.get('id')
    bike = db.session.query(Bike).filter(Bike.id == id).first()

    if request.method=='POST':
        id = request.args.get('id')
        bikeD = db.session.query(Bike).filter(Bike.id == id).first()

        db.session.delete(bikeD)
        db.session.commit()
        return redirect('moduloBici')
    
    return render_template('delete-bike.html', bike=bike)