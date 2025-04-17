"""
Contains encrypt and decrypt functions
"""

def encrypt(message, public_key):
    """
    Encrypts message with public key
    """

    e, n = public_key
    l = []
    for x in message:
        l.append((ord(x)**e)%n)

    return ",".join(str(s) for s in l)

def decrypt(coded_msg, private_key):
    """
    Decrypts message with private key
    """

    d, n = private_key
    codes = map(int, coded_msg.split(","))
    decoded = ""
    for x in codes:
        decoded += chr((x**d)%n)

    return decoded
