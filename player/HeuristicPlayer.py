from player.Player import Player

class HeuristicPlayer(Player):
    '''
        A player that plays according to some expert-made
        heuristics. It implements a different action logic
        for every game.
    '''
    def __init__(self, ID, name=''):
        super().__init__(ID, name)