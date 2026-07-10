# Python3 program Miller-Rabin primality test
import random 
import math
import time 
def find_prime_factors(n):
    res = []
    for i in range(math.floor(math.sqrt(n))):
        if(not isPrime(i,4)):
            continue 
        if(n%i==0):
            res.append(i)
            break
    return res 

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
random.seed = 42 


def diffie_chooseB(p,g):
    start_time = time.perf_counter()
    private_key = random.randint(2**127,2**128-1) 
    B = pow(g,private_key,p)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The B calculation took {execution_time:.6f} seconds to execute.")
    return B,private_key

def diffie_choose_pgA():
    start_time = time.perf_counter()

    q = random.randint(2**126,2**127-1)
    p = 2 * q + 1
    while(not isPrime(p,4)):
        q = random.randint(2**126,2**127-1)
        p = 2 * q + 1
    print(p)

    g = random.randint(2,p)

    while(pow(g,(p-1)//2,p)==1 or pow(g,p-1//q,p)==1):
        g = random.randint(2,p)


    private_key = random.randint(2**127,2**128-1) 
    A = pow(g,private_key,p)
    #print(g)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The A calculation took {execution_time:.6f} seconds to execute.")
    return p,g,A,private_key