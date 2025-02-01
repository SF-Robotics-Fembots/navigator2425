import pygame
import socket
import time
#this code actually works so far (convert joystick values to pwm)
#this code works (sending and recieving messages back and forth)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print ("Socket successfully created")


host_ip = '10.0.0.8' 
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


# def joystick_to_pwm(value):
#     pwm_value = 1500 + (value * 500)
#     pwm_value = max(1000, min(2000, pwm_value))
      
#     return int(pwm_value)


running = True
while running:
    #client_socket, client_address = s.accept()
    #message = str(input("enter your message here: "))
    #client_socket.sendall(message.encode('utf-8'))

    # msg = str(input("enter your message here: "))
    # msg = msg.encode()
    # print("input recieved")
    # s.send(msg)
    # print("message sent to client")
    

    for event in pygame.event.get():
        print("----")
        print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            axis_0 = joystick.get_axis(0)
            axis_1 = joystick.get_axis(1)
            axis_2 = joystick.get_axis(2)
            axis_3 = joystick.get_axis(3)
        
            # axis_0_pwm_value = joystick_to_pwm(axis_0)
            # axis_1_pwm_value = joystick_to_pwm(axis_1)
            # axis_2_pwm_value = joystick_to_pwm(axis_2)
            # axis_3_pwm_value = joystick_to_pwm(axis_3)

            # with client_socket:
            print("............")

            pwm_values = {
                'x':joystick.get_axis(0),
                'y':joystick.get_axis(1),
                'r': joystick.get_axis(2),
                'v':joystick.get_axis(3)
            }

            pwm_values = {
        
            }
            pwm_string = ','.join(map(str, pwm_values))
            client_socket.sendall(pwm_string.encode('utf-8'))
            
            print(f"Axis 0: {axis_0}, Axis 1: {axis_1}, Axis 2: {axis_2}, Axis 3: {axis_3}")

            time.sleep(0.1)


pygame.quit()
s.close()

# joystick_to_pwm(axis_0),
                # joystick_to_pwm(axis_1),
                # joystick_to_pwm(axis_2),
                # joystick_to_pwm(axis_3),