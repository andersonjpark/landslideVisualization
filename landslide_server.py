from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
import pandas as pd
import numpy as np
import folium
import os
import geocoder

from getData import getData

app = Flask(__name__)
currentMap = [None]

@app.route("/",)
def map():
    landslide_map = getData([[-180,-70],[180,80]])
    currentMap[0] = landslide_map
    return render_template("layout.html", view_map = landslide_map)

@app.route("/location/<name>")
def relocate(name):
	g = geocoder.google(name)
	x,y = g.lat,g.lng
        if g.status == 'OK':
          landslide_map = getData( [g.southwest, g.northeast] )
          currentMap[0] = landslide_map
          return render_template("layout.html",
                                 view_map = landslide_map,
                                 location = name)
        else:
          print "Going to the Default"
          return render_template("layout.html",
                                 view_map = currentMap[0],
                                 location = 'Not found',
                                 error    = "Could not locate {}".format(name))

@app.route("/<name>/<location>")
def sayhiatplace(name, location):
  return render_template('basic.html', name=name, location=location)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host = '0.0.0.0', port = port, debug = True)
