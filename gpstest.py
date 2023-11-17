from machine import Pin, I2C,SPI, ADC, UART
import utime
import MicropyGPS


myGPS=MicropyGPS.MicropyGPS()
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))



while True:
    
    print("getting data")
    data=str(uart1.readline())
    print(data)
    if len(data)>0:
        for x in data:
            myGPS.update(x)
        print('LAT: ',myGPS.latitude)
        print('LONG: ',myGPS.longitude)
        
                
    # Wait a second before sending the next message
    utime.sleep_ms(500)
    