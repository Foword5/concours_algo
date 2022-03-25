from math import sqrt

from client.core import team, connection, Team, Pos, game
from client.events import handleEvent
from common import recv, parse_message, ERROR, DIRECTION


def start():
    global center
    team.joinServer()
    gamemap = game.map
    state = "center"
    x2list = []

    while True:
        resp = recv(connection)
        if not resp:
            continue

        command, *params = parse_message(resp)
        if not team.id:
            if command == "NEWGAME":
                (size, k, i, x, y, baseGroupSize, eventProba) = list(map(int, params))
                center = Pos(size / 2, size / 2)

                game.baseGroupSize = baseGroupSize
                game.eventProba = eventProba

                gamemap.initialize(size)
                team.initialize(i, Pos(x, y))
                team.addGroup(game.baseGroupSize, Pos(x, y))
                game.teams.append(team)

                for i in range(k - 1):
                    otherTeam = Team()
                    otherTeam.id = i + 1
                    game.teams.append(otherTeam)

        if command == "NEWTURN":
            n = int(params[0])
            eventsHandled = 0
            while eventsHandled < n:
                resp = recv(connection)
                command, *params = parse_message(resp)
                if command == "EVENT":
                    handleEvent(int(params[0]), params[3:])
                    if int(params[0]) == 2:
                        state = "rush"
                        x2list.append(Pos(int(params[1]), int(params[2])))
                    eventsHandled += 1
            if state == "center":

                closegroup = team.activeGroups[0]
                for group in team.activeGroups:
                    if group.pos.x == center.x and group.pos.y == center.y:
                        state = "idle"
                    elif sqrt((closegroup.pos.x - center.x) ** 2 + (closegroup.pos.y - center.y) ** 2) > sqrt(
                            (group.pos.x - center.x) ** 2 + (group.pos.y - center.y) ** 2):
                        closegroup = group

                if center.x > closegroup.pos.x:
                    team.move(closegroup.id, closegroup.size, DIRECTION.EAST)
                elif center.x < closegroup.pos.x:
                    team.move(closegroup.id, closegroup.size, DIRECTION.WEST)
                elif center.y > closegroup.pos.y:
                    team.move(closegroup.id, closegroup.size, DIRECTION.NORTH)
                elif center.y < closegroup.pos.y:
                    team.move(closegroup.id, closegroup.size, DIRECTION.SOUTH)

            elif state == "rush":
                if x2list[0] is None:
                    state = "center"
                    continue

                x2 = x2list[0]
                closegroup = team.activeGroups()[0]
                for group in team.activeGroups():
                    if group.pos.x == x2.x and group.pos.y == x2.y:
                        state = "center"
                        group.size *= 2
                    elif sqrt((closegroup.pos.x - x2.x) ** 2 + (closegroup.pos.y - x2.y) ** 2) > sqrt(
                            (group.pos.x - x2.x) ** 2 + (group.pos.y - x2.y) ** 2):
                        closegroup = group

                if x2.x > closegroup.pos.x:
                    team.move(closegroup.id, closegroup.size, DIRECTION.EAST)
                elif x2.x < closegroup.pos.x:
                    team.move(closegroup.id, closegroup.size, DIRECTION.WEST)
                elif x2.y > closegroup.pos.y:
                    team.move(closegroup.id, closegroup.size, DIRECTION.NORTH)
                elif x2.y < closegroup.pos.y:
                    team.move(closegroup.id, closegroup.size, DIRECTION.SOUTH)

            else:
                team.stay()

        elif command == "ERROR":
            ERROR(params[0])

        game.nbTurn += 1


if __name__ == '__main__':
    start()
