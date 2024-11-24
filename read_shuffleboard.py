from networktables import NetworkTables
import time
import tkinter as tk
from threading import Thread

root = tk.Tk()
root.title("Robot Info")
root.attributes("-fullscreen", True)
root.configure(background='black')

INFO_FONT = ("Arial", 50, "bold")
TITLE_FONT = ("Arial", 20)

motorSpeedLabel = tk.Label(root, text="0", font=INFO_FONT)
motorSpeedLabel.grid(row=0, column=0, padx=10, pady=10, sticky="n")
motorSpeedLabel.configure(background='#1C1C1C', foreground='white')

robotStatusLabel = tk.Label(root, text="Inactive", font=INFO_FONT)
robotStatusLabel.grid(row=0, column=1, padx=10, pady=10, sticky="n")
robotStatusLabel.configure(background='#1C1C1C', foreground='white')


def create_circular_meter(parent, row, column, percent=0, size=200):
    canvas = tk.Canvas(parent, width=size, height=size, bg="black", highlightthickness=0)
    canvas.grid(row=row, column=column, padx=10, pady=10, sticky="n")
    canvas.create_oval(10, 10, size-10, size-10, outline="white", width=2)
    canvas.create_arc(10, 10, size-10, size-10, start=90, extent=-3.6 * percent, fill="green", outline="")
    canvas.create_text(size//2, size//2, text=f"{percent}%", font=INFO_FONT, fill="white")
    return canvas


def create_horizontal_meter(parent, row, column, percent=0, width=300, height=30):
    frame = tk.Frame(parent, bg="black")
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="n")
    canvas = tk.Canvas(frame, width=width, height=height, bg="black", highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, width, height, outline="white", width=2)
    canvas.create_rectangle(0, 0, percent * width / 100, height, fill="green", outline="")
    canvas.create_text(width//2, height//2, text=f"{percent}%", font=TITLE_FONT, fill="white")
    return frame


circularMeter = create_circular_meter(root, row=1, column=0, percent=0)
horizontalMeter = create_horizontal_meter(root, row=1, column=1, percent=0)


def update_gui():
    root.after(100, update_gui)


def start_gui():
    root.after(100, update_gui)
    root.mainloop()


Thread(target=start_gui, daemon=True).start()

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


def value_changed(table, key, value, is_new):
    if key == "Motor Speed":
        motorSpeedLabel.config(text=f"{value}")
        circularMeter.children["!canvas"].delete("all")
        create_circular_meter(root, row=1, column=0, percent=int(value))
        horizontalMeter.children["!canvas"].delete("all")
        create_horizontal_meter(root, row=1, column=1, percent=int(value))

    elif key == "Status":
        robotStatusLabel.config(text=f"{value}")


smartdashboard.addEntryListener(value_changed)


def print_keys():
    while True:
        if NetworkTables.isConnected():
            pass


def networktables_thread():
    try:
        while True:
            if not NetworkTables.isConnected():
                while not NetworkTables.isConnected():
                    time.sleep(1)

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass


Thread(target=print_keys, daemon=True).start()

Thread(target=networktables_thread, daemon=True)
