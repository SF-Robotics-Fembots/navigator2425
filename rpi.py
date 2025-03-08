import socket, requests, time, json
import RPi.GPIO as GPIO # type: ignore

host_ip = '10.0.0.8' 
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
print("1")
#s.sendall(b"hello, world")
#print("...")
#data = s.recv(1024)
#print(f"recieved message: ")

thruster_5 = 0
thruster_4 = 0
thruster_3 = 0
thruster_2 = 0
thruster_1 = 0

servoPIN = [14, 1, 8, 15, 0]
GPIO.setmode(GPIO.BCM)
for pin in servoPIN:
    GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 100) #100 Hz frequency

# def set_thrusters_pwms(pwm_values):
#     for thruster, pwm_value in zip(thrusters, pwm_values):
#         thruster.ChangeDutyCycle(pwm_value)

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


p.start(2.5) # Initialization
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
    # pwm_string = data.decode('utf-8')
    # pwm_values = list(map(float, pwm_string.split(',')))
    print("received pwm values:", pwm_values)



    thrusters = [thruster_5, thruster_4, thruster_3, thruster_2, thruster_1]

    for thruster in thrusters:
        pass
         #thruster = ___ 
    
    
    try:
        time.sleep(0.005)
    except KeyboardInterrupt:
        p.stop()
        #figure out how to exit porgram with command
    except:
        GPIO.cleanup()