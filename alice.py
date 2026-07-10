import socket
from diffie_hellman import diffie_choose_pgA

HOST = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")

conn, addr = server.accept()
print("Connected by", addr)




p,g,A,K_a = diffie_choose_pgA()

    

message = f"{p},{g},{A}"
conn.sendall(message.encode())


data = conn.recv(1024).decode()
B = int(data)

print("Received B =", B)


shared_secret = pow(B,K_a,p)
print(f"Shared secret: {shared_secret}") 

message = "Alice ready to transmit"
conn.sendall(message.encode())
data = conn.recv(1024).decode()
print(data) 


#while(1):
    
from aes import user_encrypt
import pickle

solution = user_encrypt("Lets Go!Wooojooooooooooo",str(shared_secret))
# conn.sendall(solution)
conn.sendall(pickle.dumps(solution.res))
# data = conn.recv(1024).decode()
# print(data) 


conn.close()
server.close()