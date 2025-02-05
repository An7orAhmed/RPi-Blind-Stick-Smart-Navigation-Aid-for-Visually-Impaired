import serial

lati, longi = 0.0, 0.0

# In the NMEA message, the position gets transmitted as:
# DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
# the minutes. However, I want to convert this format to the following:
# DD.MMMM. This method converts a transmitted string to the desired format
def formatDegreesMinutes(coordinates, digits):
    
    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes

# This method reads the data from the serial port, the neo7m dongle is attached to,
# and then parses the NMEA messages it transmits.
# neo7m is the serial port, that's used to communicate with the neo7m adapter
def getPositionData(neo7m):
    global lati, longi
    data = neo7m.readline()
    message = data[0:6]
    if (message == "$GPRMC"):
        # GPRMC = Recommended minimum specific neo7m/Transit data
        # Reading the neo7m fix data is an alternative approach that also works
        parts = data.split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print("neo7m receiver warning!")
        else:
            # Get the position data that was transmitted with the GPRMC message
            # In this example, I'm only interested in the longitude and latitude
            # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 2)
            lati = latitude
            longi = longitude
            #print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
            return [latitude, longitude]
    else:
        # Handle other NMEA messages and unsupported strings
        pass

print("neo7m started!")

SERIAL_PORT = "/dev/serial0"
neo7m = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)
running = True

def update():
    global running
    while running:
        try:
            getPositionData(neo7m)
        except KeyboardInterrupt:
            running = False
            neo7m.close()
            print("neo7m closed!")
        except:
            # You should do some error handling here...
            print("neo7m error!")

if __name__ == "__main__":
    update()