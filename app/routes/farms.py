from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Farm 
from app.classes.forms import FarmForm
from flask_login import login_required
import datetime as dt

@app.route('/farm/new', methods=['GET', 'POST'])
@login_required
def farmNew():
    form = FarmForm()  
    if form.validate_on_submit():
        newFarm = Farm(
            streetAddress = form.streetAddress.data,
            zip = form.zipCode.data,
            city = form.city.data,
            state = form.state.data,
            type = form.type.data, 
            price = form.price.data, 
            name = form.name.data, 
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
            )
        # This is a method that saves the data to the mongoDB database.
        newFarm.save()
        return redirect(url_for('farm',farmId=newFarm.id))
    return render_template('farmform.html',form=form)

@app.route('/farm/edit/<farmId>', methods=['GET', 'POST'])
@login_required
def farmEdit(farmId):
    form = FarmForm()  
    thisFarm = Farm.objects.get(id=farmId)
    if form.validate_on_submit():
        thisFarm.update(
            streetAddress = form.streetAddress.data,
            zip = form.zipCode.data,
            city = form.city.data,
            state = form.state.data,
            type = form.type.data, 
            price = form.price.data, 
            name = form.name.data, 
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
            )
        # This is a method that saves the data to the mongoDB database.
        thisFarm.save()
        return redirect(url_for('farm',farmId=thisFarm.id))
    
    form.streetAddress.data = thisFarm.streetAddress,
    form.zipCode.data = thisFarm.zip,
    form.city.data = thisFarm.city,
    form.state.data = thisFarm.state,
    form.type.data = thisFarm.type, 
    form.price.data =thisFarm.price, 
    form.name.data = thisFarm.name, 
    current_user.id = thisFarm.author,
    
    return render_template('farmform.html',form=form)

@app.route('/farm/<farmId>')
def farm(farmId):
    thisFarm = Farm.objects.get(id=farmId)
    return render_template('farm.html',farm=thisFarm)

@app.route('/farm/delete/<farmId>')
@login_required
def farmDelete(farmId):
    deleteFarm = Farm.objects.get(id=farmId)

    deleteFarm.delete()
    flash('The farm location was deleted.')
    return redirect(url_for('farmList'))

@app.route('/farm/list')
def farmList():
    farms=Farm.objects()
    return render_template('farmlist.html',farms=farms)