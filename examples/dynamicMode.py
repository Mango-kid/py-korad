from korad import kel103

# setup the device
# 1st param: the IP of your ethernet/wifi interface
# 2nd param: the IP of the Korad device
# 3rd param: the port of the Korad device (18190 = default)
kel = kel103.kel103("192.168.2.28", "192.168.7.183", 18190)

print("Connecting to device..")
try:
    kel.checkDevice()
except:
    print("Connection timeout, could not connect to device")
    exit(1)

# changing mode (uncomment either CC or CV mode)
print("Changing mode to dynamic..")
kel.setDynamicModeCC(slope1=1.5, slope2=1.2, current1=0.0, current2=1.1, freq=5, dutycycle=10)
#kel.setDynamicModeCV(voltage1=1.5, voltage2=2.5, freq=1, dutycycle=10)

# read to see if mode has changed
dynamic = kel.getDynamicMode()
print("Dynamic settings: " + dynamic)

kel.endComm()
