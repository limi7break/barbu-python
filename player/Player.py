import random, consts
from utils import int_input
from Card import Card

class Player():

    def __init__(self, ID, name=''):
        self.ID    = ID
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

    def tell(self, string):
        # To avoid checking for HumanPlayer every time
        return

    def notify_card(self, ID, card):
        # To avoid checking for HumanPlayer every time
        return

class HumanPlayer(Player):

    def __init__(self, ID, name=''):
        super().__init__(ID, name)

    def tell(self, string):
        '''
            This method is used for telling something to a HumanPlayer.

            For example, a CLIHumanPlayer would just print the string out to the console,
            while a GUIHumanPlayer would write it to a specific area of the GUI.
        '''
        raise NotImplementedError('[-] This needs to be implemented by your HumanPlayer class!')

    def notify_card(self, ID, card):
        '''
            This method is called by a Game object whenever a card is played.
            It's necessary to be able to show which cards have been played
            by the other players, because State updates are received only
            when it's the player's turn.

            It's only present in HumanPlayer, because virtual players don't care
            about cards played by the other players: all the information needed
            to choose the next action is contained in the State received through
            get_next_action.

            Human players can override this method to display the played cards
            the way they want.
        '''
        raise NotImplementedError('[-] This needs to be implemented by your HumanPlayer class!')

class RandomPlayer(Player):
    '''
        A completely random player: always chooses all
        actions randomly.
    '''
    def __init__(self, ID, name=''):
        super().__init__(ID, name)

    def get_next_game(self):
        return random.choice([game_num for game_num, played in self.played_games.items() if not played])

    def get_trump_suit(self):
        return random.choice(Card.suits)

    def get_starting_value(self):
        return random.choice(list(range(13)))

    def get_next_action(self, state):
        return random.choice(state.playable_actions)