import random
from utils import int_input

class Player():

    def get_next_action(self, state):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

class RandomPlayer(Player):
    '''
        A completely random player: always chooses all
        actions randomly.
    '''
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
    def get_next_action(self, state):
        hand = state.hands[state.current_player]
        playable_cards = [hand[i] for i in state.playable_actions]
        
        print('Hand: {}'.format(hand))
        print('Cards played in last trick: {}'.format(state.trick_cards))
        print('Trump suit: {}'.format(state.trump_suit))
        print('Possible actions: {}'.format(playable_cards))
        s = '                   '
        for i in state.playable_actions:
            s += '({})   '.format(i)
        print(s)

        action = -1
        while action not in state.playable_actions:
            action = int_input('Please insert the action number: ')

        return action