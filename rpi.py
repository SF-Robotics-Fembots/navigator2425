import socket
import requests
import RPi.GPIO as GPIO
import time

host_ip = '10.0.0.97' 
port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host_ip, port))
    s.sendall(b"hello, world")
    data = s.recv(1024)

print(f"received{data!r}")

PWM_PIN = 18
FREQUENCY = 100
SERVER_URL = ""

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, FREQUENCY)
pwm.start(0)

def get_pwm_value():
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        pwm_value = response.json().get('pwm_vlaue')
        if 1000 <= pwm_value <= 2000:
            return pwm_value
        else:
            print("PWM value out of range")
            return None
    except requests.RequestsException as e:
        print(f"Error fetching pwm values")
        return None

def convert_to_duty_cycle(pwm_value):
    return (pwm_value - 1000) / 10

try:
    while True:
        pwm_value = get_pwm_value()
        if pwm_value is not None:
            duty_cycle = convert_to_duty_cycle(pwm_value)
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"set duty cycle to {duty_cycle}%")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    pwm.stop()
    GPIO.cleanup()
