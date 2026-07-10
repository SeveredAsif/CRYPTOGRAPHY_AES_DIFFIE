# Python3 program Miller-Rabin primality test
import random 

import time 


# Utility function to do
# modular exponentiation.
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

        # y must be even now
        y = y>>1; # y = y/2
        x = (x * x) % p;
    
    return res;

# This function is called
# for all k trials. It returns
# false if n is composite and 
# returns false if n is
# probably prime. d is an odd 
# number such that d*2<sup>r</sup> = n-1
# for some r >= 1
def miillerTest(d, n):
    
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4);

    # Compute a^d % n
    x = power(a, d, n);

    if (x == 1 or x == n - 1):
        return True;

    # Keep squaring x while one 
    # of the following doesn't 
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n;
        d *= 2;

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

    # Return composite
    return False;

# It returns false if n is 
# composite and returns true if n
# is probably prime. k is an 
# input parameter that determines
# accuracy level. Higher value of 
# k indicates more accuracy.
def isPrime( n, k):
    
    # Corner cases
    if (n <= 1 or n == 4):
        return False;
    if (n <= 3):
        return True;

    # Find r such that n = 
    # 2^d * r + 1 for some r >= 1
    d = n - 1;
    while (d % 2 == 0):
        d //= 2;

    # Iterate given number of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False;

    return True;

# Driver Code
# Number of iterations
# k = 4; 

# print("All primes smaller than 100: ");
# for n in range(1,100):
#     if (isPrime(n, k)):
#         print(n , end=" ");
import random
random.seed(42) 


def diffie_chooseB(p,g,k=128):
    start_time = time.perf_counter()
    private_key = random.randint(2**(k-1),2**(k)-1) 
    B = pow(g,private_key,p)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    #print(f"The B calculation took {execution_time:.6f} seconds to execute.")
    return B,private_key,execution_time

def diffie_choose_pgA(k=128):
    start_time = time.perf_counter()

    q = random.randint(2**(k-2),2**(k-1)-1)
    p = 2 * q + 1
    while(not (isPrime(p,4) and isPrime(q,4))):
        q = random.randint(2**(k-2),2**(k-1)-1)
        p = 2 * q + 1
    #print(p)

    g = random.randint(2,p)

    while(pow(g,(p-1)//2,p)==1 or pow(g,(p-1)//q,p)==1):
        g = random.randint(2,p)

    private_key = random.randint(2**(k-1), 2**k - 1)
    #private_key = random.randint(2**127,2**128-1) 
    A = pow(g,private_key,p)
    #print(g)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    #print(f"The A calculation took {execution_time:.6f} seconds to execute.")
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