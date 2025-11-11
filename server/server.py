import socket
import threading

HEADER_SIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!disconnect"

FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []

# TODO: Separate all this mess into separate methods.

def send(connection, username: str, msg: str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = f"{str(msg_length)},{username}".encode(FORMAT)
    send_length += b' ' * (HEADER_SIZE - (len(send_length) + len(username)))
    connection.send(send_length)
    connection.send(message)

def handle_client(conn, addr):
    print(f"[CONNECTION] New connection, user {addr} connected.")

    connected = True
    connections.append(conn)
    while (connected):
        header = conn.recv(HEADER_SIZE).decode(FORMAT)

        if header:
            header = header.strip().split(",")
            msg_length = header[0]
            try:
                msg_length = int(msg_length)
            except:
                print(f"[ERROR] Invalid message received from user {addr}, closing connection.")
                connected = False
            
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
                print(f"[CONNECTION] Connection closed {addr}")
                break

            print(f"[{header[1]}] {msg}")
            for connection in connections:
                send(connection, header[1], msg)
    conn.close()
    connections.remove(conn)

def start_server():
    server.listen()
    print(f"[LISTENING] Listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start_server()


