import consts
from copy import deepcopy
from utils import tell_everyone
from Card import get_trick_winner
from player.Player import HumanPlayer

class State():
    def __init__(self, game, players, first_player, trump_suit=None):
        '''
            Missing suits is a dictionary of 4 lists (one for every suit).
            Each list has 4 boolean entries (one for every player).
            If an entry is True, it means that player has ran out of
            cards of that suit.
        '''
        missing_suits = {'♥': [False for _ in range(consts.NUM_PLAYERS)],
                         '♦': [False for _ in range(consts.NUM_PLAYERS)],
                         '♣': [False for _ in range(consts.NUM_PLAYERS)],
                         '♠': [False for _ in range(consts.NUM_PLAYERS)]}

        self.game = game
        self.current_player = first_player
        self.first_player = first_player
        self.hands = [deepcopy(player.hand) for player in players]
        self.trick_cards = []
        self.played_cards = [] if game != 'Domino' else {'♥': [], '♦': [], '♣': [], '♠': []}
        self.missing_suits = missing_suits
        self.highest = {'♥': 12, '♦': 12, '♣': 12, '♠': 12}
        self.trump_suit = trump_suit
        self.playable_actions = []
        self.scores = [0 for _ in range(consts.NUM_PLAYERS)]
        self.terminal = False

    def __str__(self):
        '''
            For debugging.
        '''
        return '''
    [State]
    game: {}
    current_player: {}
    first_player: {}
    hands[0]: {}
    hands[1]: {}
    hands[2]: {}
    hands[3]: {}
    trick_cards: {}
    played_cards: {}
    missing_suits['♥']: {}
                 ['♦']  {}
                 ['♣']  {}
                 ['♠']  {}
    highest: {}
    trump_suit: {}
    playable_actions: {}
    scores: {}
    terminal: {}
    '''.format(self.game, self.current_player, self.first_player,
               self.hands[0], self.hands[1], self.hands[2],
               self.hands[3], self.trick_cards, self.played_cards,
               self.missing_suits['♥'], self.missing_suits['♦'],
               self.missing_suits['♣'], self.missing_suits['♠'],
               self.highest, self.trump_suit, self.playable_actions,
               self.scores, self.terminal)

    def __repr__(self):
        return __str__(self)

class Game():
    '''
        Class that allows the impementation of different games with different rules
        and scores by extending it.

        The play() method is the main game loop.

        The get_next_state() method calculates the next state based on the
        action chosen by the player. It's reused across every game except for
        Domino, which overrides the method because the state change is very
        different.

        The get_playable_actions() method returns the index of the card(s) in
        the hand of the current player that can be played in the current state.
        Default behavior is just to enforce following suit if possible.
        Games which override this behavior are NoHearts and NoKingOfHearts,
        because hearts may not be led unless no other suit is available,
        and Domino, due to the very different nature of the game.

        The update_scores() method must be overridden by every specific game.
        It updates the players' scores based on the current state, in which
        current_player is supposed to be the last trick winner.
    '''
    def __init__(self, players, first_player, trump_suit=None):
        assert len(players) == consts.NUM_PLAYERS, '[-] Please give a list of exactly {} players!'.format(consts.NUM_PLAYERS)
        self.players = players
        self.state = State(self.__class__.__name__, players, first_player, trump_suit)

    def play(self):
        while not self.state.terminal:
            # Copy the current state
            __state = deepcopy(self.state)
            
            # Hide the hands of the other players by setting them to None
            __state.hands = [__state.hands[i]
                             if i == self.state.current_player else None
                             for i in range(len(self.players))]
            
            # Get playable actions for the current player and embed them into the state
            __state.playable_actions = self.get_playable_actions()

            # Send modified state to the current player and wait for them to choose an action
            action = None
            while action not in __state.playable_actions:
                action = self.players[self.state.current_player].get_next_action(__state)

            # Compute the next state based on the action we got
            self.get_next_state(action)

        return self.state.scores

    def get_next_state(self, action):
        # Get card from action number and remove it from player's hand
        played_card = self.state.hands[self.state.current_player].pop(action)
        self.players[self.state.current_player].hand.pop(action)
        
        # Notify players of the played card
        for i in range(len(self.players)):
            self.players[i].notify_card(self.state.current_player, deepcopy(played_card))

        # Put the played card in the trick cards and played cards
        self.state.trick_cards.append(played_card)
        self.state.played_cards.append(played_card)

        # If the player didn't follow suit, take note of the missing suit
        if played_card.suit != self.state.trick_cards[0].suit:
            self.state.missing_suits[self.state.trick_cards[0].suit][self.state.current_player] = True

        # If the highest card of a suit has been played,
        # update the current highest card of that suit
        if played_card.value == self.state.highest[played_card.suit]:
            suit_played_values = [card.value for card in self.state.played_cards if card.suit == played_card.suit]
            remaining_values = [value for value in range(13) if value not in suit_played_values]

            if remaining_values:
                new_highest = remaining_values[-1]
            else:
                new_highest = None
            
            self.state.highest[played_card.suit] = new_highest

        # If the trick ended:
        #     - Calculate trick winner and update first and current player
        #     - Update scores
        #     - Empty trick cards
        #     - Tell players the trick winner
        if len(self.state.trick_cards) == consts.NUM_PLAYERS:
            self.state.current_player = get_trick_winner(self.state.first_player, self.state.trick_cards, self.state.trump_suit)
            self.state.first_player = self.state.current_player
            self.update_scores()
            self.state.trick_cards = []
            tell_everyone(self.players, 'Player {} won the trick!'.format(self.state.current_player))
        # Otherwise, just pass the turn to next player
        else:
            self.state.current_player = (self.state.current_player + 1) % consts.NUM_PLAYERS

        # If all hands are empty, this state is terminal
        if not any(self.state.hands):
            self.state.terminal = True

    def get_playable_actions(self):
        '''
            Default behavior: enforce following suit if possible.
        '''
        hand = self.state.hands[self.state.current_player]

        if not self.state.trick_cards:
            return [i for i in range(len(hand))]

        same_suit = [hand.index(card) for card in hand if card.suit == self.state.trick_cards[0].suit]

        if not same_suit:
            return [i for i in range(len(hand))]

        return same_suit

    def update_scores(self):
        raise NotImplementedError('[-] This needs to be implemented by your Game class!')