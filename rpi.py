import socket, time, json
import RPi.GPIO as GPIO # type: ignore

host_ip = '10.0.0.8' 
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
print("1")

#set thrusters on bottomside
thruster_5 = 0
thruster_4 = 0
thruster_3 = 0
thruster_2 = 0
thruster_1 = 0
thrusters = [thruster_5, thruster_4, thruster_3, thruster_2, thruster_1]

servoPIN = [14, 1, 8, 15, 0] #define GPIO pins for thrusters
GPIO.setmode(GPIO.BCM) #initialize GPIO
for pin in servoPIN:
    GPIO.setup(pin, GPIO.OUT)
pwm_objects = [GPIO.PWM(pin, 100) for pin in servoPIN] #100 Hz frequency
for pwm in pwm_objects:
    pwm_objects.start(2.5) # Initialization

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

    for thruster, pin in zip(thrusters, servoPIN):
        set_thrusters(thruster, pin)
         #thruster = ___ 
    
    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        pwm_objects.stop()
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