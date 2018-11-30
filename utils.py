import numpy as np
import matplotlib.pyplot as plt

def int_input(prompt='Please enter a number: '):
    while True:
        n = input(prompt)
        try:
            n = int(n)
        except (ValueError, TypeError):
            print('You must enter an integer!')
        else:
            break

    return n

def is_valid_int(n):
    try:
        n = int(n)
    except (ValueError, TypeError):
        return False

    return True

def tell_everyone(players, string):
    for player in players:
        player.tell(string)

def create_plot(players, scores, path):
    # Convert to numpy array
    scores = np.asarray(scores)

    for col in range(scores.shape[1]):
        cs = np.cumsum(scores[:, col])
        plt.plot(cs)

    labels = ['Player ' + str(i) + ' (' + players[i].__class__.__name__ + ')' for i in range(len(players))]
    plt.legend(labels)
    plt.savefig(path)
    plt.show()