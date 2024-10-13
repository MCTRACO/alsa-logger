from time import sleep

import requests
from datetime import datetime
import json



class stop:
    def __init__(self,id,name):
        self.name=name
        self.id=id
        self.previous = self.update()
        self.routes = [element[0] for element in self.previous]
    def update(self):
        out = []
        data = requests.get(
            f"http://urbanos.guadalajara.es/SSIIMovilWS/ws/cons/tiemposParada.json?codParada={self.id}").json()
        for line in data["tiempos"]:
            out.append((line["itinerario"]["linea"]["cod"], line["minutos"],False))
        return out
    def check(self):
        current = self.update()
        arrived =  []
        i= 0
        for bus in current:

            print(bus[1])
            print(bus[2])
            if bus[1] == 0:
                bus[2] = True
            elif bus[1] != 0 and bus[2] == True: # not 0 and previous 0
                bus[2] = False
                arrived.append(bus[0])
                print("ARRIVED")
            i += 1
            self.previous = current #update old one
        return arrived
#define stops to search
Supera = stop("306","Supera")

#create dict
all_stops = [Supera]
for stop in all_stops:
    to_write[stop.name] = {}
    for route in stop.routes:
        to_write[stop.name][route] = []


arrived = ["C2"]
for bush in arrived:
    to_write[stop.name][bush].append(get_time())

save()
