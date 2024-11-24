from networktables import NetworkTables
import time
import tkinter as tk
from threading import Thread
import sys

root = tk.Tk()
root.title("Robot Info")
root.attributes("-fullscreen", True)
root.configure(background='black')

# Screen dimensions and grid cell size
SCREEN_WIDTH = root.winfo_screenwidth()
GRID_CELL_SIZE = SCREEN_WIDTH // 5
GRID_CELL_HEIGHT = GRID_CELL_SIZE

INFO_FONT = ("Arial", 50, "bold")
TITLE_FONT = ("Arial", 30)
GREEN_COLOR = "#00FF00"

def closeWindow():
    root.attributes("-fullscreen", False)
    time.sleep(2)
    root.destroy()

def create_title_label(parent, text, row, column):
    label = tk.Label(parent, text=text, font=TITLE_FONT, bg="#1C1C1C", fg=GREEN_COLOR)
    label.grid(row=row, column=column, columnspan=1, pady=10, sticky="n")
    return label

def create_circular_meter(parent, row, column, percent=0):
    canvas = tk.Canvas(parent, width=GRID_CELL_SIZE, height=GRID_CELL_HEIGHT, bg="#1C1C1C", highlightthickness=0)
    canvas.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    size = GRID_CELL_SIZE - 20
    canvas.create_oval(10, 10, size, size, outline="white", width=2)
    canvas.create_arc(10, 10, size, size, start=90, extent=-3.6 * percent, fill="#00FF00", outline="")
    return canvas

def create_horizontal_meter(parent, row, column, percent=0):
    frame = tk.Frame(parent, bg="#1C1C1C", width=GRID_CELL_SIZE, height=GRID_CELL_HEIGHT)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    frame.grid_propagate(False)

    percent_label = tk.Label(frame, text=f"{percent}%", font=INFO_FONT, bg="#1C1C1C", fg=GREEN_COLOR)
    percent_label.pack(pady=10)

    bar_width = GRID_CELL_SIZE - 40
    bar_height = 40
    canvas = tk.Canvas(frame, width=bar_width, height=bar_height, bg="#1C1C1C", highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, bar_width, bar_height, outline="white", width=2)
    canvas.create_rectangle(0, 0, percent * bar_width / 100, bar_height, fill="#00FF00", outline="")
    return frame, percent_label

motorTitle = create_title_label(root, "Motor Speed", row=0, column=0)
motorSpeedLabel = create_label(root, "", INFO_FONT, row=1, column=0)

statusTitle = create_title_label(root, "Robot Status", row=0, column=1)
robotStatusLabel = create_label(root, "Inactive", INFO_FONT, row=1, column=1)

circularMeter = create_circular_meter(root, row=2, column=0, percent=0)
horizontalMeter, percentLabel = create_horizontal_meter(root, row=2, column=1, percent=0)

button_frame = tk.Frame(root, bg="#1C1C1C")
button_frame.grid(row=0, column=4, padx=5, pady=5, sticky="ne")

close_button = tk.Button(button_frame, text="Close Window", command=closeWindow, font=TITLE_FONT, bg="#FF6347", fg="white")
close_button.pack(side="top", fill="x", padx=5, pady=5)

terminate_button = tk.Button(button_frame, text="Terminate Program", command=sys.exit, font=TITLE_FONT, bg="#DC143C", fg="white")
terminate_button.pack(side="top", fill="x", padx=5, pady=5)

# NetworkTables setup
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

# Update function
def value_changed(table, key, value, is_new):
    if key == "Motor Speed":
        abs_percent = abs(value) * 100  # Convert motor speed to absolute percentage
        motorSpeedLabel.config(text=f"Motor Speed: {value}")
        percentLabel.config(text=f"{int(abs_percent)}%")

        # Update circular meter
        circularMeter.delete("all")
        create_circular_meter(root, row=2, column=0, percent=int(abs_percent))

        # Update horizontal meter
        horizontalMeter.children["!canvas"].delete("all")
        create_horizontal_meter(root, row=2, column=1, percent=int(abs_percent))

    elif key == "Status":
        robotStatusLabel.config(text=f"Robot Status: {value}")

# Adding listener to update values
smartdashboard.addEntryListener(value_changed)

# GUI update function
def update_gui():
    root.after(100, update_gui)

def start_gui():
    root.after(100, update_gui)
    root.mainloop()

Thread(target=start_gui, daemon=True).start()

# Listening to NetworkTables in a separate thread
def networktables_thread():
    try:
        while True:
            if not NetworkTables.isConnected():
                print("Lost connection. Waiting to reconnect...")
                while not NetworkTables.isConnected():
                    time.sleep(1)
                print("Reconnected...")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")

Thread(target=networktables_thread, daemon=True).start()

start_gui()
