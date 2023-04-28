from app import app
from app.utils.secrets import getSecrets
import mongoengine.errors
import requests
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Farm 
from app.classes.forms import FarmForm
from flask_login import login_required
import datetime as dt

def updateLatLon(farm):
    # get your email address for the secrets file
    secrets=getSecrets()
    # call the maps API with the address
    url = f"https://nominatim.openstreetmap.org/search?street={farm.streetAddress}&city={farm.city}&state={farm.state}&postalcode={farm.zip}&format=json&addressdetails=1&email={secrets['MY_EMAIL_ADDRESS']}"
    # get the response from the API
    r = requests.get(url)
    # Find the lat/lon in the response
    try:
        r = r.json()
    except Exception as error:
        flash(f"unable to retrieve lat/lon: {error}")
        return(farm)
    else:
        if len(r) != 0:
            # update the database
            farm.update(
                lat = float(r[0]['lat']),
                lon = float(r[0]['lon'])
            )
            flash(f"farm lat/lon updated")
            return(farm)
        else:
            flash('unable to retrieve lat/lon')
            return(farm)

@app.route("/farm/fav/<farmId>")
@login_required
def farmFav(farmId):
    thisFarm=Farm.objects.get(id=farmId)
    if thisFarm.fav:
        thisFarm.update(fav=False)
    else:
        thisFarm.update(fav=True)
    return redirect(url_for('farmList'))

@app.route("/farm/favs")
@login_required
def farmFavs():
    farms=Farm.objects(fav=True)
    return render_template("farmlist.html",farms=farms)

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
            farmType = form.farmType.data, 
            price = form.price.data, 
            name = form.name.data, 
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
            )
        # This is a method that saves the data to the mongoDB database.
        newFarm.save()
        newFarm = updateLatLon(newFarm)
        return redirect(url_for('farm',farmId=newFarm.id))
    return render_template('farmform.html',form=form)

@app.route('/farm/edit/<farmId>', methods=['GET', 'POST'])
@login_required
def farmEdit(farmId):
    form = FarmForm()  
    thisFarm = Farm.objects.get(id=farmId)
    if form.validate_on_submit():
        print(thisFarm)
        thisFarm.update(
            streetAddress = form.streetAddress.data,
            zip = form.zipCode.data,
            city = form.city.data,
            state = form.state.data,
            farmType = form.farmType.data, 
            price = form.price.data, 
            name = form.name.data, 
            modify_date = dt.datetime.utcnow
            )
        thisFarm = updateLatLon(thisFarm) 
        # This is a method that saves the data to the mongoDB database.
        thisFarm.save()
        return redirect(url_for('farm',farmId=thisFarm.id))
    
    form.streetAddress.data = thisFarm.streetAddress
    form.zipCode.data = thisFarm.zip
    form.city.data = thisFarm.city
    form.state.data = thisFarm.state
    form.farmType.data = thisFarm.farmType
    form.price.data =thisFarm.price
    form.name.data = thisFarm.name
    
    return render_template('farmform.html',form=form)

@app.route('/farm/<farmId>')
def farm(farmId):
    print(farmId)
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

@app.route('/farm/map')
@login_required
def farmMap():

    farms = Farm.objects()

    return render_template('farmlocator.html',farms=farms)