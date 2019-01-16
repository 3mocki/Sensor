import sqlite3
from CalAQI import *
from Sender import *

#for 24 hours DB
class MySqlite_24:
    calAqiPm25 = 0
    calAqiPm10 = 0

    avg_pm25 = 0
    avg_pm10 = 0

    past_pm25 = 0
    past_pm10 = 0

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
                            ' ( num INTEGER PRIMARY KEY, pm25 FLOAT, pm10 FLOAT, pm25aqi INT, pm10aqi INT)')

    def insertData(self, pm25, pm10, i, m):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (pm25, pm10, pm25aqi, pm10aqi) values(?, ?, ?, ?);',
                            (pm25, pm10, 0, 0))
        recent_pm25 = pm25
        recent_pm10 = pm10

        if i == 0:
            self.avg_pm25 = recent_pm25
            self.avg_pm10 = recent_pm10

            self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
            self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            air_sender[i][16] = int(pm25Aqi(self.avg_pm25))
            air_sender[i][17] = int(pm10Aqi(self.avg_pm10))

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set pm25aqi = ' + str(self.calAqiPm25) + ',pm10aqi = ' + str(self.calAqiPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName +');')

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

        elif 1 <= i < 86400:
            self.avg_pm25 = ((i+1)*self.avg_pm25 + recent_pm25 - self.past_pm25) / (i + 1)
            self.avg_pm10 = ((i+1)*self.avg_pm10 + recent_pm10 - self.past_pm10) / (i + 1)

            self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
            self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set pm25aqi = ' + str(self.calAqiPm25) + ',pm10aqi = ' + str(self.calAqiPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName +');')

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

        # based on a day
        elif i >= 86400:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM = (SELECT MIN(NUM) FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.avg_pm25 = ((i+1)*self.avg_pm25 + recent_pm25 - self.past_pm25) / (i + 1)
                    self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
                elif x == 1:
                    self.avg_pm10 = ((i+1)*self.avg_pm10 + recent_pm10 - self.past_pm10) / (i + 1)
                    self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                                ' set pm25aqi = ' + str(self.calAqiPm25) + ',pm10aqi = ' + str(self.calAqiPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName +');')
        if i % 10 == m:
            air_sender[m][16] = self.calAqiPm25
            air_sender[m][17] = self.calAqiPm10

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()
