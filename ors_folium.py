import openrouteservice as ors
import folium
from folium.features import DivIcon
import matplotlib.pyplot as plt
import math
import random
import csv

ors_key = '5b3ce3597851110001cf6248c65c806ddb464dfc81512e297135a3a0'
client = ors.Client(key='5b3ce3597851110001cf6248c65c806ddb464dfc81512e297135a3a0')

with open('./map_data/init_coords_day.csv','r') as file:
    reader = csv.reader(file, delimiter=',')
    data_start =[row for row in csv.reader(file)]
    long_csv_start = data_start[1][0]
    lat_csv_start = data_start[1][1]
    day_csv_start = data_start[1][2]
    
long_start=float(long_csv_start)
lat_start=float(lat_csv_start)
day_start=int(day_csv_start)

long_r1=round(random.uniform(-1.5,0),6)
long_r2=round(random.uniform(0,1.5),6)
long_rand=random.choice([long_r1,long_r2])

lat_r1=round(random.uniform(-1.5,-0),6)
lat_r2=round(random.uniform(0,1.5),6)
lat_rand=random.choice([lat_r1,lat_r2])

long_end_in = long_start+long_rand
lat_end_in = lat_start+lat_rand

# longitude - latitude / longitude - latitude

coordinates = [[long_start,lat_start],[long_end_in,lat_end_in]]

long_1 = coordinates[0][0]
lat_1 = coordinates[0][1]
long_2 = coordinates[1][0]
lat_2 = coordinates[1][1]

lat_mean = (lat_1+lat_2)/2
long_mean = (long_1+long_2)/2

route = client.directions(coordinates=coordinates,
                          profile='cycling-road',
                          format='geojson',
                          elevation = True)
cumulative_distances = [] 
elevations = []


previous_route_point =  route["features"][0]["geometry"]["coordinates"][0]
previous_cumulative_distance = 0

for route_point in route["features"][0]["geometry"]["coordinates"]:
    lon_delta = route_point[0]-previous_route_point[0]
    lat_delta = route_point[1]-previous_route_point[1]
    lon_distance = lon_delta * 111  # meters
    lat_distance = lat_delta * 111  # meters
    cumulative_distances.append((lon_distance**2 + lat_distance**2)**0.5+previous_cumulative_distance)
    elevations.append(route_point[2])

    previous_route_point = route_point
    previous_cumulative_distance = cumulative_distances[-1]





distance = route['features'][0]['properties']['segments'][0]['distance']*0.001
duration = route['features'][0]['properties']['segments'][0]['duration']*0.000277778
mean_velocity = distance/duration

hours = math.floor(duration)
minutes = math.floor((duration-hours)*60)
seconds = math.floor(((duration-hours)*60-minutes)*60)

num_coords = len(route['features'][0]['geometry']['coordinates'])

el_plus = 0
el_minus = 0
el_first = 0
el_second = 0

for x in range(1, num_coords):
    el_first = route['features'][0]['geometry']['coordinates'][x-1][2]
    el_second = route['features'][0]['geometry']['coordinates'][x][2]
    el_delta = el_first-el_second
    if el_delta >= 0:
        el_minus = el_minus + el_delta
    else:
        el_plus = el_plus - el_delta

# vettori da usare per la composizione del .csv recap day

lat_arch= []
for xx in range(0, num_coords):
    lat_xx = route['features'][0]['geometry']['coordinates'][xx][1]
    lat_arch.append(lat_xx)

long_arch= []
for zz in range(0, num_coords):
    long_zz = route['features'][0]['geometry']['coordinates'][zz][0]
    long_arch.append(long_zz)
    
alt_arch=[]
for aa in range(0, num_coords):
    alt_aa = route['features'][0]['geometry']['coordinates'][aa][2]
    alt_arch.append(alt_aa)

markers_points = []
for yy in range(0, num_coords):
    markers_points.append([lat_arch[yy],long_arch[yy]])


#map_directions = folium.Map(location=[lat_mean,long_mean],zoom_start=9,tiles="Stamen Terrain")
#map_directions = folium.Map(location=[lat_mean,long_mean],zoom_start=1,tiles="Stamen Watercolor")

if distance <10:
    map_directions = folium.Map(location=[lat_mean,long_mean],zoom_start=10,tiles="Stamen Toner", zoom_control=False)
elif distance <160:
    map_directions = folium.Map(location=[lat_mean,long_mean],zoom_start=9,tiles="Stamen Toner", zoom_control=False)
else:
    map_directions = folium.Map(location=[lat_mean,long_mean],zoom_start=8,tiles="Stamen Toner", zoom_control=False)

# in folium prima lat e poi long

location_start = [lat_1,long_1]
location_end = [lat_2, long_2]

#icon_start = folium.features.CustomIcon('./icons/1.png', icon_size=(50,50))
#icon_end = folium.features.CustomIcon('./icons/2.png', icon_size=(50,50))

folium.GeoJson(route, name='route').add_to(map_directions)


#modifica colore e dimensione del tracciato
folium.PolyLine(markers_points, color='red', weight=50).add_to(map_directions)


folium.Marker(location=location_start, icon=DivIcon(
    icon_size=[50,50],
    html='<div style="font-size: 25pt; text-align:center; color : white">A</div>',
    )).add_to(map_directions)


folium.Marker(location=location_end, icon=DivIcon(
    icon_size=[50,50],
    html='<div style="font-size: 25pt; text-align:center; color : white">B</div>',
    )).add_to(map_directions)

#folium.Marker(location=location_start, icon=icon_start).add_to(map_directions)
#folium.Marker(location=location_end, icon=icon_end).add_to(map_directions)
#folium.Marker(location=location_start).add_to(map_directions)
#folium.Marker(location=location_end, icon=icon_end).add_to(map_directions)

map_directions
map_directions.save('./map_data/map.html')

import os
import time
from selenium import webdriver
##from webdriver_manager.chrome import ChromeDriverManager


delay=5
fn='./map_data/map.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
map_directions.save(fn)

##browser = webdriver.Chrome(ChromeDriverManager().install())
browser = webdriver.Chrome('/usr/bin/chromedriver')
#browser.set_window_size(1080,1080)
browser.get(tmpurl)
time.sleep(delay)
#browser.save_screenshot('map.png')
browser.save_screenshot('./exported_maps/map'+str(day_start)+'.png')
browser.quit()


#aggiunta
#plt.figure(figsize=(5,1.7))
plt.figure(figsize=(8.28,2.4))
plt.tight_layout()
plt.plot(cumulative_distances, elevations, '_', linewidth=4,color='black')
#plt.subplots_adjust(left=0.182,bottom=0.258,right=0.982,top=0.913)
plt.subplots_adjust(left=0.182,bottom=0.458,right=0.982,top=0.913)
plt.locator_params(axis='x',nbins=2)
plt.locator_params(axis='y',nbins=2)

if round(max(elevations))>=1000:
    labeldistance_y = -17.5
elif round(max(elevations))<1000:
    labeldistance_y = -11
        
plt.xlabel("Distance [km]", labelpad=-10)
plt.ylabel("Elevation \n[m.a.s.l.]", labelpad=labeldistance_y)
plt.yticks([0,round(max(elevations))])
plt.xticks([0,max(cumulative_distances)],[0,round(distance)])
plt.savefig('./exported_plots/plot'+str(day_start)+'.png',dpi=200)
#plt.show()
