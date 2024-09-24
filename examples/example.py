import PCE_THB_40

pce_thb_40 = PCE_THB_40.PCE_THB_40("COM4")

while True:
    print(pce_thb_40.getValues())