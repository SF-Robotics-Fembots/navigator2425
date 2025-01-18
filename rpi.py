import socket

host_ip = '10.0.0.97' 
port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host_ip, port))
    s.sendall(b"hello, world")
    data = s.recv(1024)

print(f"received{data!r}")

running = True
while running:
