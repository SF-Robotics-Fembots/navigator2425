import board
import busio
import pwmio
#import RPi.GPIO as GPIO # type: ignore
import adafruit_pca9685 #import PCA9685
from adafruit_servokit import ServoKit
import socket, time, json, sys

host_ip = '192.168.1.68'#'10.0.0.8'
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
print("1")

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
shield.frequency = 98 #was 100

thrusterChannel5 = shield.channels[14] #left vertical
thrusterChannel4 = shield.channels[11] #right vertical
thrusterChannel3 = shield.channels[8] #middle
thrusterChannel2 = shield.channels[15] #left horizontal
thrusterChannel1 = shield.channels[10] #right horizontal
thrusterChannel5.duty_cycle = 0x2666

datain = client_socket.recv(1024)
client_socket.setblocking(False)
while True:
    while True:
        try:
            datain = (client_socket.recv(1024)).decode() #client_socket.recv(1024)
            #print("DI", datain)
        except BlockingIOError:
            # if len(datain) < 5: break
            data = datain[-30:] #orignially -44 for pwm_values
            break
    #if not data: break
    #print("D", data)
    #json_data = data.decode('utf-8')
    pwm_values = json.loads(data)
    print("received pwm values:", pwm_values)

    throttlePW = int((pwm_values[0]/10000*65536)*(98/100))
    thrusterChannel5.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int((pwm_values[1]/10000*65536)*(98/100))
    thrusterChannel4.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int((pwm_values[2]/10000*65536)*(98/100))
    thrusterChannel3.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int((pwm_values[3]/10000*65536)*(98/100))
    thrusterChannel2.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int((pwm_values[4]/10000*65536)*(98/100))
    thrusterChannel1.duty_cycle = throttlePW
    time.sleep(0)
    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        sys.exit()
        #figure out how to exit porgram with command