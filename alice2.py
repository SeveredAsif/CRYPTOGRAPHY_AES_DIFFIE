import socket
import struct
import pickle
import hashlib
import os
import sys
import time
from diffie_hellman import diffie_choose_pgA
from aes import cbc_mode_encrypt

HOST = "127.0.0.1"
PORT = 12345


def send_msg(conn, data: bytes):
    conn.sendall(struct.pack(">Q", len(data)) + data) #> diye big endian bujhi,msb first.Q hocche unsigned 8 byte integer  
    
# def recv_exact(conn, n):
#     buf = b""
#     while len(buf) < n:
#         chunk = conn.recv(min(65536, n - len(buf)))
#         if not chunk:
#             raise ConnectionError("socket closed before full message received")
#         buf += chunk
#     return buf

FILE_TO_SEND = sys.argv[1] if len(sys.argv) > 1 else "CSE406_Assignment_v2.pdf"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print("Connected by", addr)


p, g, A, K_a, _ = diffie_choose_pgA()
conn.sendall(f"{p},{g},{A}".encode())

data = conn.recv(1024).decode()
B = int(data)
print("Received B =", B)

shared_secret = pow(B, K_a, p)
print(f"Shared secret: {shared_secret}")

conn.sendall("Alice ready to transmit".encode())
data = conn.recv(1024).decode()  
print(data) #bob ready print

key0 = hashlib.sha256(str(shared_secret).encode()).digest()  
print(f"alice key: {key0[:16].hex()}")

with open(FILE_TO_SEND, "rb") as f:
    file_bytes = list(f.read())

print(f"Encrypting {FILE_TO_SEND} ({len(file_bytes)} bytes)...")
start = time.perf_counter()
solution = cbc_mode_encrypt(file_bytes, key0)
enc_time = time.perf_counter() - start
print(f"Encryption took {enc_time:.3f}s")

payload = {
    "filename": os.path.basename(FILE_TO_SEND),
    "orig_len": len(file_bytes),   
    "solution": solution,
}
send_msg(conn, pickle.dumps(payload))
print("File sent.")

conn.close()
server.close()