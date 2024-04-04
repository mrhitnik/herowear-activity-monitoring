import serial
import csv
import datetime
import tkinter as tk
import threading
import numpy as np
from playsound import playsound
import time
from tkinter import PhotoImage

def analyze(data):
    data_mean = np.mean(data)
    data_var = np.var(data)
    data_std = np.std(data)
    load = 'Low'
    if data_mean > 1:
        load = 'Medium'
    if data_mean > 1.5:
        load = 'Heavy'
    variation = 'Consistent'
    if data_var > 1:
        variation = 'Varying'
    return load, variation, data_mean, data_var, data_std


def load_analysis(al, l, v):
    if l == 'Low':
        al += -10
    elif l == 'Medium':
        al += 5
    elif l == 'Heavy':
        al += 15
    if v == 'Consistent':
        al += -5
    else:
        al += 10
    return np.max([al, 0])


def update_gui_message(alert_level, l, v, data_mean, data_var, data_std):
    message = f'Alerting Level: {alert_level} ({l} {v} Load)\nMean: {data_mean:.2f}, Std Dev: {data_std:.2f}, Variance: {data_var:.2f}'
    alert_label.configure(bg='#D2D3AE')  # Set this for all widgets to match the window background
    alert_label.config(text=message)


def main_func():
    global serial_lock
    with serial_lock:
        if arduino.is_open:
            arduino_data = arduino.readline()
        else:
            return None
    decoded_value = str(arduino_data[0:len(arduino_data)].decode("utf-8")) if arduino_data else "0"
    current_time = str(datetime.datetime.now())
    time_values = current_time.split(' ')
    starting_date = time_values[0]
    HRS = time_values[1].split('.')[0].split(':')

    fileName = task + '_' + starting_date + '_' + HRS[0] + HRS[1] + HRS[2] + '.csv'

    header = ["Time", "Weight(lbs)"]

    try:
        open(fileName, 'r')
    except FileNotFoundError:
        with open(fileName, 'w', newline='') as file:
            filewriter = csv.writer(file, delimiter=',')
            filewriter.writerow(header)

    with open(fileName, 'a', newline='') as file:
        filewriter = csv.writer(file, delimiter=',')
        try:
            filewriter.writerow([time_values[1], float(decoded_value)])
        except ValueError:
            filewriter.writerow([time_values[1], decoded_value])

    value = float(decoded_value[:-2]) if decoded_value.strip() else 0
    if value > 100:
        value = 0.99
    return value


def read_and_process_data():
    global should_continue
    count = 1
    wait_period = 150
    window = 100
    alerting_tolerance = 150
    alerting_load = 0

    holder = []

    while should_continue:
        value = main_func()
        if value is None:  # If the serial connection was closed
            break
        holder.append(value)

        if (len(holder) >= wait_period) and (count % window == 0):
            holder_period = holder[-wait_period:]

            l, v, data_mean, data_var, data_std = analyze(holder_period)
            alerting_load = load_analysis(alerting_load, l, v)

            alerting_level = 'Low'
            if alerting_load > alerting_tolerance:
                alerting_level = 'High'
            elif alerting_load > (alerting_tolerance / 2):
                alerting_level = 'Medium'

            root.after(0, update_gui_message, alerting_level, l, v, data_mean, data_var, data_std)

            if alerting_load > alerting_tolerance:
                playsound('sounds/what.mp3')
                alerting_load -= 50

        count += 1


def exit_application():
    global should_continue, serial_lock
    should_continue = False  # Signal the thread to stop
    time.sleep(1)  # Allow a moment for the thread to exit its loop
    with serial_lock:
        if arduino.is_open:
            arduino.close()
    print("Exiting the application and cleaning up resources...")
    root.destroy()


# Initialize the Tkinter window
root = tk.Tk()
root.title("Herowear Load Cell Data Display")
# Set the window size
root.geometry("500x100")
# Sets the window background color
root.configure(bg='#D2D3AE')
# window icon
# root.iconbitmap('pictures/icon/FOM-Icon_LRG_Yellow-e1667321469885.ico')
# placing image
# image = PhotoImage(file='pictures/1602542323412.gif')
# image_label = tk.Label(root, image=image, bg='#D2D3AE')  # Ensure bg matches window if needed
# image_label.pack(side='right', fill='both', expand=True)
# inserting placeholder text
alert_label = tk.Label(root, text="Waiting for enough work to be done...", font=('Helvetica', 14))
alert_label.configure(bg='#D2D3AE')  # Set this for all widgets to match the window background
alert_label.pack()

# Initialize serial connection
arduino = serial.Serial('com6', 9600)  # Adjust COM port as necessary

# Flag to control the reading thread
should_continue = True

# Lock for serial access
serial_lock = threading.Lock()

task = './data/test'
starting_time = str(datetime.datetime.now()).split(' ')[1]

# exit button
exit_button = tk.Button(root, text="Exit", command=exit_application, font=('Helvetica', 11), width=4, height=1, bg='#404040', fg='#FFFFFF')
exit_button.pack(side=tk.BOTTOM, pady=10)

if __name__ == '__main__':
    thread = threading.Thread(target=read_and_process_data, daemon=True)
    thread.start()
    root.mainloop()
