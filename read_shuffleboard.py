# The commented code below works for connecting to the robot, but is not able to display any data.

from networktables import NetworkTables
import time
import tkinter as tk
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


smartdashboard = NetworkTables.getTable("SmartDashboard")

motorSpeed = 0.0
robotStatus = ""

root = tk.Tk()
root.title("Robot Info")

motorSpeedLabel = tk.Label(root, text="Motor Speed: 0", font=("Arial", 50))
motorSpeedLabel.pack(pady=10)

robotStatusLabel = tk.Label(root, text="Robot Status: 0", font=("Arial", 50))
robotStatusLabel.pack(pady=10)


def value_changed(table, key, value, is_new):
    print(f"Table: {table.getPath()}, Key: {key}, Value: {value}, Is new: {is_new}")
    if key == "Status":
        #robotStatus = value
        robotStatusLabel.config(text=f"Robot Status: {value}")
    
    elif key == "Motor Speed":
        #motorSpeed = value
        motorSpeedLabel.config(text=f"Motor Speed: {value}")


def update_gui():
    pass
    #motorSpeedLabel.config(text=f"Motor Speed: {motorSpeed}")
    #robotStatusLabel.config(text=f"Robot Status: {robotStatus}")

    root.after(100, update_gui)

def start_gui():
    root.after(100, update_gui)
    root.mainloop()

Thread(target=start_gui, daemon=True).start()

smartdashboard.addEntryListener(value_changed)

def print_keys():
    while True:
        if NetworkTables.isConnected():
            pass
            #print(f"Smartdashboard keys: {smartdashboard.getKeys}")


def networktables_thread():
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


Thread(target=print_keys, daemon=True).start()

Thread(target=networktables_thread, daemon=True)


start_gui()




# Bunch of old code and stuff
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