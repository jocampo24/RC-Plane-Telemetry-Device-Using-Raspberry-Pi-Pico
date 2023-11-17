"""
nRF24L01 receiver
Raspberry Pi Pico and nRF24L01 module.
If an integer is received, it is acknowledged by flipping its modulo.
For more info:
www.bekyelectronics.com/raspberry-pico-nrf25l01-micropython/
"""
import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const



# delay between receiving a message and waiting for the next message
POLL_DELAY = const(15)

# Pico pin definition:
myPins = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 15, "ce": 14}

# Addresses
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

csn = Pin(myPins["csn"], mode=Pin.OUT, value=1)
ce = Pin(myPins["ce"], mode=Pin.OUT, value=0)
nrf = NRF24L01(SPI(0, 10_000_000, sck=Pin(6), mosi=Pin(7), miso=Pin(4)), csn, ce, payload_size=16)

nrf.open_tx_pipe(pipes[1])
nrf.open_rx_pipe(1, pipes[0])
nrf.start_listening()

counter=0

print("nRF24L01 receiver; waiting for the first post...")

while True:
    for counter in range(0,126):
        
        nrf.stop_listening()
        utime.sleep_ms(20)
        
        nrf.set_channel(counter)
        utime.sleep_ms(20)
        
        nrf.start_listening()
        utime.sleep_ms(500)
        nrf.stop_listening()
        
        #if nrf.reg_read(0x09):
        print("channel: ", nrf.reg_read(0x05), " CD: ", nrf.reg_read(0x09))
        
        utime.sleep_ms(10)      
              
        
        
        
    
    
    
    
    
    
    
    
    if nrf.any(): # we received something
        
        
        while nrf.any():
            buf = nrf.recv()
            index = buf.find(b"\x00")
            if index >= 0:
                new_buf = buf[0:index].decode("utf-8")
            else:
                new_buf = buf.decode("utf-8")
            
            print(buff)
            counter = struct.unpack(str(nrf.payload_size)+'s', buf)

            utime.sleep_ms(POLL_DELAY) # delay before next listening
        
        
