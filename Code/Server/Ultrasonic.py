import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
RANGE = 30
STEP = 10
class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1
     
    def get_distance(self):
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(distance_cm[2])
    def run_motor(self,L,M,R):
        if (L < RANGE and M < RANGE and R < RANGE) or M < RANGE :
            self.PWM.setMotorModel(-1450,-1450,-1450,-1450) 
            time.sleep(0.1)   
            if L < R:
                self.PWM.setMotorModel(1450,1450,-1450,-1450)
            else :
                self.PWM.setMotorModel(-1450,-1450,1450,1450)
        elif L < RANGE and M < RANGE:
            PWM.setMotorModel(1500,1500,-1500,-1500)
        elif R < RANGE and M < RANGE:
            PWM.setMotorModel(-1500,-1500,1500,1500)
        elif L < RANGE - STEP :
            PWM.setMotorModel(2000,2000,-500,-500)
            if L < RANGE - STEP * 2 :
                PWM.setMotorModel(1500,1500,-1000,-1000)
        elif R < RANGE - STEP * 2 :
            PWM.setMotorModel(-500,-500,2000,2000)
            if R < RANGE - STEP :
                PWM.setMotorModel(-1500,-1500,1500,1500)
        else :
            self.PWM.setMotorModel(600,600,600,600)
                
    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('1', 70)
        deg = 30
        for i in range(deg, deg * 5 + 1,deg * 2):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i == deg:
                    L = self.get_distance()
                elif i == deg * 3:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
        while True:
            for i in range(deg * 3, deg,-deg * 2):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i == deg:
                    L = self.get_distance()
                elif i == deg * 3:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
            for i in range(deg, (deg * 5) + 1, deg * 2):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i == deg:
                    L = self.get_distance()
                elif i == deg * 3:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
        
            
        
ultrasonic=Ultrasonic()              
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)

