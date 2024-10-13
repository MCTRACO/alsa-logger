
from time import sleep

import requests
from datetime import datetime,timedelta
import json


check_stops=[("306","Supera"),("124","Biona")]
min_interval=5
class stopc:
    def __init__(self,id,name):
        self.name=name
        self.id=id
        self.data = self.get_start()
        self.routes = [element["code"] for element in self.data]

    def get_start(self):
        out = []
        data = requests.get(
            f"http://urbanos.guadalajara.es/SSIIMovilWS/ws/cons/tiemposParada.json?codParada={self.id}").json()
        for line in data["tiempos"]:

            out.append({"code": line["itinerario"]["linea"]["cod"], "time": line["minutos"], "reach0": False,"lastTime":get_time() })
        return out
    def update(self):
        out = []
        data = requests.get(
            f"http://urbanos.guadalajara.es/SSIIMovilWS/ws/cons/tiemposParada.json?codParada={self.id}").json()
        i=0
        for line in data["tiempos"]:
            self.data[i]["time"] = line["minutos"]
            i +=1
    def check(self):
        self.update()
        arrived =  []
        i= 0
        for bus in self.data:
            print(bus)
            if bus["time"] == 0:
                bus["reach0"] = True
            elif bus["time"] != 0 and bus["reach0"] == True:
                date_str = "2024-10-01"  # Example date
                # Convert the time strings to datetime objects
                time1 = datetime.strptime(get_time(), "%H:%M:%S")
                time2 = datetime.strptime(bus["lastTime"], "%H:%M:%S")
                time_difference = abs(time2 - time1)
                if time_difference > timedelta(minutes=min_interval):
                    bus["reach0"] = False
                    bus["lastTime"] = get_time()
                    arrived.append(bus["code"])


            i += 1
        return arrived

def save():
    with open('output.json', 'w') as json_file:
        json.dump(to_write, json_file, indent=4)
        print("saved")

def get_time():
    # Get the current time
    now = datetime.now()
    # Extract hours, minutes, and seconds
    return now.strftime("%H:%M:%S")

with open('output.json', 'r') as json_file:
    to_write = json.load(json_file)


Supera = stopc("306","Supera")
Biona = stopc("124","Biona")
EstBuses = stopc("131","Estacion de Autobuses")
EstRenfe = stopc("5","Estacion de Renfe")
Santamaria = stopc("125","Santamaria")


all_stops = [Supera,EstBuses,Santamaria,Biona,EstRenfe]

for stop in all_stops:
    if not stop.name in to_write:
        to_write[stop.name] = {}
        for route in stop.routes:
            to_write[stop.name][route] = []
save()

print(to_write)
while True:
    try:
        sleep(1)
        print("----------------------------------------------------------------------------------------")
        for stop in all_stops:
            print(stop.name)
            for line in stop.check():
                to_write[stop.name][line].append(get_time())
                save()
    except :
        pass
