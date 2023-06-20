from dataclasses import dataclass
from typing import Tuple
import os
import pickle
import shelve
import socket

PERSISTENCE_SOCKET_PATH = "/tmp/telusuri_dbe_socket"


@dataclass
class Barrel:
    __slots__ = ["start_range", "end_range"]
    start_range: int
    end_range: int

    def getRange(self) -> Tuple[int, int]:
        return (self.start_range, self.end_range)


# Plan: Barrel key will be the starting wordID
class PersistenceStorage:

    __slots__ = ["sock", "db"]

    def __init__(self, db_path: str) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(PERSISTENCE_SOCKET_PATH)
        self.db: shelve.Shelf[Barrel] = shelve.open(
            db_path, writeback=True, protocol=pickle.HIGHEST_PROTOCOL)

    # Plan: receive barrel from socket
    def addBarrel(self):
        pass

    # TODO What should we return ?
    # Plan: get barrel (pickle object), then send to socket
    def getBarrel(self, dbId: str):
        buf = pickle.dumps(self.db[dbId])
        self.sock.send(buf)

    def closeBarrel(self):
        self.db.close()
        self.sock.close()
        try:
            os.unlink(PERSISTENCE_SOCKET_PATH)
        except OSError:
            if os.path.exists(PERSISTENCE_SOCKET_PATH):
                os.remove(PERSISTENCE_SOCKET_PATH)

    def run(self):
        while True:
            try:
                # TODO Create message class
                # Plan: Header send size of incoming packet
                buf = self.sock.recv(1024)
                if buf:
                    pass  # TODO
                continue

            except KeyboardInterrupt:
                self.closeBarrel()
            except OSError:
                self.closeBarrel()  # TODO ???
