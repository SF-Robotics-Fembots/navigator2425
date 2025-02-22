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
print ("Socket successfully connected")

try:
    pygame.init()
    print("...")
except:
    print("Canceled")
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print(joystick_count)
if joystick_count == 0:
    print("No joystick connected")

else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")

#from raw values straight to pwm (no other conversions)
def joystick_to_pwm(value):
    pwm_value = 1500 + (value * 500) #1000-2000
    pwm_value = max(1000, min(2000, pwm_value))
    return int(pwm_value)

#the actual conversion from percentage to pwm
def joystick_to_pwms(value):
    pwm_value = 1500 + (value * 5) #1000-2000
    pwm_value = max(1000, min(2000, pwm_value))
    return int(pwm_value)

#*50 or *100 then scale it after
#if dont get value for 0 move according to that

running = True
while running:
    for event in pygame.event.get():
        print(event)
        print("...")
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            axis_r = joystick.get_axis(2)
            axis_z = joystick.get_axis(3)

            axis_x_scale = int((axis_x)*100) 
            axis_y_scale = int((axis_y)*100)
            axis_r_scale = int((axis_r)*100)
            axis_z_scale = int((axis_z)*100)

            thruster_5 = axis_z_scale
            thruster_4 = axis_z_scale
            thruster_3 = axis_y_scale
            thruster_2 = axis_x_scale - axis_r_scale
            thruster_1 = axis_x_scale + axis_r_scale

            thruster_percent_ideal = [thruster_5, thruster_4, thruster_3, thruster_2, thruster_1]

            thruster_5_b = thruster_5
            thruster_4_b = thruster_4
            thruster_3_b = thruster_3
            thruster_2_b = thruster_2
            thruster_1_b = thruster_1

            #if the thruster values are less than 100, then it will pass the if statment

            if max(thruster_1, thruster_2) > 100:
                ratio = int(100/max(thruster_1, thruster_2)) #if the thruster value is over 100, then the ratio will take the value back down to 100
                new_thruster_1_b = thruster_1 * ratio
                new_thruster_2_b = thruster_2 * ratio
            else:
                pass
            # print(thruster_1_b, thruster_2_b)

            thruster_percent_max = [thruster_5_b, thruster_4_b, thruster_3_b, thruster_2_b, thruster_1_b]
            
            power_total = sum(abs(num) for num in thruster_percent_max) #taking absolute value of each thruster and adding it together to get total amount of power

            power_max = 200 #max amount of power we can use (percentage) ex: 200%
            power_ratio = power_max/power_total

            thruster_5_b = power_ratio * thruster_5_b
            thruster_4_b = power_ratio * thruster_4_b
            thruster_3_b = power_ratio * thruster_3_b
            thruster_2_b = power_ratio * thruster_2_b
            thruster_1_b = power_ratio * thruster_1_b

            final_percentage = [thruster_5_b, thruster_4_b, thruster_3_b, thruster_2_b, thruster_1_b]

            thruster_pwm_values = [joystick_to_pwms(percentage) for percentage in final_percentage]

            axis_x_pwm_value = joystick_to_pwm(axis_x)
            axis_y_pwm_value = joystick_to_pwm(axis_y)
            axis_r_pwm_value = joystick_to_pwm(axis_r)
            axis_z_pwm_value = joystick_to_pwm(axis_z)

            # print(f"Raw Values: Axis 0: {axis_x}, Axis 1: {axis_y}, Axis 2:{axis_r}, Axis 3: {axis_z}")
            # print(f"Thruster %:", thruster_percent_ideal)
            # print(f"Power Total:", power_total)
            # print(f"Final %:", final_percentage)
            print(f"PWM Thruster Values: ", thruster_pwm_values)
            # print(f"PWM Values: Axis 0: {axis_x_pwm_value}, Axis 1: {axis_r_pwm_value}, Axis 2: {axis_r_pwm_value}, Axis 3: {axis_z_pwm_value}")

            pwm_values = {
                'x': axis_x_pwm_value,
                'y': axis_y_pwm_value,
                'r': axis_r_pwm_value,
                'v': axis_z_pwm_value
            }

            thruster_values = {
                    'thruster_1': thruster_1_b,
                    'thruster_2': thruster_2_b,
                    'thruster_3': thruster_3_b,
                    'thruster_4': thruster_4_b,
                    'thruster_5': thruster_5_b
                }
            
            print(thruster_values)

            json_data = json.dumps(pwm_values)
            client_socket.sendall(json_data.encode('utf-8'))

            # json_data = json.dumps(thruster_values)
            # client_socket.sendall(json_data.encode('utf-8'))

            time.sleep(0.005)


pygame.quit()
client_socket.close()