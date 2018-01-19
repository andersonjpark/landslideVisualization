# Nasa Space App Challenge

## Landslide Visualization

Makes a map showing all the landslides cases. Pressing the circle gives information about that case.

Source: https://data.nasa.gov/dataset/Global-Landslide-Catalog-Export/dd9e-wu2v/data

### Screenshot

![alt tag](https://github.com/jspark971/landslideVisualization/blob/master/visualization_example.png)


![alt tag](https://github.com/jspark971/landslideVisualization/blob/master/popUp_example.png)

## What should be done

1. Need to finish developing the searchbar [DONE]
2. Need to work on how to template the popup html file [DONE]
3. Made a child template, "map_page.html", which is a new way of bringing the map. could be used
for relocating the map [DONE]
4. Develop a function that filters the map depending on the search result, making a cluster around the search area so that we don't have to make pop up table for areas that is not in the search area ( use the pandas filter function) [DONE]
5. Modifying the python from 2 to 3, for deployment [DONE]
6. Randomly choosing 100 landslides for the origin html using pd.samples()
7. Changing folium into JS for using the popUp.html to increase the speed.
8. Deploying the Flask app on Heroku
