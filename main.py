import pygame
import socket
import time
#this code actually works so far (convert joystick values to pwm)
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print ("Socket successfully created")


host_ip = '10.0.0.58' 
port = 8080

s.bind((host_ip, port))
s.listen(1)
client_socket, client_address = s.accept()
print ("the socket has successfully connected")

try:
    pygame.init()
    print("...")
except:
    print("canceled")
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print(joystick_count)
if joystick_count == 0:
    print("No joystick connected")

else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")


def joystick_to_pwm(value):
    pwm_value = 1500 + (value * 500)
    #   scaled_value = value * 100
    #   normalized_value = scaled_value / 1000
    #   pwm_value = 1500 + (normalized_value * 5000)
    pwm_value = max(1000, min(2000, pwm_value))
      
    return int(pwm_value)


running = True
while running:
    #client_socket, client_address = s.accept()
    message = str(input("enter your message here: "))
    client_socket.sendall(message.encode('utf-8'))

    # msg = str(input("enter your message here: "))
    # msg = msg.encode()
    # print("input recieved")
    # s.send(msg)
    # print("message sent to client")



'''
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

             # for pwm_value in range(1000, 2000):
             #     if ((pwm_value > 2000) and (pwm_value < 1000)):
             #        joystick_to_pwm()
             #     elif ((pwm_value < 2000) and (pwm_value > 1000)):
             #          pass
             #     else:
             #         pass

             print(f"Axis 0: {axis_0_pwm_value}, Axis 1: {axis_1_pwm_value}, Axis 2: {axis_2_pwm_value}, Axis 3: {axis_3_pwm_value}")
             pwm_value = {
                 joystick_to_pwm(axis_0),
                 joystick_to_pwm(axis_1),
                 joystick_to_pwm(axis_2),
                 joystick_to_pwm(axis_3),
             }
            
             s.sendall(str(pwm_value).encode('utf-8'))
            
            
             time.sleep(1)
'''
            
pygame.quit()
s.close()