import socket
import requests
import RPi.GPIO as GPIO # type: ignore
import time

host_ip = '10.0.0.8' 
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
print("1")
#s.sendall(b"hello, world")
#print("...")
#data = s.recv(1024)
#print(f"recieved message: ")

servoPIN = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 100)

def get_pwm_value():
        # try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        # pwm_value = response.json().get('pwm_values')
        # if 1000 <= pwm_value <= 2000:
        #     return pwm_value
        # else:
        #     print("PWM value out of range")
        #     return None

while True:
    p.start(2.5) # Initialization
    data = client_socket.recv(1024)
    pwm_string = data.decode('utf-8')
    pwm_values = list(map(float, pwm_string.split(',')))
    print("recieved pwm values:", pwm_values)
    SERVER_URL = ""
    
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        p.stop()
    except:
        GPIO.cleanup()