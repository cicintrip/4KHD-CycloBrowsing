import csv
from geopy.geocoders import Nominatim

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import PIL.ImageOps

for _ in range(100):
    try:
        exec(open('ors_folium.py').read())
        break
    except Exception as e:
        print(e)
        continue
else:
    pass


long_end = coordinates[1][0]
lat_end = coordinates[1][1]
day_end = day_start+1

header = ['longitude','latitude','day']
data_end = [long_end, lat_end, day_end]

with open('./map_data/init_coords_day.csv','w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(header)
    writer.writerow(data_end)
   
# find city from coordinates
geolocator = Nominatim(user_agent='francesco.garavaglia11@gmail.com')
location_start = geolocator.reverse(str(lat_start)+","+str(long_start), language='en')
location_end = geolocator.reverse(str(lat_end)+","+str(long_end), language='en')

try:
    try:
        try:
            try:
                city_start = location_start.raw['address']['city']
            except:
                city_start = location_start.raw['address']['hamlet']
        except:
            city_start = location_start.raw['address']['village']
    except:
        city_start = location_start.raw['address']['town']
except:
    city_start = location_start.raw['address']['county']
    
try:
    try:
        try:
            try:
                city_end = location_end.raw['address']['city']
            except:
                city_end = location_end.raw['address']['hamlet']
        except:
            city_end = location_end.raw['address']['village']
    except:
        city_end = location_end.raw['address']['town']
except:
    city_end = location_end.raw['address']['county']

#city_start = location_start.raw['address']['city']
#city_end = location_end.raw['address']['city']

country_start = location_start.raw['address']['country']
country_end = location_end.raw['address']['country']

print('Day:',day_start)
print('From',city_start,'('+country_start+')','To',city_end,'('+country_end+')')
print('Total distance:',round(distance,1),'km')
print('Total time:',hours, 'h',minutes,'min',seconds,'s')
print('Mean velocity:',round(mean_velocity,1),'km/h')
print('Total climb:',round(el_plus),'m')
print('Total descent:',round(el_minus),'m')

## OUTPUT GRAFICO

#W,H =(1080,1080)
W,H =(864,1080)
background = Image.new(mode='RGB',size=(W,H),color=(255,255,255))

title = Image.open('./icons/ciclo-bro-logo-01.jpg')
w_title,h_title = title.size
title = title.resize((round(w_title/4.5),round(h_title/4.5)))
w_title,h_title = title.size
title = title.filter(ImageFilter.GaussianBlur(1.2))
background.paste(title,(round((W-w_title)/2-6),-68))


plot = Image.open('./exported_plots/plot'+str(day_start)+'.png')
plot = plot.resize((828,240))
w_plot, h_plot = plot.size
background.paste(plot,(round((W-w_plot)/2)-43,910))

img = Image.open('./exported_maps/map'+str(day_start)+'.png')

# left, top, right, bottom
img = img.crop((3,18,893,778))
img = img.resize((712,616))
w_img, h_img = img.size

frame=Image.new(mode='RGB',size=(w_img+2,h_img+2),color=(0,0,0))

background.paste(frame,(round((W-w_img-2)/2),round((H-h_img-2)/2)+25+25+10+2))
background.paste(img,(round((W-w_img)/2),round((H-h_img)/2)+25+25+10+2))


start_city = str(city_start)
len_city_start = len(start_city)
end_city = str(city_end)
len_city_end = len(end_city)
max_len = max(len_city_start,len_city_end)

if max_len > 19:
    font= ImageFont.truetype("./font/Roboto-Regular.ttf",24)
    font_italic = ImageFont.truetype("./font/Roboto-Italic.ttf",22)
    font_day = ImageFont.truetype("./font/Roboto-Regular.ttf",20)
    h_country = 174
else:
    font= ImageFont.truetype("./font/Roboto-Regular.ttf",34)
    font_italic = ImageFont.truetype("./font/Roboto-Italic.ttf",24)
    h_country = 184
    font_day = ImageFont.truetype("./font/Roboto-Regular.ttf",22)

font_stats= ImageFont.truetype("./font/Roboto-Regular.ttf",22) 
draw = ImageDraw.Draw(background)


w_start_city, h_start_city = draw.textsize(start_city, font=font)
draw.text((round((W/2-w_start_city)/2),92+20+30+2),start_city,(0,0,0),font=font)

start_country = str(country_start)
w_start_country, h_start_country = draw.textsize(start_country, font=font_italic)
draw.text(((round((W/2-w_start_country)/2)),h_country),start_country,(0,0,0),font=font_italic)


w_end_city, h_end_city = draw.textsize(end_city, font=font)
draw.text((round(W/2+(W/2-w_end_city)/2),92+20+30+2),end_city,(0,0,0),font=font)

end_country = str(country_end)
w_end_country, h_end_country = draw.textsize(end_country, font=font_italic)
draw.text(((round(W/2+(W/2-w_end_country)/2)),h_country),end_country,(0,0,0),font=font_italic)

# DELIRIO FRECCE

import math

freccia1 = "> "
freccia2 = "> "
w_freccia1,h_freccia1 = draw.textsize(freccia1, font=font)
w_freccia2,h_freccia2 = draw.textsize(freccia2, font=font)

w_max_start = max(w_start_city,w_start_country)
w_max_end = max(w_end_city,w_end_country)
w_distance = round((W-w_max_start-w_max_end)/2)
n_freccia1 = math.floor(w_distance/w_freccia1)

for iii in range(1,n_freccia1):
    draw.text((round(W/4+w_max_start/2)+iii*w_freccia1,115+35+2),freccia1,(0,0,0),font=font)

n_freccia2 = math.floor(w_distance/w_freccia1)-1

for jjj in range(1,n_freccia2):
    draw.text((round(W/4+w_max_start/2+w_freccia1/2)+jjj*w_freccia2,115+15+35+2),freccia2,(0,0,0),font=font)
    
day = "Day "+str(day_start)
w_day,h_day = draw.textsize(day, font=font_day)

if max_len > 19:
    if day_start<10:
        ooo=1
    elif day_start<100:
        ooo=1.5
    else:
        ooo=2
else:
    if day_start<10:
        ooo=0.5
    elif day_start<100:
        ooo=1
    else:
        ooo=1.5

if n_freccia1%2:
    draw.text((round(W/4+w_max_start/2+w_freccia1/2)+(jjj-ooo)*w_freccia2/2,115+10+5+2),day,(0,0,0),font=font_day)
else:
    draw.text((round(W/4+w_max_start/2)+(iii-ooo)*w_freccia1/2,115+10+5+2),day,(0,0,0),font=font_day)


#freccia = Image.open('./icons/straight.png')
#freccia = freccia.resize((60,60))
#w_freccia, h_freccia = freccia.size
#background.paste(freccia,(round((W-w_freccia)/2),100+20))

#w_city_max = max(w_start_city,w_end_city)
#
#if w_city_max<150:
#    freccia1 = "> > > > > > > > > >"
#    freccia2 = " > > > > > > > > > "
#elif 150<=w_city_max<180:
#    freccia1 = "> > > > > > > > >"
#    freccia2 = " > > > > > > > > "
#elif 180<=w_city_max<220:
#    freccia1 = "> > > > > > > >"
#    freccia2 = " > > > > > > > "
#elif 220<=w_city_max<240:
#    freccia1 = "> > > > > > >"
#    freccia2 = " > > > > > > "
#elif 240<=w_city_max<275:
#    freccia1 = "> > > > > >"
#    freccia2 = " > > > > > "
#elif 275<=w_city_max<300:
#    freccia1 = "> > > > >"
#    freccia2 = " > > > > "
#elif 300<=w_city_max<320:
#    freccia1 = "> > > >"
#    freccia2 = " > > > "
#elif 320<=w_city_max<340:
#    freccia1 = "> > >"
#    freccia2 = " > > "
#elif 340<=w_city_max<380:
#    freccia1 = "> >"
#    freccia2 = " > "
#elif w_city_max>=380:
#    freccia1 = ">"
#    freccia2 = " " 
# 
#w_freccia1,h_freccia1 = draw.textsize(freccia1, font=font)
#w_freccia2,h_freccia2 = draw.textsize(freccia2, font=font)
#draw.text((round((W-w_freccia1)/2),115),freccia1,(0,0,0),font=font)
#draw.text((round((W-w_freccia2)/2),115+15),freccia2,(0,0,0),font=font)

stats_out = 'Total distance: '+str(round(distance))+'km || Total time: '+str(hours)+'h '+str(minutes)+'min '+str(seconds)+'s || Average speed: '+str(round(mean_velocity,1))+'km/h'
w_stats_out, h_stats_out = draw.textsize(stats_out, font=font_stats)
draw.text((round((W-w_stats_out)/2),172+30+20+2),stats_out,(0,0,0),font=font_stats)

stats_out2 = 'Uphill: '+str(round(el_plus))+'m /\ Downhill: '+str(round(el_minus))+'m'
w_stats_out2, h_stats_out2 = draw.textsize(stats_out2, font=font_stats)
draw.text((round((W-w_stats_out2)/2),212+20+20+2),stats_out2,(0,0,0),font=font_stats)

background = background.filter(ImageFilter.GaussianBlur(1))
background = background.filter(ImageFilter.CONTOUR)
background = background.filter(ImageFilter.SHARPEN)
#background = PIL.ImageOps.invert(background)
background.save('./exported_images/temap'+str(day_start)+'.png')


## OUTPUT STATISTICHE
#csv export per recap giornata con statistiche e long e lat

header_stats = ['day','city start','country start','city end','country end','total distance [km]','total time [h]','mean velocity [km/h]','total climb [m]','total descent [m]']
general_data = [day_start, city_start, country_start, city_end, country_end, distance, duration, mean_velocity, el_plus, el_minus]
geo_header = ['longitude','latitude','altitude']

with open('./map_data/stats_day'+str(day_start)+'.csv','w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(header_stats)
    writer.writerow(general_data)
    writer.writerow(geo_header)
    for qq in range(0,num_coords):
        writer.writerow([long_arch[qq],lat_arch[qq],alt_arch[qq]])
        
