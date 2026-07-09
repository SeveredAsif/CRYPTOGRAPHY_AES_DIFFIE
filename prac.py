import random  
IV_rand = [random.randint(0, 255) for _ in range(16)]
print(IV_rand)