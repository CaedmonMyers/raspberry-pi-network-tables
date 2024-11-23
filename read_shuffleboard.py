# The commented code below works for connecting to the robot, but is not able to display any data.

from networktables import NetworkTables
import time
from threading import Thread

nt_ip = "10.12.9.2"

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)


NetworkTables.initialize(server=nt_ip)
print(f"Initializing Connection to {nt_ip}")

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)


while not NetworkTables.isConnected():
    print("Waiting for connection...")
    time.sleep(1)

print("Connected!")


# Diagnostics and Shuffleboard tables don't work yet. I got the SmartDaswhboard to work with this code
table = NetworkTables.getTable("Diagnostics")
smartdashboard = NetworkTables.getTable("SmartDashboard")
shuffleboard = NetworkTables.getTable("Shuffleboard")

def value_changed(table, key, value, is_new):
    print(f"Table: {table.getPath()}, Key: {key}, Value: {value}, Is new: {is_new}")

table.addEntryListener(value_changed)
smartdashboard.addEntryListener(value_changed)
shuffleboard.addEntryListener(value_changed)

def print_keys():
    while True:
        if NetworkTables.isConnected():
            pass
            #print(f"Smartdashboard keys: {smartdashboard.getKeys}")


Thread(target=print_keys, daemon=True).start()

try:
    print("Listening for updates. Ctrl+C to stop.")
    while True:
        if not NetworkTables.isConnected():
            print("Lost connection. Waiting to reconnect...")
            while not NetworkTables.isConnected():
                time.sleep(1)
            
            print("Reconnected...")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

'''
import threading
from networktables import NetworkTables


cond = threading.Condition()

notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

    with cond:
        notified[0] = True
        cond.notify()

nt_ip = "10.12.9.2"

NetworkTables.initialize(server=nt_ip)
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)


with cond:
    print("Waiting for connection")
    if not notified[0]:
        cond.wait()

print("Connected!")

table = NetworkTables.getTable("Diagnostics")

tableInfo1 = table.getDoubleTopic

def value_changed(table, key, value, is_new):
    print(f"Key: {key}, Value: {value}, Is new: {is_new}")

table.addEntryListener(value_changed, immediateNotify=True)

try:
    print("Listening for updates...")
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")'''

'''from networktables import NetworkTables as nt
import threading

def pushval(networkinstance, tablename:str, valuename, value):
    if networkinstance == None:
        logStuff([valuename] + value)
        return
    
    table = networkinstance.getTable(tablename)
    
    table.putNumberArray(valuename, value)

def networkConnect() -> any:
    cond = threading.Condition()
    notified = [False]

    def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        with cond:
            notified[0] = True
            cond.notify()
    
    nt.initialize(server=constants.SERVER)
    nt.addConnectionListener(connectionListener, immediateNotify=True)

    with cond:
        print("Waiting...")

        if not notified[0]:
            cond.wait()
    
    return nt

nt = networkConnect()

while True:
    pushval(nt, "Diagnostics", )'''