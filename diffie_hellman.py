import random 

import time 

# It returns (x^y) % p
def power(x, y, p):
    
    # Initialize result
    res = 1; 
    
    # Update x if it is more than or
    # equal to p
    x = x % p; 
    while (y > 0):
        
        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p;


        y = y>>1; 
        x = (x * x) % p;
    
    return res;


def miillerTest(d, n):
    
    a = 2 + random.randint(1, n - 4);

    x = power(a, d, n);

    if (x == 1 or x == n - 1):
        return True;
    while (d != n - 1):
        x = (x * x) % n;
        d *= 2;

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

    return False;

def isPrime( n, k):
    
    if (n <= 1 or n == 4):
        return False;
    if (n <= 3):
        return True;

    d = n - 1;
    while (d % 2 == 0):
        d //= 2;

    for i in range(k):
        if (miillerTest(d, n) == False):
            return False;

    return True;

import random
random.seed(42) 


def diffie_chooseB(p,g,k=128):
    start_time = time.perf_counter()
    private_key = random.randint(2**(k-1),2**(k)-1) 
    B = pow(g,private_key,p)
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return B,private_key,execution_time

def diffie_choose_pgA(k=128):
    start_time = time.perf_counter()

    q = random.randint(2**(k-2),2**(k-1)-1)
    p = 2 * q + 1
    while(not (isPrime(p,4) and isPrime(q,4))):
        q = random.randint(2**(k-2),2**(k-1)-1)
        p = 2 * q + 1

    g = random.randint(2,p)

    while(pow(g,(p-1)//2,p)==1 or pow(g,(p-1)//q,p)==1):
        g = random.randint(2,p)

    private_key = random.randint(2**(k-1), 2**k - 1)
    #private_key = random.randint(2**127,2**128-1) 
    A = pow(g,private_key,p)
    #print(g)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return p,g,A,private_key,execution_time

def benchmark_dh():
    print(f"{'k':>5} | {'A time (s)':>12} | {'B time (s)':>12} | {'shared key time (s)':>20}")
    for k in [128, 192, 256]:
        A_times, B_times, S_times = [], [], []
        for _ in range(5):
            p, g, A, Ka, A_time = diffie_choose_pgA(k)
            B, Kb, B_time = diffie_chooseB(p, g, k)

            t0 = time.perf_counter()
            s1 = pow(B, Ka, p)
            s2 = pow(A, Kb, p)
            assert s1 == s2, "shared secrets don't match!"
            S_time = time.perf_counter() - t0

            A_times.append(A_time)
            B_times.append(B_time)
            S_times.append(S_time)

        print(f"{k:>5} | {sum(A_times)/5:>12.6f} | {sum(B_times)/5:>12.6f} | {sum(S_times)/5:>20.6f}")

if __name__ == "__main__":
    benchmark_dh()