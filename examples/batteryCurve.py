"""
This sample program will use the kel103 to test a battery's capacity and
show this information in matplotlib. This method is an aproximation and its
resolution can be increased with sampling rate.
"""

import time
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from korad import kel103

#test proporties
cutOffVoltage = 2.0
dischargeRate = 5.0
MISSED_LIMIT = 10 # amount of missed samples that is allowed

# setup the device (the IP of your ethernet/wifi interface, the IP of the Korad device)
host_ip = "192.168.x.x"
device_ip = "192.168.x.x"
port = 18190
kel = kel103.kel103(host_ip, device_ip, port)
kel.checkDevice()

# a quick battery test
kel.setOutput(False)
voltage = kel.measureVolt()
kel.setCurrent(dischargeRate)
voltageData = []
timeData = []
current = 0
capacity = 0
kel.setOutput(True)

# run the test
startTime = time.time()
missedSuccessiveSamples = 0

fileBasename = f"test_{time.time()}"

while voltage > cutOffVoltage:
    try:
        # store the time before measuring volt/current
        currentTime = (time.time() - startTime)
        voltage = kel.measureVolt()
        current = kel.measureCurrent()
        voltageData.append(voltage)
        # Only append the timedata when volt/current measurements went fine.
        # This is because the voltage or current measurement could fail
        # and then the x and y-axis would have different dimensions
        timeData.append(currentTime)

        # solve the current stuff as a running accumulation
        capacity = ((time.time() - startTime) / 3600) * current

        print(f"Voltage: {voltage:.3f} V DC, Capacity: {capacity:.3f} Ah")
        time.sleep(1.0)
        missedSuccessiveSamples = 0

        with open(f'{fileBasename}.txt', 'a') as f:
          f.write(f"{currentTime} {voltage}\n")
    except Exception as e:
        print(e)
        missedSuccessiveSamples += 1
        if missedSuccessiveSamples >= MISSED_LIMIT:
            raise Exception("Too many missed samples!")

# disable the output
kel.setOutput(False)
kel.endComm()

# plot the finished data
fig, ax = plt.subplots()
ax.plot(timeData, voltageData)

ax.set(xlabel='time (s)',
       ylabel='voltage (V DC)',
       title=f'Battery Discharge Test {dischargeRate:.3f}A: {capacity:.4f}Ah')
ax.grid()

fig.savefig(f"{fileBasename}.png")
plt.show()
