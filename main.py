import pygame

import socket
import sys 

try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	print ("Socket successfully created")
except socket.error as err: 
	print ("socket creation failed with error %s" %(err))


port = 80

try: 
	host_ip = socket.gethostbyname('www.google.com') 
except socket.gaierror: 

	print ("there was an error resolving the host")
	sys.exit() 

s.connect((host_ip, port)) 

print ("the socket has successfully connected to google") 


pygame.init()

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick connected")

else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")


def joystick_to_pwm(value):
      scaled_value = value * 100
      normalized_value = scaled_value / 1000
      pwm_value = 1500 + (normalized_value * 5000)
      pwm_value = max(1000, min(2000, pwm_value))
      return int(pwm_value)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            axis_0 = joystick.get_axis(0)
            axis_1 = joystick.get_axis(1)
            axis_2 = joystick.get_axis(2)
            axis_3 = joystick.get_axis(3)
            
            axis_0_pwm_value = joystick_to_pwm(axis_0)
            axis_1_pwm_value = joystick_to_pwm(axis_1)
            axis_2_pwm_value = joystick_to_pwm(axis_2)
            axis_3_pwm_value = joystick_to_pwm(axis_3)
            print(f"Axis 0: {axis_0_pwm_value}, Axis 1: {axis_1_pwm_value}, Axis 2: {axis_2_pwm_value}, Axis 3: {axis_3_pwm_value}")

pygame.quit()