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

                game.teams.append(team)
                for i in range(k - 1):
                    game.teams.append(Team())

        if command == "NEWTURN":
            n = int(params[0])
            eventsHandled = 0
            while eventsHandled < n:
                resp = recv(connection)
                command, *params = parse_message(resp)
                if command == "EVENT":
                    handleEvent(int(params[0]), *(params[3:]))
                    eventsHandled += 1
            team.stay()

        elif command == "ERROR":
            ERROR(params[0])

        game.nbTurn += 1


if __name__ == '__main__':
    start()
