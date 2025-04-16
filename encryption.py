def encrypt(message, public_key):
    e, n = public_key
    l = []
    for x in message:
        l.append((ord(x)**e)%n)
    return ', '.join(str(s) for s in l)

def decode(coded_msg, private_key):
    d, n = private_key
    codes = map(int, coded_msg.split(', '))
    decoded = ''
    for x in codes:
        decoded += chr((x**d)%n)
    return decoded