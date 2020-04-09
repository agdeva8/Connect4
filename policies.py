from connect4Game import Game
import random
import copy


class RandomPolicy:
    def __init__(d, gameObj):
        d.__gameObj = gameObj

    def getAction(d, s):
        # print("in policy get action of Ai")
        while True:
            actionList = d.__gameObj.actions(d.__gameObj.state())
            action = random.choice(actionList)
            return action


class MiniMaxRaw:
    def __init__(d, gameObj):
        d.__gameObj = gameObj

    def recursion(d, s):
        player, boardConfig = s
        print("Rec Player is {}".format(player))
        if d.__gameObj.isEnd(s):
            print("Rec utility is {}".format(d.__gameObj.utility(s)))
            return (d.__gameObj.utility(s), None)

        actionList = d.__gameObj.actions(s)
        print(actionList)
        # print("player is {}".format(player))
        # candidates = [
        #     (d.recursion(
        #         copy.deepcopy(d.__gameObj.succ(s, action)))[0], action)
        #     for action in d.__gameObj.actions(s)
        # ]

        candidates = []
        for action in d.__gameObj.actions(s):
            print(action)
            candidates.append((d.recursion(copy.deepcopy(d.__gameObj.succ(s, action)))[0], action))


        # if len(vmmValues) == 0:
        #     return d.__gameObj.utility(s)

        if player == +1:
            return max(candidates)
        elif player == -1:
            return min(candidates)

    def getAction(d, s):
        s = d.__gameObj.state()
        player, boadConfig = s

        # print("Player is {}".format(player))
        # succP, succB = d.__gameObj.succ(s, d.__gameObj.actions(s)[0])
        # print("succ player is {}".format(succP))

        utility, action = d.recursion(copy.deepcopy(s))
        # print("utility is {}, action is {}".format(utility, action))
        return action


def main():
    game = Game(3, 4)
    AIPolicy = RandomPolicy(game)
    minMaxPolicy = MiniMaxRaw(game)
    game.gameLoop((game, minMaxPolicy))
    # game.gameLoop((game, AIPolicy))
    # game.gameLoop((AIPolicy, game))
    # game.gameLoop((AIPolicy, AIPolicy))


main()
