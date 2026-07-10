import socket
import struct
import pickle
import hashlib
from aes import cbc_mode_decrypt

HOST = "127.0.0.1"
PORT = 12345

def recv_exact(conn, n):
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(min(65536, n - len(buf)))
        if not chunk:
            raise ConnectionError("socket closed before full message received")
        buf += chunk
    return buf

def recv_msg(conn):
    header = recv_exact(conn, 8)
    (length,) = struct.unpack(">Q", header) #sender jei length ta concat kore header e pathaise, oita unpack kori n er val paite
    return recv_exact(conn, length)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

data = client.recv(1024).decode()
p, g, A = map(int, data.split(","))
print("p =", p)
print("g =", g)
print("A =", A)

from diffie_hellman import diffie_chooseB
B, K_b, _ = diffie_chooseB(p, g)
client.sendall(str(B).encode())

shared_secret = pow(A, K_b, p)
print(f"Shared secret: {shared_secret}")

data = client.recv(1024).decode()
print(data) # Alice ready print
client.sendall("Bob ready to transmit too".encode())


raw = recv_msg(client)
payload = pickle.loads(raw)
filename = payload["filename"]
orig_len = payload["orig_len"]
solution = payload["solution"]

key0 = hashlib.sha256(str(shared_secret).encode()).digest()
print(f"bob key: {key0[:16].hex()}")


import time 
start = time.perf_counter()
decrypted_blocks = cbc_mode_decrypt(solution, key0)   
enc_time = time.perf_counter() - start
print(f"Decryption took {enc_time:.3f}s")



flat_hex = [b for block in decrypted_blocks for b in block]
file_bytes = bytes(int(b, 16) for b in flat_hex)[:orig_len]

out_name = "received_" + filename
with open(out_name, "wb") as f:
    f.write(file_bytes)

print(f"Saved decrypted file as {out_name} ({len(file_bytes)} bytes)")

client.close()