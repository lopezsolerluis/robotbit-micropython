# Adaptado de https://github.com/KittenBot/pxt-robotbit/blob/master/main.ts
# Imports go at the top
import microbit
import time

PCA9685_ADDRESS = 0x40
MODE1 = 0x00
MODE2 = 0x01
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


def i2cwrite(addr, reg, val):
    microbit.i2c.write(addr, bytes([reg, val]))

def i2cread(addr, reg):
    microbit.i2c.write(addr, bytes([reg]))
    return microbit.i2c.read(addr,1)[0]

def initPCA():
    i2cwrite(PCA9685_ADDRESS, MODE1, 0x00)
    setFreq(50)
    for i in range(0, 16):
        setPwm(i, 0, 0)

def setFreq(freq):
    prescale = int(25000000.0 / 4096.0 / freq + 0.5)
    oldmode = i2cread(PCA9685_ADDRESS, MODE1)
    newmode = (oldmode & 0x7F) | 0x10 # sleep
    i2cwrite(PCA9685_ADDRESS, MODE1, newmode) # go to sleep
    i2cwrite(PCA9685_ADDRESS, PRESCALE, prescale) # set the prescaler
    i2cwrite(PCA9685_ADDRESS, MODE1, oldmode)
    time.sleep_us(5)
    i2cwrite(PCA9685_ADDRESS, MODE1, oldmode | 0xa1)

def setPwm(channel, on, off):
    microbit.i2c.write(PCA9685_ADDRESS, bytes([LED0_ON_L + 4 * channel, on & 0xff, (on >> 8) & 0xff, off & 0xff, (off >> 8) & 0xff]))

def servo(servo, degree): # servo: 1, etc.
    v_us = (degree * 1800 / 180 + 600) # 0.6 ~ 2.4
    value = v_us * 4096 / 20000
    setPwm(servo + 7, 0, int(value))

def setStepper(index, dir): # index: 1 o 2, dir: True o False
   if (index == 1):
       if (dir): 
           setPwm(0, STP_CHA_L, STP_CHA_H)
           setPwm(2, STP_CHB_L, STP_CHB_H)
           setPwm(1, STP_CHC_L, STP_CHC_H)
           setPwm(3, STP_CHD_L, STP_CHD_H)
       else:
           setPwm(3, STP_CHA_L, STP_CHA_H)
           setPwm(1, STP_CHB_L, STP_CHB_H)
           setPwm(2, STP_CHC_L, STP_CHC_H)
           setPwm(0, STP_CHD_L, STP_CHD_H)
   else:
       if (dir):
           setPwm(4, STP_CHA_L, STP_CHA_H)
           setPwm(6, STP_CHB_L, STP_CHB_H)
           setPwm(5, STP_CHC_L, STP_CHC_H)
           setPwm(7, STP_CHD_L, STP_CHD_H)
       else:
           setPwm(7, STP_CHA_L, STP_CHA_H)
           setPwm(5, STP_CHB_L, STP_CHB_H)
           setPwm(6, STP_CHC_L, STP_CHC_H)
           setPwm(4, STP_CHD_L, STP_CHD_H)

def stopMotor(index):
    for i in range(0,4) if (index == 1) else range(4,8):
        setPwm(i, 0, 0)
    
def stepperDegree(index, degree): # index: 1 o 2    
    setStepper(index, degree > 0)
    degree = abs(degree)
    microbit.sleep(10240 * degree / 360) # cambiar por algo "no bloqueante"
    stopMotor(index)
    
initPCA()
# Para mover un servo, por ahora hacer: servo(número, ángulo)
# Para mover un motor paso a paso, por ahora hacer: stepperDegree(número, ángulo)
   