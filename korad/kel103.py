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
        while 1:
            sent = self.sock.sendto(messageb , self.deviceAddress)
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

        sent = self.sock.sendto(messageb , self.deviceAddress)

class kel103(object):

    def __init__(self, localAddress, deviceAddress, port):
        self.device = koradUdpComm(localAddress, deviceAddress, port)
        self.device.connect()

    def deviceInfo(self):
        return self.device.udpSendRecv('*IDN?')
    
    def checkDevice(self):
        if 'KEL103' in self.deviceInfo():
            return True
        else:
            return False

    def measureVolt(self):
        s = self.device.udpSendRecv(':MEAS:VOLT?')
        return float(s.strip('V\n'))
    
    def measureSetVolt(self):
        s = self.device.udpSendRecv(':VOLT?')
        return float(s.strip('V\n'))

    def setVolt(self, voltage):
        s = self.device.udpSend(':VOLT ' + str(voltage) + 'V')
        if self.measureSetVolt() != voltage:
            raise ValueError('Voltage set incorectly on the device')

    def measurePower(self):
        s = self.device.udpSendRecv(':MEAS:POW?')
        return float(s.strip('W\n'))

    def measureSetPower(self):
        s = self.device.udpSendRecv(':POW?')
        return float(s.strip('W\n'))

    def setPower(self, power):
        s = self.device.udpSend(':POW ' + str(power) + 'W')
        if self.measureSetPower() != power:
            raise ValueError('Power set incorectly on the device')

    def measureCurrent(self):
        s = self.device.udpSendRecv(':MEAS:CURR?')
        return float(s.strip('A\n'))

    def measureSetCurrent(self):
        s = self.device.udpSendRecv(':CURR?')
        return float(s.strip('A\n'))

    def setCurrent(self, current):
        s = self.device.udpSend(':CURR ' + str(current) + 'A')
        if self.measureSetCurrent() != current:
            raise ValueError('Current set incorectly on the device')

    def checkOutput(self):
        s = self.device.udpSendRecv(':INP?')
        if 'OFF' in s:
            return False
        if 'ON' in s:
            return True

    def setOutput(self, state):
        if state == True:
            self.device.udpSend(':INP 1')
            if self.checkOutput() != state:
                raise ValueError('Caution: Output not set')
        if state == False:
            self.device.udpSend(':INP 0')
            if self.checkOutput() != state:
                raise ValueError('Caution: Output not set')
                
    def setConstantCurrent(self):
        self.device.udpSend(':FUNC CC')

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
        s = self.device.udpSendRecv(':DYN?')
        return s.strip('\n')
        
    def endComm(self):
        self.device.close()
