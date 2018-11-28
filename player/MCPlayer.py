from player.Player import Player

class MCPlayer(Player):
    '''
        A player that makes use of MCTS (Monte Carlo Tree Search)
        and UCT (Upper Confidence Bound applied to Trees) algorithms
        for action selection.

    '''
    def __init__(self, ID, name=''):
        super().__init__(ID, name)