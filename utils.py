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

def create_plot(scores, path):
    # Convert to numpy array
    scores = np.asarray(scores)

    for col in range(scores.shape[1]):
        cs = np.cumsum(scores[:, col])
        plt.plot(cs)

    plt.legend(['0', '1', '2', '3'])
    plt.savefig(path)
    plt.show()