import Environment.Agent as ea
import random

Action = ['Forward', 'TurnLeft', 'TurnRight', 'Shoot', 'Grab', 'Climb']
Orientation = ['North', 'East', 'South', 'West']


class Coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Coords):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y


class Percept:

    def __init__(self, st, br, gl, bu, sc, tr):
        self.stench = st
        self.breeze = br
        self.glitter = gl
        self.bump = bu
        self.scream = sc
        self.isTerminated = tr
        # self.reward = rw

    def pprint(self):
        print("stench::", self.stench)
        print("breeze::", self.breeze)
        print("glitter::", self.glitter)
        print("bump::", self.bump)
        print("scream::", self.scream)
        print("isTerminated::", self.isTerminated)
        # print("reward:::", self.reward)


class Environment:

    def __init__(self, gw, gh, pitProb, allowClimbWithoutGold):
        self.gridWidth = gw
        self.gridHeight = gh
        self.pP = pitProb
        self.allowClimbWOGold = allowClimbWithoutGold
        self.Agent = ea.Agent()
        self.pitLocations = []
        self.terminated = False
        self.wumpusAlive = True
        # set location of gold
        self.goldLocation = self.randomLocationExceptOrigin()
        # set location of Wumpus
        self.wumpusLocation = self.randomLocationExceptOrigin()

    def randomLocationExceptOrigin(self):
        x = random.randint(0, self.gridHeight - 1)
        y = random.randint(0, self.gridWidth - 1)
        if x == 0 and y == 0:
            return self.randomLocationExceptOrigin()
        else:
            return Coords(x, y)

    def initailize(self):
        # add pits
        for r in range(self.gridHeight):
            for c in range(self.gridWidth):
                if c == 0 and r == 0:
                    break
                if random.choices([1, 0], weights=(self.pP, 1 - self.pP), k=1)[0] == 1:
                    self.pitLocations.append(Coords(r, c))
        print("no of pits:::", len(self.pitLocations))

        return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), 0

    def isPitAt(self, loc):
        return True if loc in self.pitLocations else False

    def isAgentAt(self, loc):
        return self.Agent.location == loc

    def isWumpusAt(self, loc):
        return self.wumpusLocation == loc

    def isGoldAt(self, loc):
        return self.goldLocation == loc

    def isGlitter(self):
        return self.goldLocation == self.Agent.location

    def killAttemptSuccessful(self):
        wumpusInLineOfFire = False
        if self.Agent.orientation == "West":
            wumpusInLineOfFire = self.Agent.location.y == self.wumpusLocation.y and self.Agent.location.x > self.wumpusLocation.x
        if self.Agent.orientation == "East":
            wumpusInLineOfFire = self.Agent.location.y == self.wumpusLocation.y and self.Agent.location.x < self.wumpusLocation.x
        if self.Agent.orientation == "North":
            wumpusInLineOfFire = self.Agent.location.x == self.wumpusLocation.x and self.Agent.location.y < self.wumpusLocation.y
        if self.Agent.orientation == "South":
            wumpusInLineOfFire = self.Agent.location.x == self.wumpusLocation.x and self.Agent.location.y > self.wumpusLocation.y
        print("wumpusInLineOfFire:::", wumpusInLineOfFire)
        return self.Agent.hasArrow and self.wumpusAlive and wumpusInLineOfFire

    def adjacentCells(self, loc):
        adCells = []
        # to the left
        if loc.x > 0:
            adCells.append(Coords(loc.x - 1, loc.y))

        # to the right
        if loc.x < self.gridWidth - 1:
            adCells.append(Coords(loc.x + 1, loc.y))

        # to the North
        if loc.y < self.gridHeight - 1:
            adCells.append(Coords(loc.x, loc.y + 1))

        # to the South
        if loc.y > 0:
            adCells.append(Coords(loc.x, loc.y - 1))

        return adCells

    def isPitAdjacent(self, loc):
        adCells = self.adjacentCells(loc)
        return any(l in adCells for l in self.pitLocations)

    def isWumpusAdjacent(self, loc):
        adCells = self.adjacentCells(loc)
        return True if loc in adCells else False

    def isBreeze(self):
        return self.isPitAdjacent(self.Agent.location)

    def isStench(self):
        return self.isWumpusAdjacent(self.Agent.location) or self.isWumpusAt(self.Agent.location)

    def visualize(self):

        wsym = 'W' if self.wumpusAlive else 'w'
        for r in range(self.gridHeight - 1, -1, -1):
            s = "|"
            for c in range(0, self.gridWidth):
                stA = "A" if self.isAgentAt(Coords(c, r)) else " "
                stP = "P" if self.isPitAt(Coords(c, r)) else " "
                stG = "G" if self.isGoldAt(Coords(c, r)) else " "
                stW = wsym if self.isWumpusAt(Coords(c, r)) else " "
                s = s + stA + stP + stG + stW + "|"
                # s = s + str(c) + str(r) + "|"
            print(s)

    def applyAction(self, ac):
        print("action to apply:::" + ac)
        if self.terminated:
            return Percept(False, False, False, False, False, True, 0)
        if ac == 'Forward':
            oldLoc = self.Agent.location
            self.Agent.forward(self.gridWidth, self.gridHeight)
            death = (self.isWumpusAt(self.Agent.location) and self.wumpusAlive) or self.isPitAt(self.Agent.location)
            self.Agent.isAlive = not death
            return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), oldLoc == self.Agent.location, False,
                           death), -1 if not death else -1001

        if ac == 'TurnLeft':
            self.Agent.turnLeft()
            return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), -1

        if ac == 'TurnRight':
            self.Agent.turnRight()
            return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), -1

        if ac == 'Grab':
            self.Agent.hasGold = self.isGlitter()
            return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), -1

        if ac == 'Climb':
            if (self.Agent.hasGold or self.allowClimbWOGold) and self.Agent.location == Coords(0, 0):
                return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, True), \
                       999 if self.Agent.hasGold else -1
            else:
                return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), -1

        if ac == 'Shoot':
            if self.Agent.hasArrow and self.killAttemptSuccessful():
                self.Agent.hasArrow = False
                self.wumpusAlive = False
                return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, True, False), -1
            else:
                self.Agent.hasArrow = False
                return Percept(self.isStench(), self.isBreeze(), self.isGlitter(), False, False, False), -1
