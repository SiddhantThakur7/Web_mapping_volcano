import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elevation  = list(data["ELEV"])
name = list(data["NAME"])

def color_decision(ele):
    if ele < 1000:
        return "green"
    elif ele<3000 and ele>=1000:
        return "orange"
    else:
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles = "Stamen Terrain")

fg1 = folium.FeatureGroup(name="Volcanoe Locations")

for lt, ln, e, name in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html=html % (name, name, e), width=150, height=80)
    fg1.add_child(folium.CircleMarker(location = [lt, ln], radius = 7, popup =folium.Popup(iframe), fill_color = color_decision(e), color = 'grey', fill = True, fill_opacity = 0.7))

fg2 = folium.FeatureGroup(name="Population")
fg2.add_child(folium.GeoJson(data = open("world.json", 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg1)
map.add_child(fg2)

map.add_child(folium.LayerControl())

map.save("Map1.html")