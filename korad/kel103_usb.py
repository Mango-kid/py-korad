import time
import serial
import io
import sys

class koradUSBComm(object):

    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.timeout = 1

    def udpSendRecv(self, message):
        startTime = time.time()
        with serial.Serial(self.port, self.baud, timeout=self.timeout) as ser:
            sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
            sio.write(message + '\n')
            sio.flush()
            sOut = ser.readline()
            ser.close
            return sOut.decode('utf-8')

    def udpSend(self, message):
        with serial.Serial(self.port, self.baud, timeout=self.timeout) as ser:
            sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
            sio.write(message + '\n')
            sio.flush()
            ser.close

class kel103(object):

    def __init__(self, port, baud):
        self.device = koradUSBComm(port, baud)

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
        return
