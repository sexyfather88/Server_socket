import socket, threading


class createClient(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self._conn = conn
        self._addr = addr

    def send(self, data):

        try:
            self._conn.sendall(data)

        except socket.error as msg:
            self.close()

    def close(self):
        self._conn.close();
        print
        'Disconnected by', self._addr

    def run(self):

        while True:
            data = self._conn.recv(1024)
            if not data:
                self.close()
                break


            if str(data, encoding="utf-8").startswith('exit'):
                self.close()
                break

            self.send(data)


_socket = socket.socket()
_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                   1)  ## cuz kernel didn't release connectioin of TCP and keep status: "TIME_WAIT"
_socket.bind(('', 5000))
_socket.listen(5)

while True:
    conn, addr = _socket.accept()
    print('@@@')
    print
    'Connected by', addr
    createClient(conn, addr).start()
