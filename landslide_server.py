from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
import pandas as pd
import numpy as np
import folium
import os
import geocoder

from getData import getData

#store_data = pd.read_csv("global_landslides.csv")
#landslide_map = folium.Map(tiles="Stamen Terrain", zoom_start = 6)
#store_data = store_data[:100]

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
        print name, g, g.status
        # geocoder comes with a built-in bounding box
        # this is a better solution than always giving a +/ 10 degrees
        # The BB is a little narrow, so we
        if g.status == 'OK':
          landslide_map = getData( [g.southwest, g.northeast] )
          currentMap[0] = landslide_map
          return render_template("layout.html",
                                 view_map = landslide_map,
                                 location = name)
        else:
          print "Going to the default"
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
