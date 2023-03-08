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
            address = form.streetAddress.data,
            zip = form.zipCode.data,
            city = form.city.data,
            state = form.state.data,
            type = form.type.data, 
            picture = form.picture.data,
            price = form.price.data, 
            name = form.name.data, 
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
            )
        # This is a method that saves the data to the mongoDB database.
        newFarm.save()
        return redirect(url_for('farm',farmID=newFarm.id))
    return render_template('farmform.html',form=form)

@app.route('/farm/<farmId>')
def farm(farmId):
    thisFarm = Farm.objects.get(id=farmId)
    return render_template('farm.html',farm=thisFarm)