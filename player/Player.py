import random, consts
from utils import int_input
from Card import Card

class Player():

    def __init__(self, name=""):
        self.name  = name
        self.hand  = []
        self.played_games = {game_num: False for game_num in range(consts.NUM_GAMES)}

    def get_next_game(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

    def get_trump_suit(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

    def get_starting_value(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')        

    def get_next_action(self, state):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

class RandomPlayer(Player):
    '''
        A completely random player: always chooses all
        actions randomly.
    '''
    def get_next_game(self):
        return random.choice([game_num for game_num, played in self.played_games.items() if not played])

    def get_trump_suit(self):
        return random.choice(Card.suits)

    def get_starting_value(self):
        return random.choice(list(range(13)))

    def get_next_action(self, state):
        return random.choice(state.playable_actions)