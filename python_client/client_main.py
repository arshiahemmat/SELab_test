import random
from base import BaseAgent, Action
from tools import *


class Agent(BaseAgent):

    def do_turn(self) -> Action:
        return execution_test(self)


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
