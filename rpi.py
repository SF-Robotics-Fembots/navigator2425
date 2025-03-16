import board
import busio
import pwmio
#import RPi.GPIO as GPIO # type: ignore
import adafruit_pca9685 #import PCA9685
from adafruit_servokit import ServoKit
import socket, time, json, sys

host_ip = '172.20.10.11'#'10.0.0.8'
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

# servoPIN = [14, 1, 8, 15, 0] #define GPIO pins for thrusters
# GPIO.setmode(GPIO.BCM) #initialize GPIO
# for pin in servoPIN:
#     GPIO.setup(pin, GPIO.OUT)
# pwm_objects = [GPIO.PWM(pin, 100) for pin in servoPIN] #100 Hz frequency
# for pwm in pwm_objects:
#     pwm_objects.start(2.5) # Initialization

# servoPIN_5 = 14
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN_5, GPIO.OUT)
# p = GPIO.PWM(servoPIN_5, 100)
# p.start(2.5)

# servoPIN_4 = 1
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN_4, GPIO.OUT)
# p = GPIO.PWM(servoPIN_4, 100)
# p.start(2.5)

# servoPIN_3 = 8
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN_3, GPIO.OUT)
# p = GPIO.PWM(servoPIN_3, 100)
# p.start(2.5)

# servoPIN_2 = 15
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN_2, GPIO.OUT)
# p = GPIO.PWM(servoPIN_2, 100)
# p.start(2.5)

# servoPIN_1 = 0
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN_1, GPIO.OUT)
# p = GPIO.PWM(servoPIN_1, 100)
# p.start(2.5)

i2c = busio.I2C(board.SCL, board.SDA)
print("{i2c}")
listofdev = i2c.scan()
print(listofdev)

i2c = board.I2C() # uses board.SCL and board.SDA
shield = adafruit_pca9685.PCA9685(i2c)
kit = ServoKit(channels=16)
shield.frequency = 100

thrusterChannel5 = shield.channels[14]
thrusterChannel4 = shield.channels[1]
thrusterChannel3 = shield.channels[8]
thrusterChannel2 = shield.channels[15]
thrusterChannel1 = shield.channels[0]
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

    throttlePW = int(pwm_values[0]/10000*65536)
    thrusterChannel5.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int(pwm_values[1]/10000*65536)
    thrusterChannel4.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int(pwm_values[2]/10000*65536)
    thrusterChannel3.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int(pwm_values[3]/10000*65536)
    thrusterChannel2.duty_cycle = throttlePW
    time.sleep(0)

    throttlePW = int(pwm_values[4]/10000*65536)
    thrusterChannel1.duty_cycle = throttlePW
    time.sleep(0)

    # for thruster, pin in zip(thrusters, servoPIN):
    #     set_thrusters(thruster, pin)
    #      #thruster = ___
    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        sys.exit()
        # p.stop()
        #figure out how to exit porgram with command
    except:
        GPIO.cleanup()

# def get_pwm_value():
#         try:
#         SERVER_URL = ""
#         response = requests.get(SERVER_URL)
#         response.raise_for_status()
#         pwm_value = response.json().get('pwm_values')
#         if 1000 <= pwm_value <= 2000:
#             return pwm_value
#         else:
#             print("PWM value out of range")
#             return None

#s.sendall(b"hello, world")
#print("...")
#data = s.recv(1024)
#print(f"recieved message: ")

# pwm_string = data.decode('utf-8')
# pwm_values = list(map(float, pwm_string.split(',')))