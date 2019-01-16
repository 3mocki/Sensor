import sqlite3
from CalAQI import *
from Sender import *


# for 8 hours DB
class MySqlite_8:
    calAqiO3 = 0
    calAqiCo = 0

    avg_co = 0
    avg_o3 = 0

    past_co = 0
    past_o3 = 0

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
                            ' ( num INTEGER PRIMARY KEY, o3 FLOAT, co FLOAT, o3aqi INT, co_aqi INT)')

    def insertData(self, o3, co, i, m):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (o3, co, o3aqi, co_aqi) values(?, ?, ?, ?);',
                            (o3, co, 0, 0))
        recent_o3 = o3
        recent_co = co

        if i == 0:
            self.avg_co = recent_co
            self.calAqiCo = int(coAqi(self.avg_co))
            air_sender[i][14] = self.calAqiCo

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                                ' set co_aqi = ' + str(
                self.calAqiCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

            self.past_co = recent_co

        # before 8 hours
        elif 1 <= i < 28800:
            self.avg_co = ((i + 1) * self.avg_co + recent_co - self.past_co) / (i + 1)
            self.calAqiCo = int(coAqi(self.avg_co))

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                                ' set co_aqi = ' + str(
                self.calAqiCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')
            if i % 10 == m:
                air_sender[m][14] = self.calAqiCo

            self.past_co = recent_co

        # after 8 hours
        elif i >= 28800:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM = (SELECT MIN(NUM) FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.avg_o3 = ((i + 1) * self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
                    self.calAqiO3 = int(o3Aqi_8(self.avg_o3))
                elif x == 1:
                    self.avg_co = ((i + 1) * self.avg_co + recent_co - self.past_co) / (i + 1)
                    self.calAqiCo = int(coAqi(self.avg_co))

            if i % 10 == m:
                air_sender[m][13] = self.calAqiO3
                air_sender[m][14] = self.calAqiCo

            self.past_o3 = recent_o3
            self.past_co = recent_co

            # calAqiData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                                ' set o3aqi = ' + str(self.calAqiO3) + ',co_aqi = ' + str(
                self.calAqiCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()