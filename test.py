import board
import busio
import pwmio
#import RPi.GPIO as GPIO # type: ignore
import adafruit_pca9685 #import PCA9685
from adafruit_servokit import ServoKit
import socket, time, json, sys


#set thrusters on bottomside
thruster_5 = 0 #5
thruster_4 = 0 #4
thruster_3 = 0 #3
thruster_2 = 0 #2
thruster_1 = 0 #1
thrusters = [thruster_5, thruster_4, thruster_3, thruster_2, thruster_1]

i2c = busio.I2C(board.SCL, board.SDA)
print("{i2c}")
listofdev = i2c.scan()
print(listofdev)

i2c = board.I2C() # uses board.SCL and board.SDA
shield = adafruit_pca9685.PCA9685(i2c)
kit = ServoKit(channels=16)
shield.frequency = 100 #was 100

thrusterChannel = [shield.channels[14], shield.channels[1], shield.channels[8], shield.channels[15], shield.channels[2]]

# thrusterChannel[0] = shield.channels[14]
# thrusterChannel[1] = shield.channels[1]
# thrusterChannel[2] = shield.channels[8]
# thrusterChannel[3] = shield.channels[15]
# thrusterChannel[4] = shield.channels[2]

pwm_values = [1000, 1500, 2000]


for y in range(0,5):
   thrusterChannel[y].duty_cycle = 0x2666


for x in range(90, 110):
    print("shield freq: " + str(x))
    shield.frequency = x

    for z in range(0, 4):
      for i in range(0, 5):
        throttlePW = int((pwm_values[z]/10000*65536)*(x/100))
        thrusterChannel[i].duty_cycle = throttlePW
        print(i)
        time.sleep(0.25)



    # #5
    # throttlePW = int((pwm_values[1]/10000*65536)*(x/100))
    # thrusterChannel5.duty_cycle = throttlePW
    # time.sleep(0)
    # print("5")
    # time.sleep(0.005)

    # #4
    # throttlePW = int((pwm_values[1]/10000*65536)*(x/100))
    # thrusterChannel4.duty_cycle = throttlePW
    # time.sleep(0)
    # print("4")
    # time.sleep(0.005)


    # #3
    # throttlePW = int((pwm_values[1]/10000*65536)*(x/100))
    # thrusterChannel3.duty_cycle = throttlePW
    # time.sleep(0)
    # print("3")
    # time.sleep(0.005)


    # #2
    # throttlePW = int((pwm_values[1]/10000*65536)*(x/100))
    # thrusterChannel2.duty_cycle = throttlePW
    # time.sleep(0)
    # print("2")
    # time.sleep(0.005)


    # #1
    # throttlePW = int((pwm_values[1]/10000*65536)*(x/100))
    # thrusterChannel1.duty_cycle = throttlePW
    # time.sleep(0)
    # print("1")
    # time.sleep(0.005)

    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        sys.exit()
        #figure out how to exit porgram with command