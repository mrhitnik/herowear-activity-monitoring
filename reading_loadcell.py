import serial
import csv
import datetime
from utils.analyze import analyze, load_analysis
import tkinter as tk


from playsound import playsound

# Initialize the Tkinter window
root = tk.Tk()
root.title("Load Cell Data Viewer")
# Set the window size
root.geometry("400x100")

alert_label = tk.Label(root, text="Waiting for Enough Work to be done...", font=('Helvetica', 14))
alert_label.pack()


arduino = serial.Serial('com6', 9600)  # use com6 if using my laptop, com3 for og laptop

task = './data/test'  # input("Enter task name: ")

mytime = str(datetime.datetime.now())
time_values = mytime.split(' ')
starting_date = time_values[0]
starting_time = time_values[1]

def update_gui_message(alert_level, l, v):
    message = f'Alerting Level: {alert_level} ({l} {v} Load)'
    alert_label.config(text=message)
    root.update()


def main_func():
    arduino_data = arduino.readline()
    # print(f'Arduino Data: {arduino_data}')
    decoded_value = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    # print(f'Decoded Value is weight?: {decoded_value}')

    time_WO_millisecs = starting_time.split('.')
    HRS = time_WO_millisecs[0].split(':')
    # print(f'HRS Time: {HRS} time: {time_WO_millisecs}')

    fileName = task + '_' + starting_date + '_' + HRS[0] + HRS[1] + HRS[2] + '.csv'

    header = ["Time", "Weight(lbs)"]

    try:
        open(fileName, 'r')
    except:
        file = open(fileName, 'w')
        filewriter = csv.writer(file, delimiter=',')
        filewriter.writerow([header[0], header[1]])
        file.close()

    mytime = str(datetime.datetime.now())
    time_values = mytime.split(' ')

    file = open(fileName, 'a', newline='')
    filewriter = csv.writer(file, delimiter=',')
    try:
        filewriter.writerow([time_values[1], float(decoded_value)])
    except:
        filewriter.writerow([time_values[1], decoded_value])

    file.close()

    value = float(decoded_value[:-2])
    arduino_data = 0
    # print(f'value: {value}')
    if value > 100:
        value = 0.99
    return value


if __name__ == '__main__':
    wait_period = 150
    window = 100
    alerting_tolerance = 150
    alerting_load = 0
    print('Waiting for Enough Work to be done...')

    holder = []
    x_axis = []
    count = 1

    while True:
        holder.append(main_func())
        x_axis.append(count)

        if (len(holder) >= wait_period) and (count % window == 0):
            holder_period = holder[-wait_period:]

            l, v = analyze(holder_period)
            alerting_load = load_analysis(alerting_load, l, v)

            alerting_level = 'Low'
            if alerting_load > alerting_tolerance:
                alerting_level = 'High'
            elif alerting_load > alerting_tolerance / 2:
                alerting_level = 'Medium'

            # print('Alerting Level: %s   (%s %s Load)' % (alerting_level, l, v))
            print(f'Alerting Level: {alerting_level} ({l} {v} Load)')
            update_gui_message(alerting_level, l, v)

            if alerting_load > alerting_tolerance:
                playsound('sounds/what.mp3')
                alerting_load += -50

            x = 0

        count += 1
