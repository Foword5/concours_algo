from client.core import game, Pos
from common import ERROR, CASE_FUNCTION


def handleEvent(type: int, *params: str):
    if type == 0:
        handle_0(*params)
    elif type == 1:
        handle_1(int(params[0]))
        pass
    elif type == 2:
        handle_2(Pos(int(params[0]), int(params[1])))
    elif type == 3:
        handle_3(Pos(int(params[0]), int(params[1])), Pos(int(params[2]), int(params[3])))
    elif type == 4:
        handle_4(Pos(int(params[0]), int(params[1])), int(params[2]))
    elif type == 5:
        handle_5(Pos(int(params[0]), int(params[1])))
    elif type == 6:
        handle_6(Pos(int(params[0]), int(params[1])))
    elif type == 7:
        handle_7(Pos(int(params[0]), int(params[1])))
    else:
        ERROR("-".join(params) + str(type))


def handle_0(id_team: int, id_group: int, amount: int, dir: str):
    team = game.getTeam(id_team)
    group = team.getGroup(id_group)

    newPos = Pos(*group.pos).getNewPos(dir)

    team.splitGroup(group, amount, newPos)


def handle_1(id_team: int):
    team = game.getTeam(id_team)


def handle_2(pos: Pos):
    game.map.getCase(pos).function = CASE_FUNCTION.MULT


def handle_3(firstPos: Pos, secondPos: Pos):
    firstCase = game.map.getCase(firstPos)
    secondCase = game.map.getCase(secondPos)
    firstCase.makePortalWith(secondCase)


def handle_4(pos: Pos, time: int):
    game.map.getCase(pos).blockedUntilTurn = game.nbTurn + time


def handle_5(pos: Pos):
    game.map.getCase(pos).function = CASE_FUNCTION.PASS_TURN


def handle_6(pos: Pos):
    game.map.getCase(pos).function = CASE_FUNCTION.PASS_NEXT_TURN


def handle_7(pos: Pos):
    game.map.getCase(pos).function = CASE_FUNCTION.DIVIDE
