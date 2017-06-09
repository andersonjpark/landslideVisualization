from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
import pandas as pd
import numpy as np
import folium
import os
import geocoder


store_data = pd.read_csv("global_landslides.csv")
landslide_map = folium.Map(tiles="Stamen Terrain", zoom_start = 6)
store_data = store_data[:1000]

app = Flask(__name__)

def makePopUp():
  return render_template('popUp.html', **row)
      #return render_template('popUp.html',country =row["country"],
      #nearest_places = row["nearest_places"], date = row["date"],
      #landslide_type = row["landslide_type"],trigger = row["trigger"],
      #fatalities = row["fatalities"],landslide_size= row["landslide_size"],
      #latitude= row["latitude"],longitude= row["longitude"])

for _, row in store_data.iterrows():
  try:
    makePopUp() # render_template does not return html
    tableFrame = folium.IFrame(html = ,width =500, height = 300)
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
  #Problem: for some reason it does not make the fun the init_map()
  #         which is a function that makes the map with the dots
  #         This is the reason why when i first run the program, the map is okay
  #         but when i shift the location, the dots go away
  #         I currently made the first call work by templating the html file made before

  #myhtml = open("my_map.html")
  #return myhtml.read()
  #replace the code with this after solving the problem.
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