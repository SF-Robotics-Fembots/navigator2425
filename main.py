import pygame
import socket
import time, json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

host_ip = '192.168.1.68'#'10.0.0.87'
port = 8080

s.bind(('', port)) #host_ip
s.listen(1)
client_socket, client_address = s.accept()
print ("Socket successfully connected")

try:
    pygame.init()
    print("Pygame initialized")
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

dead_zone = 0.1
def apply_dead_zones(value, threshold):
    if abs(value) < threshold:
        return 0
    return value

#the actual conversion from percentage to pwm
def joystick_to_pwms(value):
    pwm_value = 1500 + (value * 5) #1000-2000
    pwm_value = max(1000, min(2000, pwm_value))
    return int(pwm_value)

#*50 or *100 then scale it after
#if dont get value for 0 move according to that
slow_mode_ratio = 0 #0.5
rotation_sensitivity_adj = 0.25

running = True
while running:
    for event in pygame.event.get():
        print(event)
        print("...")
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            axis_x = joystick.get_axis(0) #left and right
            axis_y = joystick.get_axis(1) #forward and back
            axis_r = joystick.get_axis(2) #rotation (yaw)
            axis_z = joystick.get_axis(3) #vertical (up and down)
            #print(f"Raw Values: Axis x: {axis_x}, Axis y: {axis_y}, Axis r:{axis_r}, Axis z: {axis_z}")

            if pygame.joystick.Joystick(0).get_button(5): slow_mode_ratio = 0 #stop
            if pygame.joystick.Joystick(0).get_button(2): slow_mode_ratio = 1 #fast
            if pygame.joystick.Joystick(0).get_button(3): slow_mode_ratio = 0.5 #slow

            axis_x = axis_x*slow_mode_ratio
            axis_y = axis_y*slow_mode_ratio
            axis_r = axis_r*slow_mode_ratio
            axis_z = axis_z*slow_mode_ratio
            
            #x_speed = (pygame.joystick.Joystick(0).get_axis(0))
            #x_speed = x_speed*slow_mode_ratio

            # y_speed = (pygame.joystick.Joystick(0).get_axis(1))
            # y_speed = y_speed*slow_mode_ratio

            # r_speed = (pygame.joystick.Joystick(0).get_axis(2))
            # r_speed = r_speed*slow_mode_ratio

            # z_speed = (pygame.joystick.Joystick(0).get_axis(3))
            # z_speed = z_speed*slow_mode_ratio
            #print(f"Speed: X: {axis_x}, Y: {axis_y}, R: {axis_r}, Z: {axis_z}")
        
            axis_x = apply_dead_zones(axis_x, dead_zone)
            axis_y = apply_dead_zones(axis_y, dead_zone)
            axis_r = apply_dead_zones(axis_r, dead_zone)
            axis_z = apply_dead_zones(axis_z, dead_zone)
            #print(f"Dead Zone: Axis X: {axis_x}, Axis Y: {axis_y}, Axis R:{axis_r}, Axis Z: {axis_z}")

            axis_x_scale = int((axis_x)*100) 
            axis_y_scale = int((axis_y)*-100)
            axis_r_scale = int((axis_r)*-100)
            axis_z_scale = int((axis_z)*-100) #flip verticals
            #print(f"Scale Values: Axis X: {axis_x_scale}, Axis Y: {axis_y_scale}, Axis R:{axis_r_scale}, Axis Z: {axis_z_scale}")
            #axis_r_scale = int(round(axis_r_scale * rotation_sensitivity_adj))

            #mulptply by 10% create a vairbale rotation_adjustment
            # rotation_adjustment = int(round(axis_y_scale*0.20))
            # axis_r_scale = axis_r_scale + rotation_adjustment
            
            thruster_5 = axis_z_scale #left vertical
            thruster_4 = axis_z_scale #right vertical
            thruster_3 = axis_x_scale #middle
            thruster_2 = axis_y_scale - axis_r_scale #left horizontal
            thruster_1 = axis_y_scale + axis_r_scale #right horizontal

            thruster_percent_ideal = [thruster_5, thruster_4, thruster_3, thruster_2, thruster_1]
            #print("Thruster Percent Ideal;", thruster_percent_ideal)

            #if the thruster values are less than 100, then it will pass the if statment
            if max(abs(thruster_1), abs(thruster_2)) > 100:
                ratio = (100/max(abs(thruster_1), abs(thruster_2))) #if the thruster value is over 100, then the ratio will take the value back down to 100
                new_thruster_1_b = int(thruster_1 * ratio)
                new_thruster_2_b = int(thruster_2 * ratio)
            else:
                new_thruster_1_b = thruster_1
                new_thruster_2_b = thruster_2
                #print("New Thruster 1 and 2 B: ", new_thruster_1_b, new_thruster_2_b)

            thruster_5_b = thruster_5
            thruster_4_b = thruster_4
            thruster_3_b = thruster_3
            thruster_2_b = new_thruster_2_b
            thruster_1_b = new_thruster_1_b
            thruster_1_b = new_thruster_1_b

            thruster_percent_max = [thruster_5_b, thruster_4_b, thruster_3_b, thruster_2_b, thruster_1_b]
            #print("Thruster Percent Max: ", thruster_percent_max)
            
            power_total = sum(abs(num) for num in thruster_percent_max) #taking absolute value of each thruster and adding it together to get total amount of power
            #print("Power Total: ", power_total)

            power_max = 275 #max amount of power we can use (percentage) ex: 800% (mr. grindstaff) test 250, was 800, 650
            power_ratio = 1
            if (power_total > power_max):
                power_ratio = power_max/power_total
            #print("Power Ratio: ", power_ratio)

            thruster_5_c = thruster_5_b * power_ratio
            thruster_4_c = thruster_4_b * power_ratio
            thruster_3_c = thruster_3_b * power_ratio
            thruster_2_c = thruster_2_b * power_ratio
            thruster_1_c = thruster_1_b * power_ratio

            final_percentage = [thruster_5_c, thruster_4_c, thruster_3_c, thruster_2_c, thruster_1_c]
            #print("Final Percentage: ", final_percentage)

            thruster_pwm_values = [joystick_to_pwms(percentage) for percentage in final_percentage]
            #print("Thruster PWM Values: ", thruster_pwm_values)

            thruster_values = [joystick_to_pwms(thruster_5_c), joystick_to_pwms(thruster_4_c), joystick_to_pwms(thruster_3_c), joystick_to_pwms(thruster_2_c), joystick_to_pwms(thruster_1_c)]
            #print("Thruster Values: ", thruster_values)

            print(f"PWM Thruster Values: ", thruster_pwm_values)

            json_data = json.dumps(thruster_values)
            client_socket.sendall(json_data.encode('utf-8'))

            time.sleep(0.001)

pygame.quit()
client_socket.close()