import paho.mqtt.client as mqtt
import time
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print("Message: " + message.payload.decode())
    msg = "open"
    query = "select * from " + tablename + " where `state`= \"%s\";" % message.payload.decode()
    cursor = connection.cursor()
    cursor.execute(query)

    t = datetime.now()
    h = t.hour

    if message.payload.decode() == "NORI":
        h -= 1
        if h < 0:
            h = 23

    if h >= 10 and h < 18:
        state = "open"
    else:
        state = "close"
        

    for row in cursor:
        client.publish("Observatories/" + message.payload.decode(), row["location"] + " - " + state)
 
connection = pymysql.connect(
    host='localhost',
    user='root',
    db='Observatories',
    cursorclass=DictCursor
)

Connected = False   #global variable for the state of the connection
 
tablename = "obs"
broker_address= "192.168.1.8"
port = 1883
user = "yourUser"
password = ""
 
client = mqtt.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
client.subscribe("ObservatoryOf/")
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
try:
    while True:
        a = 1
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()