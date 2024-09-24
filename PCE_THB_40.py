import time
import serial
import decimal

class PCE_THB_40:
    serial = None

    def __init__(self, fname):
        PCE_THB_40.serial = serial.Serial(
            port=fname,
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def test(self):
        ret = self.serial.readline(48)
        return ret

    def getValues(self):
        try:
            data = b''
            while data == b'':
                data = self.serial.readline(48)

            humidity_polarity = int(data[5:6].decode("utf-8"))
            humidity_decimal = int(data[6:7].decode("utf-8"))
            humidity_value = int(data[7:15].decode("utf-8"))
            humidity = humidity_value / (10**humidity_decimal)
            if(humidity_polarity == 1):
                humidity = -humidity
            temperature_polarity = int(data[21:22].decode("utf-8"))
            temperature_decimal = int(data[22:23].decode("utf-8"))
            temperature_value = int(data[23:31].decode("utf-8"))
            temperature = temperature_value / (10**temperature_decimal)
            if (temperature_polarity == 1):
                temperature = -temperature
            pressure_polarity = int(data[37:38].decode("utf-8"))
            pressure_decimal = int(data[38:39].decode("utf-8"))
            pressure_value = int(data[39:47].decode("utf-8"))
            pressure = pressure_value / (10**pressure_decimal)
            if (pressure_polarity == 1):
                pressure = -pressure

            return {
                'humidity': humidity,
                'temperature': temperature,
                'pressure': pressure
            }
        except:
            return {
                'humidity': 0,
                'temperature': 0,
                'pressure': 0
            }