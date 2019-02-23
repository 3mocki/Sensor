import serial, os, time, csv
from Database import *
from Database2 import *
from Database3 import *
from Sender import *

# air list; ppm is O3 and CO // ppb is NO2, SO2
air_list = ['no2', 'o3', 'co', 'so2', 'pm25', 'pm10']

# timestamp, temp, no2, o3, co, so2, pm25, pm10, i, m
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# calibration data of 25-000160 Indoor Sensor
we_zero = [295, 391, 347, 345]
ae_zero = [282, 390, 296, 255]
sens = [0.195, 0.399, 0.276, 0.318]

# temp_n is going to no2, o3, co, so2 in 2 X 2 list
temp_n = [[1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00, 2.70],
          [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 2.87],
          [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48, -0.80],
          [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 1.95]]

# path of gpio control files
port = '/dev/tty96B0'
ard = serial.Serial(port, 9600)
gpio_path = '/sys/class/gpio/'

path_dir_gpio36 = gpio_path + 'gpio36/direction'
path_dir_gpio13 = gpio_path + 'gpio13/direction'
path_dir_gpio12 = gpio_path + 'gpio12/direction'
path_dir_gpio69 = gpio_path + 'gpio69/direction'
path_dir = [path_dir_gpio36, path_dir_gpio13, path_dir_gpio12, path_dir_gpio69]

path_val_gpio36 = gpio_path + 'gpio36/value'
path_val_gpio13 = gpio_path + 'gpio13/value'
path_val_gpio12 = gpio_path + 'gpio12/value'
path_val_gpio69 = gpio_path + 'gpio69/value'
path_val = [path_val_gpio36, path_val_gpio13, path_val_gpio12, path_val_gpio69]

numberOfData = 0
csvRowCount = 0


# set the gpio pins to OUTPUT mode
def init_direction():
    for i in range(4):
        with open(path_dir[i], 'w') as f:
            f.write("out")


# set the gpio pins the value to '0'
def init_gpio():
    for i in range(4):
        with open(path_val[i], 'w') as f:
            f.write('0')


# gpio controlling function
def gpio_control(num):
    init_gpio()
    if num % 2 == 1:
        with open(path_val[0], 'w') as f:
            f.write('1')
    if num % 4 > 1:
        with open(path_val[1], 'w') as f:
            f.write('1')
    if num % 8 > 3:
        with open(path_val[2], 'w') as f:
            f.write('1')
    if num % 16 > 7:
        with open(path_val[3], 'w') as f:
            f.write('1')


# get the voltage value
# Digital Value(ADC Value) will convert to mV
def adc_converter(value):
    adc = int(value)
    mV = float(adc / 1023) * 5000 # to get millivolt
    return mV


def temp_choice(tmp, x):
    if -30 <= tmp:
        return temp_n[x - 1][0]
    elif -30 <= tmp < -20:
        return temp_n[x - 1][1]
    elif -20 <= tmp < -10:
        return temp_n[x - 1][2]
    elif -10 <= tmp < 0:
        return temp_n[x - 1][3]
    elif 0 <= tmp < 10:
        return temp_n[x - 1][4]
    elif 10 <= tmp < 20:
        return temp_n[x - 1][5]
    elif 20 <= tmp < 30:
        return temp_n[x - 1][6]
    elif 30 <= tmp < 40:
        return temp_n[x - 1][7]
    elif 40 <= tmp <= 50:
        return temp_n[x - 1][8]


def write_rad(csvRowCount, numberOfData):
    if csvRowCount == 10:
        f = open('temp_RAD.csv', 'w', newline='')
        f.truncate()
        wr = csv.writer(f)

        for i in air_sender:
            wr.writerow(i)
        f.close()
        print("CSV CLEAR!!!")
        numberOfData += 1
        csvRowCount = 0
        return csvRowCount, numberOfData
    else:
        numberOfData += 1
        csvRowCount += 1
        return csvRowCount, numberOfData


