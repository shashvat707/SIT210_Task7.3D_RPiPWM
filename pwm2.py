import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
# US-100:
#       VCC to PI PIN-2
#       GND to PI PIN-6
#       TRIGGER to PIN-11
#       ECHO to PIN-13
# BUZZER
#       +ve to PIN-22
#       -ve to 100 ohm resistor to GND

GPIO_TRIG = 11
GPIO_ECHO = 13
GPIO_BUZZ = 22
i=0
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_BUZZ, GPIO.OUT)

buz_pwm = GPIO.PWM(GPIO_BUZZ, 100)
buz_pwm.start(0)
GPIO.output(GPIO_TRIG, False)
print "Calibrating....."
time.sleep(2)

MAX_DISTANCE = 100
Calibration = 0

print "Place the object......"

try:
    while True:
        #print "In loop"
    	GPIO.output(GPIO_TRIG, True)
       	time.sleep(0.00001)
       	GPIO.output(GPIO_TRIG, False)

       	while GPIO.input(GPIO_ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(GPIO_ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # Distance = Velocity of Sound * (Time/2)
        # Vel of sound = 34300 cm/s
        # Distance = 34300 * Time / 2 = Time * 17150
        distance = pulse_duration * 17150

        #Round to two decimal
        distance = round(distance + Calibration, 2)
        print "dist:",distance
        if distance<=MAX_DISTANCE and distance>=5:
            #print "distance:",distance,"cm"
            duty_cycle = min(100,(100-distance*100/MAX_DISTANCE))
            print "duty_cycle:",duty_cycle
            buz_pwm.ChangeDutyCycle(duty_cycle)
            i=1

        if distance>MAX_DISTANCE and i==1:
            buz_pwm.ChangeDutyCycle(0)
            print "place the object...."
            i=0
        time.sleep(0.75)

except KeyboardInterrupt:
    GPIO.cleanup()
