import socket

HOST = '192.168.1.72'
PORT = '9090'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True: 
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    message = communication_socket.recv(1024).decode('utf-8')
    if not message: 
        break
    # Convert the data string back to a list
    data_list = list(map(float, message.split(',')))

    # Process the data as needed
    print("Received Data List:", data_list)

    communication_socket.send(f"Got your message! Thank you!".encode('utf-8'))
    communication_socket.close()

