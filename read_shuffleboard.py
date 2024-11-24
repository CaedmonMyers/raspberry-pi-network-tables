from networktables import NetworkTables
import time
import tkinter as tk
from threading import Thread
import sys

root = tk.Tk()
root.title("Robot Info")
root.attributes("-fullscreen", True)
root.configure(background='black')

# Screen dimensions for grid layout
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
GRID_CELL_SIZE = SCREEN_WIDTH // 5

INFO_FONT = ("Arial", 50, "bold")
TITLE_FONT = ("Arial", 20)

def closeWindow():
    #NetworkTables.stopClient()
    root.attributes("-fullscreen", False)
    #time.sleep(2)
    #root.destroy()


def create_label(parent, text, font, row, column):
    label = tk.Label(parent, text=text, font=font, bg="#1C1C1C", fg="white")
    label.grid(row=row, column=column, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
    return label


def create_circular_meter(parent, row, column, percent=0):
    canvas = tk.Canvas(parent, width=GRID_CELL_SIZE, height=GRID_CELL_SIZE, bg="#1C1C1C", highlightthickness=0)
    canvas.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
    size = GRID_CELL_SIZE - 20
    canvas.create_oval(10, 10, size, size, outline="white", width=2)
    canvas.create_arc(10, 10, size, size, start=90, extent=-3.6 * percent, fill="#00FF00", outline="")
    canvas.create_text(size // 2, size // 2, text=f"{percent}%", font=INFO_FONT, fill="white")
    return canvas


def create_horizontal_meter(parent, row, column, percent=0):
    frame = tk.Frame(parent, bg="#1C1C1C")
    frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
    width = GRID_CELL_SIZE - 40
    height = 40
    canvas = tk.Canvas(frame, width=width, height=height, bg="#1C1C1C", highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, width, height, outline="white", width=2)
    canvas.create_rectangle(0, 0, percent * width / 100, height, fill="#00FF00", outline="")
    canvas.create_text(width // 2, height // 2, text=f"{percent}%", font=TITLE_FONT, fill="white")
    return frame


motorSpeedLabel = create_label(root, "Motor Speed: 0", INFO_FONT, row=0, column=0)
robotStatusLabel = create_label(root, "Robot Status: Inactive", INFO_FONT, row=0, column=1)

circularMeter = create_circular_meter(root, row=1, column=0, percent=0)
horizontalMeter = create_horizontal_meter(root, row=1, column=1, percent=0)

button_frame = tk.Frame(root, bg="#1C1C1C")
button_frame.grid(row=0, column=4, padx=5, pady=5, sticky="ne")

close_button = tk.Button(button_frame, text="Close Window", command=closeWindow, font=TITLE_FONT, bg="#FF6347", fg="white")
close_button.pack(side="top", fill="x", padx=5, pady=5)

terminate_button = tk.Button(button_frame, text="Terminate Program", command=sys.exit, font=TITLE_FONT, bg="#DC143C", fg="white")
terminate_button.pack(side="top", fill="x", padx=5, pady=5)


def update_gui():
    root.after(100, update_gui)


def start_gui():
    root.after(100, update_gui)
    root.mainloop()


#Thread(target=start_gui, daemon=True).start()
start_gui()
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
        motorSpeedLabel.config(text=f"Motor Speed: {value}")
        circularMeter.children["!canvas"].delete("all")
        create_circular_meter(root, row=1, column=0, percent=int(value))
        horizontalMeter.children["!canvas"].delete("all")
        create_horizontal_meter(root, row=1, column=1, percent=int(value))

    elif key == "Status":
        robotStatusLabel.config(text=f"Robot Status: {value}")


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
