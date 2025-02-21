#!/usr/bin/env python
"""
This sample program uses the kel103 to measure the voltage drop and current
for two resistances and calculate the internal resistance of the battery.  
"""

import time
from korad import kel103


def measureVoltageAndCurrentAtResistance(kel, resistance):
    kel.setResistance(resistance)
    kel.setOutput(True)
    time.sleep(1.0)
    u1 = kel.measureVolt()
    i1 = kel.measureCurrent()
    kel.setOutput(False)
    return u1, i1

def main():
    host_ip = "192.168.x.x"
    device_ip = "192.168.x.x"
    port = 18190
    kel = kel103.kel103(host_ip, device_ip, port)
    kel.setOutput(False)
    
    u1, i1 = measureVoltageAndCurrentAtResistance(kel, 5)
    u2, i2 = measureVoltageAndCurrentAtResistance(kel, 10)

    ri = (u1 - u2) / (i2 - i1)
    print(f"internal resistance {ri}")

if __name__ == "__main__":
    main()

