from secrets import randbits
from math import sqrt

def is_prime(x):
    for i in range(2, int(sqrt(x))):
        if x % i == 0:
            return False
    return True

def generate_large_prime(bits):
    while True:
        candidate = randbits(bits)
        if is_prime(candidate):
            return candidate

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x, y = extended_gcd(b % a, a)
    return (g, y - (b // a) * x, x)
        
def generate_keys():
    p = generate_large_prime(bits=32)
    q = generate_large_prime(bits=16)

    n = p*q

    fi = (p-1)*(q-1)

    # generaing e
    while True:
        # if e is prime then it is "взаємо просте" with fi \_0_/
        e = generate_large_prime(bits=16)
        if e != q:
            break

    # looking for d by Evklid algo
    d = (extended_gcd(e, fi)[1]%fi+fi)%fi

    private = (d, n)
    public = (e, n)

    return private, public
