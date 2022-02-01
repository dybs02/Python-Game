"""
Main file used for starting the game.
"""
from game import Game

if __name__ == '__main__':
    g = Game()

    while True:
        g.game_loop()
