import socket, time, json
#from adafruit_pca9685 import PCA9568
import adafruit_pca968
import pwmio
import RPi.GPIO as GPIO # type: ignore

host_ip = '10.0.0.8'
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
print("1")

#set thrusters on bottomside
thruster_e = 0 #5
thruster_d = 0 #4
thruster_c = 0 #3
thruster_b = 0 #2
thruster_a = 0 #1
thrusters = [thruster_e, thruster_d, thruster_c, thruster_b, thruster_a]

# servoPIN = [14, 1, 8, 15, 0] #define GPIO pins for thrusters
# GPIO.setmode(GPIO.BCM) #initialize GPIO
# for pin in servoPIN:
#     GPIO.setup(pin, GPIO.OUT)
# pwm_objects = [GPIO.PWM(pin, 100) for pin in servoPIN] #100 Hz frequency
# for pwm in pwm_objects:
#     pwm_objects.start(2.5) # Initialization

servoPIN_5 = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_5, GPIO.OUT)
p = GPIO.PWM(servoPIN_5, 100)
p.start(2.5)

servoPIN_4 = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_4, GPIO.OUT)
p = GPIO.PWM(servoPIN_4, 100)
p.start(2.5)

servoPIN_3 = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_3, GPIO.OUT)
p = GPIO.PWM(servoPIN_3, 100)
p.start(2.5)

servoPIN_2 = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_2, GPIO.OUT)
p = GPIO.PWM(servoPIN_2, 100)
p.start(2.5)

servoPIN_1 = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_1, GPIO.OUT)
p = GPIO.PWM(servoPIN_1, 100)
p.start(2.5)


def set_thrusters(thruster, pin):
    print(f"Setting Pin: {pin} to Thruster: {thruster}")

# def set_thrusters_pwms(pwm_values, thrusters):
#     for thruster, pwm_value in zip(thrusters, pwm_values):
#         thruster.ChangeDutyCycle(pwm_value)
# set_thrusters_pwms(pwm_values, thrusters)

datain = client_socket.recv(1024)
client_socket.setblocking(False)
while True:
    while True:
        try:
            datain = client_socket.recv(1024)
            print("DI", datain)
        except BlockingIOError:
            # if len(datain) < 5: break
            data = datain[-30:] #orignially -44 for pwm_values
            break
    #if not data: break
    print("D", data)
    json_data = data.decode('utf-8')
    pwm_values = json.loads(json_data)
    print("received pwm values:", pwm_values)

    

    throttlePW = int(pwm_values[0]/10000*65536)
    thruster_e.duty_cycle = throttlePW

    throttlePW = int(pwm_values[1]/10000*65536)
    thruster_d.duty_cycle = throttlePW

    throttlePW = int(pwm_values[2]/10000*65536)
    thruster_c.duty_cycle = throttlePW

    throttlePW = int(pwm_values[3]/10000*65536)
    thruster_b.duty_cycle = throttlePW

    throttlePW = int(pwm_values[4]/10000*65536)
    thruster_a.duty_cycle = throttlePW

    # for thruster, pin in zip(thrusters, servoPIN):
    #     set_thrusters(thruster, pin)
    #      #thruster = ___
    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        p.stop()
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