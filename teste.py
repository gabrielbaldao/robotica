import RPi.GPIO as gpio
import time

#Configuring don’t show warnings 
gpio.setwarnings(False)

#Configuring GPIO
gpio.setmode(gpio.BOARD)
gpio.setup(17,gpio.OUT)
gpio.setup(18,gpio.OUT)

#Configure the pwm objects and initialize its value
pwmBlue = gpio.PWM(17,100)
pwmBlue.start(0)

pwmRed = gpio.PWM(18,100)
pwmRed.start(100)
 
#Create the dutycycle variables
dcBlue = 0
dcRed  = 100
def mudaPWM(pwm1, pwm2):
    pwm1.ChangeDutyCycle(100)
    pwm2.ChangeDutyCycle(0)
    time.sleep(2)

#Loop infinite
while True:
   
    #increment gradually the luminosity
    mudaPWM(pwmRed, pwmBlue)
    mudaPWM(pwmBlue,pwmRed)


    #decrement gradually the luminosity
    

    
#End code
gpio.cleanup()
exit()