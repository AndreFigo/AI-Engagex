import sys
import numpy as np
import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt


def plot_training(matrix):
    playerscores = matrix[:, :4]
    actions = matrix[:, 4:]
    for i in range(actions.shape[0]):
        s = np.sum(actions[i, :])
        actions[i, :] = actions[i, :] / s * 100
    plt.figure()
    plt.plot(playerscores)
    plt.legend(["player " + str(i + 1) for i in range(4)])
    plt.show(block=False)
    plt.figure()
    plt.plot(actions)
    action_names = [
        "move_north",
        "move_south",
        "move_east",
        "move_west",
        "collect",
        "commit",
        "seed",
        "attack",
        "kill",
        "flee",
        "share",
    ]
    plt.legend(action_names)
    plt.show(block=False)


if __name__ == "__main__":
    file_name = sys.argv[1]
    arr = np.loadtxt(file_name, delimiter=",")
    print("arr shape: ", arr.shape)
    plot_training(arr)
    input()
