# Adapted from https://github.com/KittenBot/pxt-robotbit/blob/master/main.ts

from microbit import i2c
import time

PCA9685_ADDRESS = 0x40
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

STP_CHA_L = 2047
STP_CHA_H = 4095
STP_CHB_L = 1
STP_CHB_H = 2047
STP_CHC_L = 1023
STP_CHC_H = 3071
STP_CHD_L = 3071
STP_CHD_H = 1023

class PCA9685:

    def __init__(self):
        self.i2cwrite(PCA9685_ADDRESS, MODE1, 0x00)
        self.setFreq(50)
        for i in range(0, 16):
            self.setPwm(i, 0, 0)

    def i2cwrite(self, addr, reg, val):
        i2c.write(addr, bytes([reg, val]))

    def i2cread(self, addr, reg):
        i2c.write(addr, bytes([reg]))
        return i2c.read(addr,1)[0]

    def setFreq(self, freq):
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        oldmode = self.i2cread(PCA9685_ADDRESS, MODE1)
        newmode = (oldmode & 0x7F) | 0x10 # sleep
        self.i2cwrite(PCA9685_ADDRESS, MODE1, newmode) # go to sleep
        self.i2cwrite(PCA9685_ADDRESS, PRESCALE, prescale) # set the prescaler
        self.i2cwrite(PCA9685_ADDRESS, MODE1, oldmode)
        time.sleep_us(5)
        self.i2cwrite(PCA9685_ADDRESS, MODE1, oldmode | 0xa1)

    def setPwm(self, channel, on, off):
        i2c.write(PCA9685_ADDRESS, bytes([LED0_ON_L + 4 * channel, on & 0xff, (on >> 8) & 0xff, off & 0xff, (off >> 8) & 0xff]))

    def setServoDegree(self, servo, degree): # servo: 1, etc.
        v_us = (degree * 1800 / 180 + 600) # 0.6 ~ 2.4
        value = v_us * 4096 / 20000
        self.setPwm(servo + 7, 0, int(value))

    def setStepper(self, index, dir): # index: 1 o 2, dir: True o False
       if (index == 1):
           if (dir): 
               self.setPwm(0, STP_CHA_L, STP_CHA_H)
               self.setPwm(2, STP_CHB_L, STP_CHB_H)
               self.setPwm(1, STP_CHC_L, STP_CHC_H)
               self.setPwm(3, STP_CHD_L, STP_CHD_H)
           else:
               self.setPwm(3, STP_CHA_L, STP_CHA_H)
               self.setPwm(1, STP_CHB_L, STP_CHB_H)
               self.setPwm(2, STP_CHC_L, STP_CHC_H)
               self.setPwm(0, STP_CHD_L, STP_CHD_H)
       else:
           if (dir):
               self.setPwm(4, STP_CHA_L, STP_CHA_H)
               self.setPwm(6, STP_CHB_L, STP_CHB_H)
               self.setPwm(5, STP_CHC_L, STP_CHC_H)
               self.setPwm(7, STP_CHD_L, STP_CHD_H)
           else:
               self.setPwm(7, STP_CHA_L, STP_CHA_H)
               self.setPwm(5, STP_CHB_L, STP_CHB_H)
               self.setPwm(6, STP_CHC_L, STP_CHC_H)
               self.setPwm(4, STP_CHD_L, STP_CHD_H)

    def stopMotor(self, index):
        for i in range(0,4) if (index == 1) else range(4,8):
            self.setPwm(i, 0, 0)
    
    def setStepperDegree(self, index, degree): # index: 1 o 2    
        self.setStepper(index, degree > 0)
        delta_ms = int(abs(10240 * degree / 360))
        return delta_ms # returns milliseconds to stop
        #self.stopMotor(index)

if __name__=='__main__':   

    pca = PCA9685()
    pca.setServoDegree(1, 90) 
    delta = pca.setStepperDegree(1, 90)
    time.sleep_ms(delta)
    pca.stopMotor(1)
    