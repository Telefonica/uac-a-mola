from multiprocessing.connection import Client

class Agent:
    def __init__(self, binary, address, port, password):
        self.address = (address, port)
        self.password = password
        self.binary = binary

    def send_forbidden(self, key):
        conn = Client(self.address, authkey=self.password)
        conn.send([self.binary, key])
        conn.close()
