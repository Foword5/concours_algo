import socket
from typing import List

from common import send, build_message, DIRECTION


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Group:
    def __init__(self, size: int, pos: Pos):
        self.size = size
        self.pos = pos


class Team:
    name = "Squid Game"

    def __init__(self):
        self.id = None
        self.groups: List[Group] = []
        self.basePos = None

    @property
    def activeGroups(self):
        return list(filter(lambda g: (g.size > 0), self.groups))

    def initialize(self, id: int, pos: Pos):
        self.id = id
        self.basePos = pos

    def joinServer(self):
        send(connection, build_message("JOIN", [Team.name]))

    def move(self, id_group: int, amount: int, dir: DIRECTION):
        pass
    
    def stay(self):
        send(connection, build_message("STAY"))


class Map:
    def __init__(self):
        self.size = None
        self.grid = []

    def initialize(self, size: int):
        self.size = size
        self.grid = [[Case(Pos(x, y)) for x in range(size)] for y in range(size)]


class Case:
    def __init__(self, pos: Pos):
        self.pos = pos


class Game:
    nbTours = 0
    teams = []

    def addTeam(self, team: Team):
        self.teams.append(team)

    def removeTeam(self, team: Team):
        self.teams.remove(team)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(('127.0.0.1', 5000))
team = Team()
gameMap = Map()
