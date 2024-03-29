import serial
import schedule
import csv
import datetime

arduino = serial.Serial('com3', 9600)

def main():
    print('2')
    arduino_data = 0
    arduino_data = arduino.readline()
    print('3')
    decoded_value = str(arduino_data[0:len(arduino_data)].decode("utf-8"))

    if isinstance(decoded_value, float):
        print(float(decoded_value) + 0.1)
        # return float(decoded_value) + 0.1
    else:
        print(float(decoded_value))
        # return decoded_value

# schedule.every(0.001).seconds.do(main)

# while True:
#     schedule.run_pending()
    # time.sleep(0.001)

if __name__ == '__main__':
    print("1")
    main()

