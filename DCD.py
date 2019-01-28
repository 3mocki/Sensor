import requests, json
from Msgtype import *
from ResultCode import *
from globalVar import *

class DCD_class:

    msgtype = SSP_DCDNOT
    payload = None
    # eId is Connection ID
    eId = ""

    def packedMsg(self):
        packedMsg = {
            "header": {
                "msgType" : self.msgtype,
                "msgLen" : self.payload,
                "endpointId" : self.eId
            }
        }
        return packedMsg

    def setTimer(self):
        global response, rt
        print("Timer Working")
        response = requests.post(url_1, json=self.packedMsg())  # 2.2 fnSendMsg => json
        rt = response.elapsed.total_seconds()
        print('(check)rspTime :' + str(rt))
        return rt

    # 3.1 fnRecvMsg()
    def rcvdMsg(self):
        if rt > 5:
            print("Retry Checking response time")
            self.setTimer()  # 3.2
        else:
            self.verifyMsgHeader()
            if rcvdPayload != RES_FAILED:
                print("check")
                return rcvdPayload
            else:
                self.rcvdMsg()

    def verifyMsgHeader(self): # 3.3.1
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType'] # rcvdMsgType
        rcvdPayload = self.json_response['payload']
        # rcvdLength = len(str(rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId'] # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId: # rcvdEndpointId = fnGetTemporarySensorId
            stateCheck = 1
            if stateCheck == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return rcvdPayload
        else:
            return RES_FAILED

    def UnpackMsg(self):
        if self.json_response['payload']['resultCode'] == RESCODE_SSP_SIR_OK: # 4.1
            rc = self.json_response['payload']['resultCode']
            print("(check)Result Code: "+ str(rc))
            return rc

    def init(self):
        print('check msgType : ' + str(self.msgtype))
        print("check payload : " + str(self.payload))

        self.setTimer()

        t = response.json()
        print('(check)Received Msg : ' + str(t))  # check log
        data = response.text
        self.json_response = json.loads(data)

        self.rcvdMsg()
        self.UnpackMsg()