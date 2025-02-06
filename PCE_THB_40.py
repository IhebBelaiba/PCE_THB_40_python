import time
import serial

def getUnit(unit):
    if unit == 1:
        return "°C"
    elif unit == 2:
        return "°F"
    elif unit == 4:
        return "%RH"
    elif unit == 91:
        return "hPa"
    elif unit == 80:
        return "inch Hg"
    elif unit == 78:
        return "mm Hg"
    else:
        return "Invalid"

class PCE_THB_40:
    serial = None

    def __init__(self, fname):
        PCE_THB_40.serial = serial.Serial(
            port=fname,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    def test(self):
        ret = self.serial.readline(48)
        return ret

    def getValues(self):
        data = b''
        try:
            while data == b'':
                data = self.serial.readline(48)
                if(data != b'') and ((data[0:1] != b'\x02') or (data[16:17] != b'\x02') or (data[32:33] != b'\x02')):
                    print("re-syncing sensor")
                    data = b''
                    time.sleep(1)

            humidity_unit = int(data[3:5].decode("utf-8"))
            humidity_polarity = int(data[5:6].decode("utf-8"))
            humidity_decimal = int(data[6:7].decode("utf-8"))
            humidity_value = int(data[7:15].decode("utf-8"))
            humidity = (humidity_value / (10**humidity_decimal))*((-1)**humidity_polarity)

            temperature_unit = int(data[19:21].decode("utf-8"))
            temperature_polarity = int(data[21:22].decode("utf-8"))
            temperature_decimal = int(data[22:23].decode("utf-8"))
            temperature_value = int(data[23:31].decode("utf-8"))
            temperature = (temperature_value / (10**temperature_decimal))*((-1)**temperature_polarity)

            pressure_unit = int(data[35:37].decode("utf-8"))
            pressure_polarity = int(data[37:38].decode("utf-8"))
            pressure_decimal = int(data[38:39].decode("utf-8"))
            pressure_value = int(data[39:47].decode("utf-8"))
            pressure = (pressure_value / (10**pressure_decimal))*((-1)**pressure_polarity)

            return {
                'humidity': humidity,
                'humidity_unit': humidity_unit,
                'humidity_unit_txt': getUnit(humidity_unit),
                'temperature': temperature,
                'temperature_unit': temperature_unit,
                'temperature_unit_txt': getUnit(temperature_unit),
                'pressure': pressure,
                'pressure_unit': pressure_unit,
                'pressure_unit_txt': getUnit(pressure_unit),
            }
        except:
            print("error:", data)
            return {
                'humidity': 0,
                'humidity_unit': 0,
                'humidity_unit_txt': "",
                'temperature': 0,
                'temperature_unit': 0,
                'temperature_unit_txt': "",
                'pressure': 0,
                'pressure_unit': 0,
                'pressure_unit_txt': "",
            }
