from secrets import randbits
from random import choice
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
    return (g, ((y - (b // a) * x)%b+b)%b, x)

def gcd(a,b):
    if b == 0:
        return a
    return gcd(b, a % b)

def generate_keys(bits=(8,16)):
    p = generate_large_prime(bits=bits[0])
    q = generate_large_prime(bits=bits[1])

    n = p*q

    fi = (p-1)*(q-1)

    pairs = {}
    for x in range(fi//2, fi//4, -1):
        if gcd(fi, x) == 1:
            d = extended_gcd(x,fi)[1]
            if d != x:
                pairs[x] = d

    e = choice(list(pairs.keys()))
    d = pairs[e]

    private = (d, n)
    public = (e, n)

    return private, public