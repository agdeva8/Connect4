from connect4Game import Game
import random


class RandomPolicy:
    def __init__(d, gameObj):
        d.__gameObj = gameObj

    def getAction(d):
        # print("in policy get action of Ai")
        while True:
            actionList = d.__gameObj.actions(d.__gameObj.state())
            action = random.choice(actionList)
            return action


def main():
    game = Game(3, 7)
    AIPolicy = RandomPolicy(game)
    game.gameLoop((game, AIPolicy))


main()
