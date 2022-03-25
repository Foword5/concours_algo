import socket


def connect():
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.connect(('vps.teroaz.me', 5000))
    return connexion


def game():
    connexion = connect()

    while (True):
        print("Connecté !")


if __name__ == '__main__':
    game()
