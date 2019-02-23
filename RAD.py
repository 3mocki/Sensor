import requests, json, time, csv
from Msgtype import *
# from ResultCode import *
from globalVar import *
from Sender import *


class RAD_class:
    row = [[], [], [], 0, 0, 0, 0, 0, 0, 0]

    # msgHeader[0]
    msgtype = SSP_RADTRN

    # Collect per 1 sec
    payload = {
        "airQualityDataListEncodings": {
            "dataTupleLen": '10',
            "airQualityDataTuples": row
        }
    }

    # msgHeader[3:5]
    eId = ""

    def packedMsg(self):
        packedMsg = {
            "header": {
                "msgType": self.msgtype,
                "msgLen": len(str(self.payload)),
                "endpointId": self.eId
            },
            "payload": self.payload
        }
        return packedMsg

    def setTimer(self):
        global response
        print("Timer Working")
        response = requests.post(url_2, json=self.packedMsg())
        print('(check)State in Sensor : CID_ALLOCATED_STATE')
        # print('RAD-ACK => ', response.json())
        rt = response.elapsed.total_seconds()
        print('(check)rspTime :' + str(rt))
        return rt

    def rcvdMsg(self):
        if self.rt > 5:
            print("Retry Checking response time")
            self.setTimer()  # 3.2
        else:
            self.verifyMsgHeader()
            if rcvdPayload != RES_FAILED:
                print("(check)RES_FAILED")
                self.rt = 0
                return rcvdPayload
            else:
                self.rcvdMsg()

    def verifyMsgHeader(self):
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType']  # rcvdMsgType
        rcvdPayload = self.json_response['payload']
        # rcvdLength = len(str(self.rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId']  # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId:  # rcvdEndpointId = SSN
            stateCheck = 1
            if stateCheck == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return rcvdPayload
        else:
            return RES_FAILED

    def UnpackMsg(self):
        rcvdMsgPayload = self.json_response['payload']
        print(str(self.rcvdMsgPayload))

    def read_RAD(self):

        f = open('temp_RAD.csv', 'r')
        rad_data = csv.reader(f)

        for idx, line in enumerate(rad_data):
            air_sender[idx][0] = int(line[0])
            air_sender[idx][5] = float(line[5])
            air_sender[idx][6] = float(line[6])
            air_sender[idx][7] = float(line[7])
            air_sender[idx][8] = float(line[8])
            air_sender[idx][9] = float(line[9])
            air_sender[idx][10] = float(line[10])
            air_sender[idx][11] = float(line[11])
            air_sender[idx][12] = int(line[12])
            air_sender[idx][13] = int(line[13])
            air_sender[idx][14] = int(line[14])
            air_sender[idx][15] = int(line[15])
            air_sender[idx][16] = int(line[16])
            air_sender[idx][17] = int(line[17])

        f.close()

    def init(self):

        self.read_RAD()

        for x in range(0, 10):
            self.row[x] = air_sender[x]
            print('RAD_class self.row[' + str(x) + '] => ' + str(self.row[x]))

        print("(check)msgtype : " + str(self.msgtype))
        print("(check)eId(=cId) : " + str(self.eId))

        self.setTimer()

        t = response.json()
        print('(check)Received Msg : ' + str(t))  # check log

