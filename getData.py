import sqlite3 as db
import folium

data_src = "data/landslides.sql"


my_popup_html="""
<!DOCTYPE html>
<html><head>
<style>
table {{ width: 100%;}}

    table, th, td {{
      border: 1px solid black;
      border-collapse: collapse;
      }}

    th, td {{
      padding: 5px;
      text-align: left;
  }}
  table#t01 tr:nth-child(odd) {{
      background-color: #8e8;
  }}
  table#t01 tr:nth-child(even) {{
      background-color:#fff;
  }}
  </style>
  </head>
  <body>
    <table id="t01">
      <tr> <td>Country</td> <td>{country}</td> </tr>
      <tr> <td>Location</td> <td>{nearest_places}</td> </tr>
      <tr> <td>date</td> <td>{date}</td></tr>
      <tr> <td>Landslide type</td> <td>{landslide_type}</td></tr>
      <tr> <td>Trigger</td> <td>{trigger}</td> </tr>
      <tr> <td>Fatalities</td> <td>{fatalities}</td> </tr>
      <tr> <td>Landslide size</td> <td>{landslide_size}</td></tr>
      <tr> <td>Latitude</td> <td>{latitude}</td></tr>
      <tr> <td>Longitude</td> <td>{longitude}</td></tr>
    </table>

  </body>
  </html>
  """

"""
for _, row in store_data.iterrows():
  try:
    tableFrame = folium.IFrame(html = my_popup_html.format(**row),width =500, height = 300)
    popupTable = folium.Popup(tableFrame, max_width= 500)
    folium.CircleMarker(
      location = [row["latitude"], row["longitude"]],
      radius = 5,
      fill_color = "Brown",
      popup  = popupTable
      ).add_to(landslide_map)
  except:
    pass
"""

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
            tableFrame = folium.IFrame(html = my_popup_html.format(**data), width=500, height=300)
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
