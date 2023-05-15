# Test bot
# From start tu day `n`

import csv
import os

def initialize_bot():
    #inizializza csv a lat long iniziali, svuota cartella dalle immagini
    with open('./map_data/init_coords_day.csv','w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['longitude','latitude','day'])
        writer.writerow([8.9142,45.5983, 1])

    try: 
        os.remove("./map_data/map.html")

    except:
        pass

def run_bot(n):
    #esegue il codice `n` volte, generando `n` immagini
    for i in range(n):
        exec(open('./ors_folium_no_errors.py').read())

    initialize_bot()


initialize_bot()

n_trip_days = 30
run_bot(n_trip_days)
