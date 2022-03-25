import struct
from enum import Enum
from typing import List, Any


class CASE_FUNCTION:
    NONE = 0
    MULT = 2
    TELEPORT = 3
    BLOCK = 4
    PASS_TURN = 5
    PASS_NEXT_TURN = 6
    DIVIDE = 7


class DIRECTION(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


def ERROR(msg: str) -> None:
    print("[ERROR] {}".format(msg))
    exit()


def send(socket, message):
    socket.send(struct.pack("i", len(message)) + message)


def recv(socket):
    try:
        size = struct.unpack("i", socket.recv(struct.calcsize("i")))[0]
        data = ""
        while len(data) < size:
            msg = socket.recv(size - len(data))
            if not msg:
                ERROR("Problème lors de la reception du socket {}".format(socket))
            data += msg.decode()
        return data
    except:
        exit()


def build_message(key: str, params: List[Any]) -> bytes:
    msg = key + "|" + '|'.join(map(str, params))
    print("[LOG/MSG] " + msg)
    return msg.encode()


def parse_message(msg: str) -> List[str]:
    return [s.upper() for s in msg.split("|")]
