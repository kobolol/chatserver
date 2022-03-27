import socket
from threading import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4956

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} hat den ChatServer verlassen!".encode("utf-8"))
            stop = True

def main():
    print(f"Server is running under {HOST}:{PORT}...")
    while True:
        client, addr = server.accept()
        print(f"Connect to {addr}")

        client.send("NICK".encode("utf-8"))

        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname is {nickname}")

        client.send("**You are now connected**\n".encode("utf-8"))
        broadcast(f"{nickname} ist dem ServerChat beigetreten \n".encode("utf-8"))

        thread = Thread(target=handle_connection, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
