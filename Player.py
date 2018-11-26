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

    def get_next_action(self, state):
        return random.choice(state.playable_actions)

class HeuristicPlayer(Player):
    '''
        A player that plays according to some expert-made
        heuristics. It implements a different action logic
        for every game.
    '''
    pass

class MCPlayer(Player):
    '''
        A player that makes use of MCTS (Monte Carlo Tree Search)
        and UCT (Upper Confidence Bound applied to Trees) algorithms
        for action selection.

    '''
    pass

class HumanCLIPlayer(Player):
    '''
        A human player that can play interactively
        and select actions via Command Line Interface.
    '''
    def get_next_game(self):
        available_games = [game_num for game_num, played in self.played_games.items() if not played]

        print('Games left:')
        [print('    {}: {}'.format(i, consts.GAMES[i].split('.')[1])) for i in available_games]
        print('Hand: {}'.format(self.hand))

        game = -1
        while game not in available_games:
            game = int_input('Please insert the game number: ')

        return game

    def get_trump_suit(self):
        print('Suits: {}'.format(Card.suits))

        suit = -1
        while suit not in range(len(Card.suits)):
            suit = int_input('Please insert the trump suit: ')

        return Card.suits[suit]

    def get_next_action(self, state):
        hand = state.hands[state.current_player]
        playable_cards = [hand[i] for i in state.playable_actions]
        
        print('Hand: {}'.format(hand))
        print('Cards played in last trick: {}'.format(state.trick_cards))
        print('Trump suit: {}'.format(state.trump_suit))
        print('Possible actions: {}'.format(playable_cards))
        s = '                   '
        for i in range(len(state.playable_actions)):
            s += '({})   '.format(i)
        print(s)

        action = -1
        while action not in range(len(state.playable_actions)):
            action = int_input('Please insert the action number: ')

        return state.playable_actions[action]