import sqlite3
from CalAQI import *
from Sender import *

# for a hour DB
class MySqlite_1:
    calAqiNo2 = 0
    calAqiO3 = 0
    calAqiSo2 = 0

    avg_no2 = 0
    avg_o3 = 0
    avg_so2 = 0

    past_no2 = 0
    past_o3 = 0
    past_so2 = 0

    # setting for db name
    def __init__(self, name):
        self.dbName = name + '.db'
        self.AirDataTableName = name + 'Air'

    # setting for db connection
    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def createTable(self):
        self.cursor.execute(' CREATE TABLE IF NOT EXISTS ' + self.AirDataTableName +
                            ' (num INTEGER PRIMARY KEY, ts INT, temp FLOAT, no2 FLOAT, o3 FLOAT, so2 FLOAT, no2aqi INT, o3aqi INT, so2aqi INT) ')

    def insertData(self, timestamp, temp, no2, o3, so2, i, m):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (ts, temp, no2, o3, so2, no2aqi, o3aqi, so2aqi) values(?, ?, ?, ?, ?, ?, ?, ?);',
                            (timestamp, temp, no2, o3, so2, 0, 0, 0))
        recent_no2 = no2
        recent_o3 = o3
        recent_so2 = so2

        if i == 0:
            self.avg_no2 = recent_no2
            self.avg_o3 = recent_o3
            self.avg_so2 = recent_so2

            self.calAqiNo2 = int(no2Aqi(self.avg_no2))
            self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
            self.calAqiSo2 = int(so2Aqi(self.avg_so2))

            air_sender[i][12] = self.calAqiNo2
            air_sender[i][13] = self.calAqiO3
            air_sender[i][15] = self.calAqiSo2

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calAqiNo2) + ',o3aqi =' + str(self.calAqiO3) + ',so2aqi =' + str(self.calAqiSo2) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

        elif 1 <= i < 3600:

            self.avg_no2 = ((i+1)*self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
            self.avg_o3 = ((i+1)*self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
            self.avg_so2 = ((i+1)*self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

            self.calAqiNo2 = int(no2Aqi(self.avg_no2))
            self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
            self.calAqiSo2 = int(so2Aqi(self.avg_so2))

            if i % 10 == m:
                air_sender[m][12] = self.calAqiNo2
                air_sender[m][13] = self.calAqiO3
                air_sender[m][15] = self.calAqiSo2

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calAqiNo2) + ',o3aqi =' + str(self.calAqiO3) + ',so2aqi =' + str(self.calAqiSo2) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

        # After 1 hour
        elif 3600 <= i < 28800:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM =(SELECT MIN(NUM) FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.avg_no2 = ((i+1)*self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
                    self.calAqiNo2 = int(no2Aqi(self.avg_no2))
                elif x == 1:
                    self.avg_s3 = ((i+1)*self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
                    self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
                elif x == 2:
                    self.avgSo2 = ((i+1)*self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)
                    self.calAqiSo2 = int(so2Aqi(self.avg_so2))
            if i % 10 == m:
                air_sender[m][12] = self.calAqiNo2
                air_sender[m][13] = self.calAqiO3
                air_sender[m][15] = self.calAqiSo2

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calAqiNo2) + ',o3aqi = ' + str(self.calAqiO3) + ',so2aqi = ' + str(self.calAqiSo2) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')


        elif i > 28800:
            self.cursor.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM =(SELECT MIN(NUM) FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 1):
                if x == 0:
                    self.avg_no2 = ((i+1)*self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
                    self.calAqiNo2 = int(no2Aqi(self.avg_no2))
                elif x == 1:
                    self.avg_so2 = ((i+1)*self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)
                    self.calAqiSo2 = int(so2Aqi(self.avg_so2))
            if i % 10 == m:
                air_sender[m][12] = self.calAqiNo2
                air_sender[m][15] = self.calAqiSo2

            self.past_no2 = recent_no2
            self.past_so2 = recent_so2

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calAqiNo2) + ',so2aqi = ' + str(self.calAqiSo2) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName +');')

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()

