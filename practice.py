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

def shift_map(x,y):
  try:
  	bb = [[x - 10, y-10],[x+10,y+10]]
  except:
    bb = [[-130,30],[-120,40]]
  landslide_map.fit_bounds(bb)
  return landslide_map._repr_html_()

@app.route("/")
def hello():
  return landslide_map._repr_html_()

@app.route("/<name>")
def sayhi(name):
	g = geocoder.google(name)
	x,y = g.lat,g.lng

	return shift_map(x,y)

@app.route("/<name>/<location>")
def sayhiatplace(name, location):
  return render_template('layouts.html', name=name, location=location)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host = '0.0.0.0', port = port, debug = True)