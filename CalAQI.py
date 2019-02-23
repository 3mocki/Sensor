# 1 hour
def no2Aqi(no2aver):
    if 0 <= no2aver <= 53:
        no2aqi = (((no2aver - 0) * (50 - 0)) / (53 - 0)) + 0
        return no2aqi
    elif 54 <= no2aver <= 100:
        no2aqi = (((no2aver - 54) * (100 - 51)) / (100 - 54)) + 51
        return no2aqi
    elif 101 <= no2aver <= 360:
        no2aqi = (((no2aver - 101) * (150 - 101)) / (360 - 101)) + 101
        return no2aqi
    elif 361 <= no2aver <= 649:
        no2aqi = (((no2aver - 361) * (200 - 151)) / (649 - 361)) + 151
        return no2aqi
    elif 650 <= no2aver <= 1249:
        no2aqi = (((no2aver - 650) * (300 - 201)) / (1249 - 650)) + 201
        return no2aqi
    elif 1250 <= no2aver <= 2049:
        no2aqi = (((no2aver - 1250) * (500 - 301)) / (1649 - 1250)) + 301
        return no2aqi
    else:
        return 500

# 1 hour
def o3Aqi_1(o3aver_1):
    if 0.125 <= o3aver_1 <= 0.164:
        o3aqi = (((o3aver_1-0.125) * (150-101)) / (0.164-0.125)) + 101
        return o3aqi
    elif 0.165 <= o3aver_1 <= 0.204:
        o3aqi = (((o3aver_1-0.165) * (200-151)) / (0.204-0.165)) + 151
        return o3aqi
    elif 0.205 <= o3aver_1 <= 0.404:
        o3aqi = (((o3aver_1-0.205) * (300-201)) / (404-205)) + 201
        return o3aqi
    elif 0.405 <= o3aver_1 <= 0.604:
        o3aqi = (((o3aver_1-0.405) * (300-201)) / (504-405)) + 301
        return o3aqi
    else:
        return 500

# 8 hour
def o3Aqi_8(o3aver_8):
    if 0 <= o3aver_8 <= 0.054:
        o3aqi = (((o3aver_8 - 0) * (50 - 0)) / (0.054 - 0)) + 0
        return o3aqi
    elif 0.055 <= o3aver_8 <= 0.070:
        o3aqi = (((o3aver_8 - 0.055) * (100 - 51)) / (0.070 - 0.055)) + 51
        return o3aqi
    elif 0.071 <= o3aver_8 <= 0.085:
        o3aqi = (((o3aver_8 - 0.071) * (150 - 101)) / (0.085 - 0.071)) + 101
        return o3aqi
    elif 0.086 <= o3aver_8 <= 0.105:
        o3aqi = (((o3aver_8 - 0.086) * (200 - 151)) / (0.105 - 0.086)) + 151
        return o3aqi
    elif 0.106 <= o3aver_8 <= 0.200:
        o3aqi = (((o3aver_8 - 0.106) * (300 - 201)) / (0.200 - 0.106)) + 201
        return o3aqi
    else:
        return 500

# 8 hour
def coAqi(coaver):
    if 0 <= coaver <= 4.4:
        co_aqi = (((coaver - 0) * (50 - 0)) / (4.4 - 0)) + 0
        return co_aqi
    elif 4.5 <= coaver <= 9.4:
        co_aqi = (((coaver - 4.5) * (100 - 51)) / (9.4 - 4.5)) + 51
        return co_aqi
    elif 9.5 <= coaver <= 12.4:
        co_aqi = (((coaver - 9.5) * (150 - 101)) / (12.4 - 9.5)) + 101
        return co_aqi
    elif 12.5 <= coaver <= 15.4:
        co_aqi = (((coaver - 12.5) * (200 - 151)) / (15.4 - 12.5)) + 151
        return co_aqi
    elif 15.5 <= coaver <= 30.4:
        co_aqi = (((coaver - 15.5) * (300 - 201)) / (30.4 - 15.5)) + 201
        return co_aqi
    elif 30.5 <= coaver <= 50.4:
        co_aqi = (((coaver - 30.5) * (500 - 301)) / (50.4 - 30.5)) + 301
        return co_aqi
    else:
        return 500

# 1 hour
def so2Aqi(so2aver):
    if 0 <= so2aver <= 35:
        so2aqi = (((so2aver - 0) * (50 - 0)) / (35 - 0)) + 0
        return so2aqi
    elif 36 <= so2aver <= 75:
        so2aqi = (((so2aver - 36) * (100 - 51)) / (75 - 36)) + 51
        return so2aqi
    elif 76 <= so2aver <= 185:
        so2aqi = (((so2aver - 76) * (150 - 101)) / (185 - 76)) + 101
        return so2aqi
    elif 186 <= so2aver <= 304:
        so2aqi = (((so2aver - 186) * (200 - 151)) / (304 - 186)) + 151
        return so2aqi
    elif 305 <= so2aver <= 604:
        so2aqi = (((so2aver - 305) * (300 - 201)) / (604 - 305)) + 201
        return so2aqi
    elif 605 <= so2aver <= 1004:
        so2aqi = (((so2aver - 605) * (500 - 301)) / (1004 - 605)) + 301
        return so2aqi
    else:
        return 501

# 24 hour
def pm25Aqi(pm25aver):
    if 0 <= pm25aver <= 12:
        pm25aqi = (((pm25aver - 0) * (50 - 0)) / (12 - 0)) + 0
        return pm25aqi
    elif 12.1 <= pm25aver <= 35.4:
        pm25aqi = (((pm25aver - 12.1) * (100 - 51)) / (35.4 - 12.1)) + 51
        return pm25aqi
    elif 35.5 <= pm25aver <= 55.4:
        pm25aqi = (((pm25aver - 35.5) * (150 - 101)) / (55.4 - 35.5)) + 101
        return pm25aqi
    elif 55.5 <= pm25aver <= 150.4:
        pm25aqi = (((pm25aver - 55.5) * (200 - 151)) / (150.4 - 55.5)) + 151
        return pm25aqi
    elif 150.5 <= pm25aver <= 250.4:
        pm25aqi = (((pm25aver - 150.5) * (300 - 201)) / (250.4 - 150.5)) + 201
        return pm25aqi
    elif 250.5 <= pm25aver <= 500.4:
        pm25aqi = (((pm25aver - 250.5) * (500 - 301)) / (500.4 - 250.5)) + 301
        return pm25aqi
    else:
        return 500

# 24 hour
def pm10Aqi(pm10aver):
    if 0 <= pm10aver <= 54:
        pm10aqi = (((pm10aver - 0) * (50 - 0)) / (54 - 0)) + 0
        return pm10aqi
    elif 55 <= pm10aver <= 154:
        pm10aqi = (((pm10aver - 55) * (100 - 51)) / (154 - 55)) + 51
        return pm10aqi
    elif 155 <= pm10aver <= 254:
        pm10aqi = (((pm10aver - 155) * (150 - 101)) / (254 - 155)) + 101
        return pm10aqi
    elif 255 <= pm10aver <= 354:
        pm10aqi = (((pm10aver - 255) * (200 - 151)) / (354 - 255)) + 151
        return pm10aqi
    elif 355 <= pm10aver <= 424:
        pm10aqi = (((pm10aver - 355) * (300 - 201)) / (424 - 355)) + 201
        return pm10aqi
    elif 425 <= pm10aver <= 604:
        pm10aqi = (((pm10aver - 425) * (500 - 301)) / (604 - 425)) + 301
        return pm10aqi
    else:
        return 500