# import libraries
from imu import MPU6050
from time import sleep
from time import ticks_ms
from machine import Pin, I2C,SPI, ADC, UART
import bme280 #BME280 altitude
import ustruct as struct
import utime
from nrf24l01 import NRF24L01 #wireless radio
import uos # for sd card -- added by Jose on 06/05/2023
import sdcard # for sd card -- added by Jose on 06/05/2023
import MicropyGPS

# I2C hardware setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)


bme = bme280.BME280(i2c=i2c)          #BME280 object created

# pin definition for SD card:
myPins = myPins = {"spi": 0, "miso": 7, "mosi": 4, "sck": 6, "csn": 15, "ce": 14}

# sd card chip select
sd_cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
sd_spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(12))

# Initialize SD card
sd = sdcard.SDCard(sd_spi, sd_cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Wireless Transmitter/Receiver Addresses (little endian)
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

csn = Pin(myPins["csn"], mode=Pin.OUT, value=1)
ce = Pin(myPins["ce"], mode=Pin.OUT, value=0)
# nrf = NRF24L01(SPI(0, 10_000_000, sck=Pin(6), mosi=Pin(7), miso=Pin(4)), csn, ce, payload_size=16)
# 
# nrf.open_tx_pipe(pipes[0])
# nrf.open_rx_pipe(1, pipes[1])
# nrf.start_listening()
# nrf.stop_listening()

# current sensor
# Configure ADC
adc = ADC(Pin(27))

# Set calibration value (adjust as per your sensor)
calibration_value = 51100

# GPS
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
myGPS=MicropyGPS.MicropyGPS()
measurements=[]

while True:

    #imu
    ax=round(imu.accel.x,2)
    measurements.append(["ax:", ax])
       
    ay=round(imu.accel.y,2)
    measurements.append(["ay:", ay])
    
    az=round(imu.accel.z,2)
    measurements.append(["az:", az])
    
    tem=round(imu.temperature,2)
    measurements.append(["Temp(C):", tem])
    
    #bmu
    press=bme.values
    measurements.append(["Pressure:", press])
     
    #GPS
    data=str(uart1.readline())
    if len(data)>0:
        for x in data:
            myGPS.update(x)
        
        measurements.append(["Lat:", myGPS.latitude_string()])
        measurements.append(["Lon:", myGPS.longitude_string()])
        measurements.append(["Speed:", myGPS.speed_string()])
        measurements.append(["Date:", myGPS.date_string('s_mdy')])
        measurements.append(["Time:", myGPS.timestamp])
        
        
    # Current sensor
    # Read raw ADC value
    raw_value = adc.read_u16()

    # Convert raw value to current (in milliamperes)
    current = ((raw_value - calibration_value) / 2**16)*3.3/0.4
    measurements.append(["Current:", current])

    
    #read battery voltage
    
    
    # Send Start indicator
    print("START")
    start=ticks_ms()
    
    for measurement in measurements:
        
        measurement_desc=str(measurement[0])+str(measurement[1])
        print(measurement_desc)
        len_str=str(len(measurement_desc))+'s'
    
#         try:
#             nrf.send(struct.pack(len_str, measurement_desc)) # sending the message
#             utime.sleep_ms(15)
#         except OSError:
#             pass
    
    # Send Start indicator
    print("END")
    
    
    #write data to SD card
    with open("/sd/test01.txt", "a") as file:
        for measurement in measurements:
            file.write(str(measurement[0])+str(measurement[1])) 
            file.write("\r\n")
    
    
    #clear the current measurements list
    measurements=[]        
   
    # Wait before sending the next message
    utime.sleep_ms(100) 
