import Environment.Environment as eea


class Agent:

    def __init__(self):
        self.location = eea.Coords(0, 0)
        self.orientation = eea.Orientation[1]
        self.hasGold = False
        self.hasArrow = True
        self.isAlive = True

    def turnLeft(self):
        # print("turnLeft:::Current Orientation is::" + self.orientation)
        newOrientationIndex = eea.Orientation.index(self.orientation) - 1
        self.orientation = eea.Orientation[newOrientationIndex if newOrientationIndex >= 0 else 3]
        # print("turnLeft:::New Orientation is::" + self.orientation)

    def turnRight(self):
        # print("turnRight:::Current Orientation is::" + self.orientation)
        newOrientationIndex = eea.Orientation.index(self.orientation) + 1
        self.orientation = eea.Orientation[newOrientationIndex if newOrientationIndex <= 3 else 0]
        # print("turnRight:::New Orientation is::" + self.orientation)

    def forward(self, gh, gw):
        if self.orientation == 'North':
            self.location = eea.Coords(self.location.x, min(self.location.y + 1, gh - 1))
        if self.orientation == 'South':
            self.location = eea.Coords(self.location.x, max(self.location.y - 1, 0))
        if self.orientation == 'East':
            self.location = eea.Coords(min(self.location.x + 1, gw - 1), self.location.y)
        if self.orientation == 'West':
            self.location = eea.Coords(max(self.location.x - 1, 0), self.location.y)

    def pprint(self):
        print("location::", self.location.y, self.location.y, "::orientation::", self.orientation, "::hasGold::",
              self.hasGold, "::hasArrow::", self.hasArrow, "::isAlive::", self.isAlive)
        # print("orientation::", self.orientation)
        # print("hasGold::", self.hasGold)
        # print("hasArrow::", self.hasArrow)
        # print("isAlive::", self.isAlive)
