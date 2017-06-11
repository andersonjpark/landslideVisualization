from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
import pandas as pd
import numpy as np
import folium
import os
import geocoder


store_data = pd.read_csv("global_landslides.csv")
landslide_map = folium.Map(tiles="Stamen Terrain", zoom_start = 6)
store_data = store_data[:100]

app = Flask(__name__)

def makePopup():
  return render_template('popUp.html', **row)

for _, row in store_data.iterrows():
  try:
    myPopUp = makePopUp() 
    tableFrame = folium.IFrame(html = myPopUp,width =500, height = 300)
    popupTable = folium.Popup(tableFrame, max_width= 500)
    folium.CircleMarker(
      location = [row["latitude"], row["longitude"]],
      radius = 5,
      fill_color = "Brown",
      popup  = popupTable
      ).add_to(landslide_map)
  except:
    pass

@app.route("/")
def hello():
  return landslide_map._repr_html_()

@app.route("/location/<name>")
def relocate(name):
  g = geocoder.google(name)
  x,y = g.lat,g.lng
        print name, g, g.status
        # geocoder comes with a built-in bounding box
        # this is a better solution than always giving a +/ 10 degrees
        # The BB is a little narrow, so we
        if g.status == 'OK':
          landslide_map.fit_bounds( [g.southwest, g.northeast] )
          return render_template("map_page.html",
                                 view_map = landslide_map,
                                 location = name)
        else:
          print "Going to the default"
          return render_template("map_page.html",
                                 view_map = landslide_map,
                                 location = 'Not found',
                                 error    = "Could not locate {}".format(name))

@app.route("/<name>/<location>")
def sayhiatplace(name, location):
  return render_template('layouts.html', name=name, location=location)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host = '0.0.0.0', port = port, debug = True)