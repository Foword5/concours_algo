from client.core import team, connection, Team, Pos, game
from client.events import handleEvent
from common import recv, parse_message, ERROR


def start():
    team.joinServer()
    gamemap = game.map

    while True:
        resp = recv(connection)
        if not resp:
            continue

        command, *params = parse_message(resp)
        if not team.id:
            if command == "NEWGAME":
                (size, k, i, x, y, baseGroupSize, eventProba) = list(map(int, params))

                game.baseGroupSize = baseGroupSize
                game.eventProba = eventProba

                gamemap.initialize(size)
                team.initialize(i, Pos(x, y))

                gamemap.teams.append(team)
                for i in range(k - 1):
                    gamemap.teams.append(Team())
            else:
                continue

        if command == "NEWTURN":
            (n) = params
            eventsHandled = 0
            while eventsHandled < n:
                if command == "EVENT":
                    (type, *params) = params
                    handleEvent(type, params)
                    eventsHandled += 1

        elif command == "ERROR":
            ERROR(params[0])


if __name__ == '__main__':
    start()
