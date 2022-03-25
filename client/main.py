from client.core import team, connection, gameMap, Team, Pos
from client.events import handleEvent
from common import recv, parse_message, ERROR


def start():
    team.joinServer()

    while True:
        resp = recv(connection)
        if not resp:
            continue

        command, *params = parse_message(resp)
        if not team.id:
            if command == "NEWGAME":

                (size, k, i, x, y) = list(map(int, params))

                gameMap.initialize(size)
                team.initialize(i, Pos(x, y))

                gameMap.teams.append(team)
                for i in range(k - 1):
                    gameMap.teams.append(Team())
            else:
                continue

        if command == "NEWTURN":
            (n) = params
        elif command == "EVENT":
            (type, x, y, params) = params
            handleEvent(type, x, y, params)
        elif command == "ERROR":
            ERROR(params[0])


if __name__ == '__main__':
    start()
