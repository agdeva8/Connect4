from gym import spaces
from gym.utils import seeding
import numpy as np
from backendFunctions import GameEnv

nRows = 6
nCols = 7


class Connect4Env():
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # super(Connect4Env, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # # Example when using discrete actions:
        self.action_space = spaces.Discrete(nCols)
        # self.observation_space = spaces.Discrete(nRows * nCols * 3)

        self.gameEnv = GameEnv()

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        board = np.zeros((nRows, nCols))
        player = 1

        self.state = {
            "board": board,
            "player": player,
            "nRows": nRows,
            "nCols": nCols
        }

        stateList = self.gameEnv.state2List(self.state)
        return stateList

    def step(self, action):
        # assert self.gameEnv.isValidAction(self.state, action)

        self.gameEnv.succ(self.state, action)
        reward = self.gameEnv.utility(self.state)
        done = self.gameEnv.isEnd(self.state)

        stateList = self.gameEnv.state2List(self.state)
        return stateList, reward, done, {}

    def render(self, mode='human', close=False):
        # print("Render Function Called")
        pass
