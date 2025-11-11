import socket
import threading

HEADER_SIZE = 64
PORT = 5050
SERVER = "192.168.10.143"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

DISCONNECT_MSG = "!disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# TODO: separate this mess into separate methods.
# TODO: use stdout and flush().

def send(username: str, msg: str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = f"{str(msg_length)},{username}".encode(FORMAT)
    send_length += b' ' * (HEADER_SIZE - (len(send_length) + len(username)))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            header = client.recv(HEADER_SIZE).decode(FORMAT)

            if header:
                header = header.strip().split(",")
                msg_length = header[0]
                msg_length = int(msg_length)
                
                msg = client.recv(msg_length).decode(FORMAT)
                print(f"[{header[1]}] {msg}")
        except:
            print("[ERROR] Error during receiving.")

thread = threading.Thread(target=receive, daemon=True)
thread.start()

username = input("Write your username: ")
inp = input("Write your message: ")
while inp != "-1":
    send(username, inp)
    inp = input("Write your message: ")

send(username, "!disconnect")
