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


def normalize(value, input_min=-1, input_max=1, output_min=-100, output_max=100):
     return ((value - input_min) * (output_max - output_min) / (input_max - input_min)) + output_min

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
            print(f"Axis 0: {axis_0}, Axis 1: {axis_1}, Axis 2: {axis_2} Axis 3: {axis_3}")

            axis_0_normalized = normalize(axis_0)
            axis_1_normalized = normalize(axis_1)
            axis_2_normalized = normalize(axis_2)
            axis_3_normalized = normalize(axis_3)
            print(f"Axis 0: {axis_0_normalized}, Axis 1: {axis_1_normalized}, Axis 2: {axis_2_normalized}, Axis 3: {axis_3_normalized}")


pygame.quit()