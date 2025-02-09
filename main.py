import pygame
import socket
import time, json
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


def joystick_to_pwm(value):
    pwm_value = 1500 + (value * 500)
    pwm_value = max(1000, min(2000, pwm_value))
      
    return int(pwm_value)

def calculate_rotation_thrusters():
    pass
    # return int(added_values)
    #*50 or *100 then scale it after
    
    # if int(axis_1 == 0):
    #     pass
    # elif int(axis_2 == -1):
    #     pass
    # elif int(axis_2 == 1):
    #     pass
    # else:
    #     pass
#if dont get value for 0 move according to that

running = True
while running:
    global axis_0, axis_1, axis_2
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

            # axis_0_calculate = calculate_rotation_thrusters(axis_0)
            # axis_1_calculate = calculate_rotation_thrusters(axis_1)
            # axis_2_calculate = calculate_rotation_thrusters(axis_2)
            # print(f"Axis 0: {axis_0_calculate}, Axis 1: {axis_1_calculate}, Axis 2: {axis_2_calculate}")

            axis_0 = int((axis_0)*100)
            axis_1 = int((axis_1)*100)
            axis_2 = int((axis_2)*100)
            added_values = int(axis_1 + axis_2 + axis_3)
            print("x, y, and r:", added_values)
            
            
            axis_0_pwm_value = joystick_to_pwm(axis_0)
            axis_1_pwm_value = joystick_to_pwm(axis_1)
            axis_2_pwm_value = joystick_to_pwm(axis_2)
            axis_3_pwm_value = joystick_to_pwm(axis_3)

            # with client_socket:
            print("............")

            pwm_values = {
                'x': axis_0_pwm_value,
                'y': axis_1_pwm_value,
                'r': axis_2_pwm_value,
                'v': axis_3_pwm_value
            }

            # pwm_string = ','.join(map(str, pwm_values))
            # client_socket.sendall(pwm_string.encode('utf-8'))\
            json_data = json.dumps(pwm_values)
            client_socket.sendall(json_data.encode('utf-8'))
            

            print(f"Axis 0: {axis_0}, Axis 1: {axis_1}, Axis 2:{axis_2}, Axis 3: {axis_3}")
            #print(json_data)
            print(f"Axis 0: {axis_0_pwm_value}, Axis 1: {axis_1_pwm_value}, Axis 2: {axis_2_pwm_value}, Axis 3: {axis_3_pwm_value}")

            time.sleep(0.005)


pygame.quit()
client_socket.close()