def collect_Data():
    # collecting air data
    for x in range(0, 6):
        init_direction()
        init_gpio()
        print('*******************************')
        data[0] = int(time.time())
        if x == 0:
            # measuring temperature
            gpio_control(x)
            ardOut = ard.readline()
            temp_low = ardOut.rstrip(b'\n')
            temp_value = adc_converter(temp_low)
            temp_result = (float(temp_value) - 500) * 0.1 # 500 is offset & 0.1 is Output Voltage Scailing
            if temp_result <= -30:
                temp_result = -30
            elif temp_result > 50:
                temp_result = 50
            print('Temperature : ' + str(round(temp_result, 3)) + 'degree celcius')
            # choice temperature each sensor
            data[1] = round(temp_result, 2)

        elif 1 <= x <= 4:
            # Measuring Working Electrode
            gpio_control(x * 2 - 1)
            ardOut = ard.readline()
            we_low = ardOut.rstrip(b'\n')
            we_value = adc_converter(we_low)
            print(air_list[x - 1] + ' WE : ' + str(round(we_value, 3)) + 'mV')

            # Measuring Auxiliary Electrode
            gpio_control(x * 2)
            ardOut = ard.readline()
            ae_low = ardOut.rstrip(b'\n')
            ae_value = adc_converter(ae_low)
            print(air_list[x - 1] + ' AE : ' + str(round(ae_value, 3)) + 'mV')

            if x == 1:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                no2 = round(ppb_value, 3)
                data[2] = no2
                print(air_list[x - 1] + ' : ' + str(no2) + 'ppb')

            elif x == 2:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                o3 = round(ppb_value / 1000, 3)
                data[3] = o3
                print(air_list[x - 1] + ' : ' + str(o3) + 'ppm')

            elif x == 3:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                co = round(ppb_value / 1000, 3)
                data[4] = co
                print(air_list[x - 1] + ' : ' + str(co) + 'ppm')

            elif x == 4:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                so2 = round(ppb_value, 3)
                data[5] = so2
                print(air_list[x - 1] + ' : ' + str(so2) + 'ppb')

            print('n Table :' + str(temp))

        elif x == 5:
            gpio_control(x * 2 - 1)
            ardOut = ard.readline()
            pm25_low = ardOut.rstrip(b'\n')
            pm25_value = adc_converter(pm25_low)
            v = pm25_value / 1000
            hppcf = 240 * (v ** 6) - 2491.3 * (v ** 5) + 9448.7 * (v ** 4) - 14840 * (v ** 3) + 10684 * (
                    v ** 2) + 2211.8 * v + 7.9623
            ugm3 = .518 + .00274 * hppcf
            pm25 = round(ugm3, 3)
            data[6] = pm25
            pm10 = round(ugm3, 3)
            data[7] = pm10
            print(air_list[x - 1] + ' : ' + str(pm25) + 'ug/m^3')
            print(air_list[x] + ' : ' + str(pm10) + 'ug/m^3')
            print('*******************************')


def save_to_DS(r, z):
    if r % 10 == z:
        air_sender[z][0] = data[0]  # timestamp=
        air_sender[z][5] = data[1]  # temp
        air_sender[z][6] = data[2]  # no2
        air_sender[z][7] = data[3]  # o3
        air_sender[z][8] = data[4]  # co
        air_sender[z][9] = data[5]  # so2
        air_sender[z][10] = data[6]  # pm10
        air_sender[z][11] = data[7]  # pm25


if __name__ == '__main__':
    print("=========Operating Sensor=========")

    # delete past air db file
    os.system("sudo rm -r hour1.db hour8.db hour24.db")

    # create each db file
    db = MySqlite_1('hour1')
    db2 = MySqlite_8('hour8')
    db3 = MySqlite_24('hour24')

    db.connectDB()
    db2.connectDB()
    db3.connectDB()

    db.createTable()
    db2.createTable()
    db3.createTable()

    try:
        while True:
            data[8] = numberOfData
            data[9] = csvRowCount

            print('Data Number:' + str(data[8]))
            print('CSVR Number:' + str(data[9]))

            collect_Data()
            save_to_DS(numberOfData, csvRowCount)

            db.insertData(data[0], data[1], data[2], data[3], data[5], data[8],
                          data[9])  # timestamp, temp, no2, o3, so2
            db2.insertData(data[3], data[4], data[8], data[9])  # o3, co
            db3.insertData(data[6], data[7], data[8], data[9])  # pm10, pm25

            db.commitDB()
            db2.commitDB()
            db3.commitDB()

            csvRowCount, numberOfData = write_rad(csvRowCount, numberOfData)

            print('Data Number:' + str(data[8]))
            print('CSVR Number:' + str(data[9]))

    except KeyboardInterrupt:
        db.closeDB()
        db2.closeDB()
        db3.closeDB()

        print("Exit")