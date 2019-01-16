from SIR import SIR_class
from DCA import DCA_class
from RAD import RAD_class
import time

if __name__ == '__main__':

    try:
        print("-----------Generate SIR-----------")
        sir = SIR_class()
        sir.init()

        print("-----------Generate DCA-----------")
        dca = DCA_class()
        dca.eId = sir.ssn
        dca.init()

        while True:
            print("-----------Generate RAD-----------")
            rad = RAD_class()
            rad.eId = dca.cId

            print("----------------------------------")
            print(int(time.time()))
            rad.init()
            time.sleep(10)


    except KeyboardInterrupt:
        # [Ctrl + C] or [Ctrl + Z]
        print("-----Quit Measuring-----")