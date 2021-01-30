import random


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Coords):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y


def visualize(gw, gh):
    for r in range(gh - 1, -1, -1):
        s = "|"
        for c in range(0, gw):
            s = s + str(r) + str(c) + "|"
        print(s)


def main():
    print(random.choices(["True", "False"], (.2, .8), k=10))


if __name__ == "__main__":
    main()
