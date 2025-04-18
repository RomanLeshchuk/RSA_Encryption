"""
Contains server representation
"""

import socket
import threading
import hashlib
from generate_keys import generate_keys
from encryption import encrypt

class Server:
    """
    Represents server
    """

    def __init__(self, port: int) -> None:
        """
        Creates server
        """

        self.host = "127.0.0.1"
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.private_key = None
        self.public_key = None

    def start(self):
        """
        Starts server
        """

        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys ...
        self.private_key, self.public_key = generate_keys()

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f"New person has joined: {username}")
            self.username_lookup[c] = username
            self.clients.append(c)

            # send public key to the client
            c.send(str(self.public_key).encode())

            # encrypt the secret with the clients public key
            str_client_public = c.recv(1024).decode()
            client_public = tuple(int(x) for x in str_client_public.strip("()").split(","))
            encrypted_private = encrypt(str(self.private_key), client_public)

            # send the encrypted secret to a client
            c.send(encrypted_private.encode())

            threading.Thread(target=self.handle_client,args=(c,)).start()

    def broadcast(self, msg: str):
        """
        Sends message to all clients
        """

        encrypted_msg = encrypt(msg, self.public_key)
        msg_hash = hashlib.sha256(msg.encode()).hexdigest()
        total_msg = f"{msg_hash}:{encrypted_msg}".encode()

        for client in self.clients:
            client.send(total_msg)

    def handle_client(self, c: socket):
        """
        Handles message from client and sends it to all other clients
        """

        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
