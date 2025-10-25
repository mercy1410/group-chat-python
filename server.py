import socket
from Crypto.Cipher import AES
import base64
import threading

# AES encryption key (16 bytes)
key = b'ThisIsA16ByteKey'

def encrypt(message):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = message + (16 - len(message) % 16) * ' '
    return base64.b64encode(cipher.encrypt(padded.encode()))

def decrypt(ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext)).decode()
    return decrypted.rstrip()

clients = []

# Broadcast message to all clients except sender
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(encrypt(message))
            except:
                clients.remove(client)

# Handle each client connection
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = decrypt(data)
            print(message)  # Display on server
            broadcast(message, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"Connection closed: {addr}")

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen(5)
print("Server listening on port 5555...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr)).start()
