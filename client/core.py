import socket
from typing import List

from common import send, build_message, DIRECTION, CASE_FUNCTION


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getNewPos(self, dir: str):
        if dir == "N":
            self.y -= 1
        elif dir == "S":
            self.y += 1
        elif dir == "E":
            self.x += 1
        elif dir == "W":
            self.x -= 1


class Group:
    def __init__(self, id: int, size: int, pos: Pos):
        self.id = id
        self.size = size
        self.pos = pos


class Team:
    name = "Squid Game"

    def __init__(self):
        self.id = None
        self.idGroup = 0
        self.groups: List[Group] = []
        self.basePos = None
        self.canPlay = True

    @property
    def activeGroups(self):
        return list(filter(lambda g: (g.size > 0), self.groups))

    def getGroupById(self, id: int) -> Group:
        return list(filter(lambda g: g.id == id, self.groups))[0]

    def getGroupByPos(self, pos: Pos):
        return list(filter(lambda g: g.pos.x == pos.x and g.pos.y == pos.y, self.groups))[0]

    def getGroupsPos(self) -> List[Pos]:
        return [g.pos for g in self.groups]

    def addGroup(self, size: int, pos: Pos):
        self.idGroup += 1
        self.groups.append(Group(self.idGroup, size, pos))

    def killGroup(self, group: Group):
        self.groups = list(filter(lambda g: g.id != group.id, self.groups))

    def initialize(self, id: int, pos: Pos):
        self.id = id
        self.basePos = pos

    def joinServer(self):
        send(connection, build_message("JOIN", [Team.name]))

    def move(self, id_group: int, amount: int, dir: DIRECTION):
        pass

    def stay(self):
        send(connection, build_message("STAY", []))


class Case:
    def __init__(self, pos: Pos):
        self.pos: Pos = pos
        self.group: Group = None
        self.function: CASE_FUNCTION = None
        self.linkedTo: Case = None
        self.blockedUntilTurn = -1

    def setFunction(self, function: CASE_FUNCTION):
        self.function = function

    def setGroup(self, group: Group):
        self.group = group

    def makePortalWith(self, otherCase):
        self.function = CASE_FUNCTION.TELEPORT
        self.linkedTo = otherCase

        otherCase.function = CASE_FUNCTION.TELEPORT
        otherCase.linkedTo = self

    def removePortal(self, otherCase):
        self.function = None
        self.linkedTo = None

        otherCase.function = None
        otherCase.linkedTo = None


class Map:
    def __init__(self):
        self.size = None
        self.grid = None

    def initialize(self, size: int):
        self.size = size
        self.grid = [[Case(Pos(x, y)) for x in range(size)] for y in range(size)]

    def getCase(self, pos: Pos) -> Case:
        return self.grid[pos.x][pos.y]

    def inMap(self, pos: Pos) -> bool:
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size


class Game:
    nbTurn = 0
    teams = []
    map = Map()
    baseGroupSize: int
    eventProba: int

    def addTeam(self, team: Team):
        self.teams.append(team)

    def removeTeam(self, team: Team):
        self.teams.remove(team)

    def getTeam(self, id: int) -> Team:
        return list(filter(lambda t: t.id == id, self.teams))[0]


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(('127.0.0.1', 5000))
team = Team()
game = Game()
