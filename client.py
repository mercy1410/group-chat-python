import socket
from Crypto.Cipher import AES
import base64
import threading

# AES encryption key (must match server)
key = b'ThisIsA16ByteKey'

# Roll number → Name mapping
roll_to_name = {
    "14": "Mercy",
    "21": "Nivashini",
    "25": "Santhiya",
    "12": "Atchaya",
    "13": "Manjula",
    "23": "Poorani"
}

# AES Encryption / Decryption functions
def encrypt(message):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = message + (16 - len(message) % 16) * ' '
    return base64.b64encode(cipher.encrypt(padded.encode()))

def decrypt(ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext)).decode()
    return decrypted.rstrip()

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# Enter roll number
roll_number = input("Enter your roll number: ")
username = roll_to_name.get(roll_number, roll_number)  # fallback to roll number if not in mapping

# Thread to receive messages from server
def receive_messages(client):
    while True:
        try:
            data = client.recv(1024)
            print("\n" + decrypt(data))
        except:
            break

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# Send messages
while True:
    msg = input()
    client.send(encrypt(f"{username}: {msg}"))  