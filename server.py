import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast --- To send the message to multiple clients
def broadcaste(message):
    for client in clients:
        client.send(message)

# Handle --- To handle the individual connections to the client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcaste(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# Receive --- To listen and accept new clients or connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connection with {str(address)} has been established !")
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is :{nickname} ")
        broadcaste(f"{nickname} connected to the server !\n".encode("utf-8"))
        client.send("Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# receive() is calling the handle() which inturn calls the broadcast()
print("Server running.....")
receive()