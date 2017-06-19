import sqlite3 as db
import folium
from flask import render_template

data_src = "data/landslides.sql"


def getData( bounding_box, limit=600 ):
    conn = db.connect(data_src)
    conn.row_factory = db.Row
    cursor = conn.cursor()

    landslide_map = folium.Map(tiles="Stamen Terrain", zoom_start = 6)
    landslide_map.fit_bounds(bounding_box)

    query = """SELECT country,nearest_places,date,landslide_type,trigger, fatalities, landslide_size, latitude, longitude
                FROM LANDSLIDES WHERE
                latitude < {} and latitude > {} and
                longitude < {} and longitude > {} order by landslide_size DESC LIMIT {}"""
    print bounding_box
    query = query.format(bounding_box[1][0], bounding_box[0][0],
                         bounding_box[1][1], bounding_box[0][1], limit)
    print query
    N = 0
    for data in cursor.execute(query):
        try:
            N = N+1
            tableFrame = folium.IFrame(html = render_template("popup.html", column = data), width=500, height=300)
            popupTable = folium.Popup(tableFrame, max_width = 500)
            folium.CircleMarker(
                location = [data["latitude"], data["longitude"]],
                radius = 5,
                fill_color = "Brown",
                popup  = popupTable
            ).add_to(landslide_map)
        except Exception as e:
            print "ERROR:" + str(e)
            pass
    print "N = ", N
    return landslide_map
