import socket
import time

class koradUdpComm(object):

    def __init__(self, localAddress, deviceAddress, port):
        self.clientAddress = (localAddress, port)
        self.deviceAddress = (deviceAddress, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.sock.bind(self.clientAddress)
        self.sock.settimeout(1.0)

    def close(self):
        self.sock.close()

    def udpSendRecv(self, message):
        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        startTime = time.time()
        while True:
            sent = self.sock.sendto(messageb, self.deviceAddress)
            self.sock.settimeout(1.0)
            data, server = self.sock.recvfrom(1024)
            if len(data) > 0:
                return data.decode('utf-8')

            if time.time() - startTime > 3:
                print ("UDP timeout")
                return " "

    def udpSend(self, message):
        # build the message
        messageb = bytearray()
        messageb.extend(map(ord, message))
        messageb.append(0x0a)

        sent = self.sock.sendto(messageb, self.deviceAddress)


class kel103(object):
    def __init__(self, localAddress, deviceAddress, port):
        self.device = koradUdpComm(localAddress, deviceAddress, port)
        self.device.connect()

    def endComm(self):
        self.device.close()

    def deviceInfo(self):
        """
        Device info string containing device type, revision, and serial number
        """
        return self.device.udpSendRecv('*IDN?').strip()

    def checkDevice(self):
        """
        Returns True if the device returns a sane deviceInfo, False otherwise.
        """
        return 'KEL103' in self.deviceInfo()

    def setDhcp(self, state):
        if state:
            self.device.udpSend(':SYST:DHCP 1')
        else: 
            self.device.udpSend(':SYST:DHCP 0')

    def ipAddress(self):
        return self.device.udpSendRecv(':SYST:IPAD?').strip()
    def setIpAddress(self, ip):
        print("You will have to reconnect to the new IP now.")
        self.device.udpSend(f':SYST:IPAD {ip}')

    def port(self):
        return int(self.device.udpSendRecv(':SYST:PORT?').strip())
    def setPort(self, port):
        print("You will have to reconnect to the new port now. (Some ports seem not to be selectable, in which case the next higher port seems to be chosen.)")
        self.device.udpSend(f':SYST:PORT {port}')

    def netmask(self):
        return self.device.udpSendRecv(':SYST:SMASK?').strip()
    def setNetmask(self, mask):
        self.device.udpSend(f':SYST:SMASK {mask}')

    def gateway(self):
        return self.device.udpSendRecv(':SYST:GATE?').strip()
    def setGateway(self, gate):
        self.device.udpSend(f':SYST:GATE {gate}')

    def baudRate(self):
        return int(self.device.udpSendRecv(':SYST:BAUD?').strip())
    def setBaudRate(self, baud):
        possible_rates = [9600, 19200, 38400, 57600, 115200]
        if not baud in possible_rates:
            raise ValueError(f"The baud rate must be one of {possible_rates}.")
        self.device.udpSend(f':SYST:BAUD {baud}')

    # there exist ":SYST:DEVINFO" and ":SYST:FACTRESET" options that don't seem to work properly


    def measureVolt(self):
        """
        Measure voltage drop over internal load
        """
        s = self.device.udpSendRecv(':MEAS:VOLT?')
        return float(s.strip('V\n'))

    def measureSetVolt(self):
        """
        Return set voltage drop over internal load, should be equal to what was requested
        """
        s = self.device.udpSendRecv(':VOLT?')
        return float(s.strip('V\n'))

    def setMaxVoltage(self, maxV):
        self.device.udpSend(f':VOLT:UPP {maxV}V')
    def minVoltage(self):
        return float(self.device.udpSendRecv(':VOLT:LOW?').strip('\nV'))
    def maxVoltage(self):
        return float(self.device.udpSendRecv(':VOLT:UPP?').strip('\nV'))

    def setVolt(self, voltage):
        """
        Set voltage, implies 'constant voltage' mode
        """
        s = self.device.udpSend(f':VOLT {voltage}V')
        if self.measureSetVolt() != voltage:
            raise ValueError('Voltage set incorrectly on the device')

    def measurePower(self):
        s = self.device.udpSendRecv(':MEAS:POW?')
        return float(s.strip('W\n'))

    def measureSetPower(self):
        """
        Return set power, should be equal to what was requested
        """
        s = self.device.udpSendRecv(':POW?')
        return float(s.strip('W\n'))

    def setMaxPower(self, maxP):
        self.device.udpSend(f':POW:UPP {maxP}W')
    def minPower(self):
        return float(self.device.udpSendRecv(':POW:LOW?').strip('\nW'))
    def maxPower(self):
        return float(self.device.udpSendRecv(':POW:UPP?').strip('\nW'))

    def setPower(self, power):
        """
        Set power, implies 'constant power' mode
        """
        s = self.device.udpSend(f':POW {power}W')
        if self.measureSetPower() != power:
            raise ValueError('Power set incorrectly on the device')

    def measureCurrent(self):
        s = self.device.udpSendRecv(':MEAS:CURR?')
        return float(s.strip('A\n'))

    def measureSetCurrent(self):
        """
        Return set current, should be equal to what was requested
        """
        s = self.device.udpSendRecv(':CURR?')
        return float(s.strip('A\n'))

    def setMaxCurrent(self, maxC):
        self.device.udpSend(f':CURR:UPP {maxC}A')
    def minCurrent(self):
        return float(self.device.udpSendRecv(':CURR:LOW?').strip('\nA'))
    def maxCurrent(self):
        return float(self.device.udpSendRecv(':CURR:UPP?').strip('\nA'))

    def setCurrent(self, current):
        """
        Set current, implies 'constant current' mode
        """
        s = self.device.udpSend(f':CURR {current}A')
        if self.measureSetCurrent() != current:
            raise ValueError('Current set incorrectly on the device')

    def setResistance(self, resistance):
        """
        Set resistance, implies 'constant resistance' mode
        """
        s = self.device.udpSend(f':RES {resistance}OHM')

    def measureSetResistance(self):
        """
        Return set resistance, should be equal to what was requested
        """
        s = self.device.udpSendRecv(':RES?')
        return float(s.strip('OHM\n'))

    def setMaxResistance(self, maxR):
        self.device.udpSend(f':RES:UPP {maxR}OHM')
    def minResistance(self):
        return float(self.device.udpSendRecv(':RES:LOW?').strip('\nOHM'))
    def maxResistance(self):
        return float(self.device.udpSendRecv(':RES:UPP?').strip('\nOHM'))

    def checkOutput(self):
        return self.device.udpSendRecv(':INP?').strip() == "ON"

    def setOutput(self, state):
        if state:
            self.device.udpSend(':INP 1')
        else:
            self.device.udpSend(':INP 0')
        if self.checkOutput() != state:
            raise ValueError('Caution: Output not set correctly')

    def setConstantCurrent(self):
        self.device.udpSend(':FUNC CC')

    def setConstantVoltage(self):
        self.device.udpSend(':FUNC CV')

    def setConstantPower(self):
        self.device.udpSend(':FUNC CW')

    def setConstantResistance(self):
        self.device.udpSend(':FUNC CR')

    def setDynamicModeCV(self, voltage1, voltage2, freq, dutycycle):
        cmd = ':DYN 1,'
        cmd += '%.3fV,' % voltage1
        cmd += '%.3fV,' % voltage2
        cmd += '%.3fHZ,' % freq
        cmd += '%.3f%%' % dutycycle
        s = self.device.udpSend(cmd)

    def setDynamicModeCC(self, slope1, slope2, current1, current2, freq, dutycycle):
        cmd = ':DYN 2,'
        cmd += '%.3fA/uS,' % slope1
        cmd += '%.3fA/uS,' % slope2
        cmd += '%.3fA,' % current1
        cmd += '%.3fA,' % current2
        cmd += '%.3fHZ,' % freq
        cmd += '%.3f%%' % dutycycle
        s = self.device.udpSend(cmd)

    def getDynamicMode(self):
        return self.device.udpSendRecv(':DYN?').strip() == "ON"

    def getBeep(self):
        return self.device.udpSendRecv(':SYST:BEEP?').strip() == "ON"
    def setBeep(self, state):
        if state:
            self.device.udpSend(':SYST:BEEP 1')
        else:
            self.device.udpSend(':SYST:BEEP 0')

