import utime

def getGPSData(uart):
    # Parse NMEA data from GPS
    # Sample NMEA data GPRMC:b'$GPRMC,213742.00,A,3405.30835,N,11817.50804,W,1.766,,080923,,,A*6D\r\n' 
    # NMEA specifications from: https://www.sparkfun.com/datasheets/GPS/NMEA%20Reference%20Manual-Rev2.1-Dec07.pdf
    
    INDEX_TIME=1
    INDEX_DATA_VALID=2
    INDEX_LAT=3
    INDEX_LAT_HEMISPHERE=4
    INDEX_LONG=5
    INDEX_LONG_HEMISPHERE=6
    INDEX_GROUND_SPEED=7
    INDEX_GROUND_HEADING=8
    INDEX_GROUND_DATE=9
    INDEX_GROUND_HEADING=8
    
    
    data=str(uart.readline())
    utime.sleep_ms(2000)
    
    print("data",data)
    #check data
    if (len(data) >0):
        tokens=data.split(",")
        #check gps quality
        if (tokens[INDEX_DATA_VALID]=='A'):
            #UTC
            time=tokens[INDEX_TIME]
            #lattitude
            lat=tokens[INDEX_LAT]
            lat_hem=tokens[INDEX_LAT_HEMISPHERE]
            
            #longitude
            lon=tokens[INDEX_LONG]
            lon_hem=tokens[INDEX_LONG_HEMISPHERE]
            
            print("UTC: ", time)
            print("LAT: ", lat, " ", lat_hem)
            print("LON: ", lon, " ", lon_hem)
                       
