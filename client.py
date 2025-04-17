"""
Contains client representation
"""

import socket
import threading
from generate_keys import generate_keys
from encryption import encrypt, decrypt

class Client:
    """
    Represents client
    """

    def __init__(self, server_ip: str, port: int, username: str) -> None:
        """
        Creates client
        """

        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.s = None
        self.server_public_key = None
        self.server_private_key = None

    def init_connection(self):
        """
        Creates connection between client and server
        """

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs
        private, public = generate_keys()

        # exchange public keys
        str_server_public = self.s.recv(1024).decode()
        self.server_public_key = tuple(int(x) for x in str_server_public.strip("()").split(","))
        self.s.send(str(public).encode())

        # receive the encrypted secret key
        str_server_private_encrypted = self.s.recv(1024).decode()
        str_server_private = decrypt(str_server_private_encrypted, private)
        self.server_private_key = tuple(int(x) for x in str_server_private.strip("()").split(","))

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        """
        Handles received messages
        """

        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key
            decrypted_msg = decrypt(message, self.server_private_key)

            print(decrypted_msg)

    def write_handler(self):
        """
        Sends messages
        """

        while True:
            message = input()

            # encrypt message with the secrete key
            encrypted_msg = encrypt(f"{self.username}: {message}", self.server_public_key)

            self.s.send(encrypted_msg.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, input("Enter your name: "))
    cl.init_connection()
