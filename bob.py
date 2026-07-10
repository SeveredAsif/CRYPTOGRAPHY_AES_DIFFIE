import socket

HOST = "127.0.0.1"
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))


data = client.recv(1024).decode()

p, g, A = map(int, data.split(","))

print("p =", p)
print("g =", g)
print("A =", A)

from diffie_hellman import diffie_chooseB
B,K_b = diffie_chooseB(p,g)

client.sendall(str(B).encode())

shared_secret = pow(A,K_b,p)

print(f"Shared secret: {shared_secret}") 


data = client.recv(1024).decode()
print(data)
message = "Bob ready to transmit too"
client.sendall(message.encode())
 
from aes import user_decrypt
import pickle

data = client.recv(100000)

solution = pickle.loads(data)
# solution = client.recv(1024)
plain_text = user_decrypt(solution,str(shared_secret))

print(plain_text)

client.close()