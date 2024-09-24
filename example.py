import PCE_THB_40
import time

pce_thb_40 = PCE_THB_40.PCE_THB_40("COM4", 5)

while True:
    print(pce_thb_40.getValues())