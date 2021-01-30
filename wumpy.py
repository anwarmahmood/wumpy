import Agent.NaiveAgent as aa
import Environment.Environment as ee


def runEpisode(e, a, p):
    # print(e.Agent.orientation)
    i = 0
    reward = 0
    while i < 50:
        p, r = e.applyAction(ee.Action[a.nextAction(p)])
        reward = reward + r
        # p = e.applyAction("Grab")
        print("Iteration:::", i + 1, ":::Reward received::", r)
        print("Total rewards:::", reward)
        e.visualize()
        e.Agent.pprint()
        print("-----------------------------------------------------------------------------")
        # p.pprint()
        i += 1
        if p.isTerminated:
            print("Total Iteration:::", i, ":::Total Rewards:::", reward)
            print("Game Over!", "Congrats." if e.Agent.isAlive else "Better luck next time.")
            break


def main():
    # print("initialize agent")
    a = aa.Agent()
    # print("initialize environment")
    e = ee.Environment(4, 4, 0.2, True)
    p, r = e.initailize()
    e.visualize()
    e.Agent.pprint()
    print("-----------------------------------------------------------------------------")
    # p.pprint()
    runEpisode(e, a, p)


if __name__ == "__main__":
    main()
