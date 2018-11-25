from Atout import Atout
from Player import RandomPlayer, HumanCLIPlayer

players = [RandomPlayer() for _ in range(3)]
players.append(HumanCLIPlayer())

atout = Atout(players)
scores = atout.play()

print('Scores:', scores)