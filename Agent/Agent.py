import random


class Agent:

    def __init__(self):
        self.n = 5

    def nextAction(self, percept):
        return random.randint(0, self.n)

