from copy import deepcopy
from Card import Card, Deck, get_trick_winner

class State():
    def __init__(self, trump_suit=None):
        '''
            Missing suits is a dictionary of 4 lists (one for every suit).
            Each list has 4 boolean entries (one for every player).
            If an entry is True, it means that player has ran out of
            cards of that suit.
        '''
        missing_suits = {'♥': [False for _ in range(Game.NUM_PLAYERS)],
                         '♦': [False for _ in range(Game.NUM_PLAYERS)],
                         '♣': [False for _ in range(Game.NUM_PLAYERS)],
                         '♠': [False for _ in range(Game.NUM_PLAYERS)]}

        self.current_player = 0
        self.first_player = 0
        self.hands = [[] for _ in range(Game.NUM_PLAYERS)]
        self.trick_cards = []
        self.played_cards = []
        self.missing_suits = missing_suits
        self.highest = {'♥': 12, '♦': 12, '♣': 12, '♠': 12}
        self.trump_suit = trump_suit
        self.playable_actions = []
        self.scores = [0 for _ in range(Game.NUM_PLAYERS)]
        self.terminal = False

    def __str__(self):
        '''
            For debugging.
        '''
        return '''
   [State]
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
   '''.format(self.current_player, self.first_player,
              self.hands[0], self.hands[1], self.hands[2],
              self.hands[3], self.trick_cards, self.played_cards,
              self.missing_suits['♥'], self.missing_suits['♦'],
              self.missing_suits['♣'], self.missing_suits['♠'],
              self.highest, self.trump_suit, self.playable_actions,
              self.scores, self.terminal)

    def __repr__(self):
        return __str__(self)

class Game():

    NUM_PLAYERS = 4

    def __init__(self, players, trump_suit=None):
        assert len(players) == Game.NUM_PLAYERS, '[-] Please give a list of exactly {} players!'.format(NUM_PLAYERS)
        self.players = players

        self.state = State()

        self.deck = Deck()
        self.distribute_cards()
        assert self.deck.is_empty(), '[-] Not all cards have been distributed!'

    def play(self):
        while not self.state.terminal:
            # Copy the current state
            __state = deepcopy(self.state)
            
            # Hide the hands of the other players by setting them to None
            __state.hands = [__state.hands[i]
                             if i == self.state.current_player else None
                             for i in range(len(self.players))]
            
            # Get playable actions for the current player
            hand = __state.hands[self.state.current_player]
            trick_cards = self.state.trick_cards
            playable_actions = self.get_playable_actions(hand, trick_cards)
            __state.playable_actions = playable_actions
            
            action = None
            while action not in playable_actions:
                # Send state to the current player and wait for the action
                action = self.players[self.state.current_player].get_next_action(__state)
            
            # Compute the next state based on the action we got
            self.state = self.get_next_state(self.state, action)

        return self.state.scores

    def distribute_cards(self):
        for i in range(Card.DIFFERENT_CARDS):
            self.state.hands[i % len(self.players)] += self.deck.draw()

        for i in range(len(self.state.hands)):
            self.state.hands[i] = list(map(Card.int_to_card, sorted(map(int, self.state.hands[i]))))

    def get_next_state(self, state, action):
        # Get card from action number and remove it from player's hand
        played_card = state.hands[state.current_player].pop(action)
        
        # Put the played card in the trick cards and played cards
        state.trick_cards.append(played_card)
        state.played_cards.append(played_card)

        # If the player didn't follow suit, record it
        if played_card.suit != state.trick_cards[0].suit:
            state.missing_suits[state.trick_cards[0].suit][state.current_player] = True

        # If the highest card of a suit has been played,
        # update it with a new highest card
        if played_card.value == state.highest[played_card.suit]:
            values_played_suit = sorted([card.value for card in state.played_cards if card.suit == played_card.suit])
            
            if values_played_suit:
                new_highest = values_played_suit[-1]
            else:
                new_highest = None
            
            state.highest[played_card.suit] = new_highest

        # If the trick ended:
        #     - calculate winner and update first and current player
        #     - empty trick cards
        #     - update scores
        if len(state.trick_cards) == 4:
            state.current_player = (get_trick_winner(state.trick_cards) + state.first_player) % len(self.state.hands)
            state.first_player = state.current_player
            state = self.update_scores(state)
            state.trick_cards = []
        else:
            state.current_player = (state.current_player + 1) % Game.NUM_PLAYERS

        # If all hands are empty, this state is terminal
        if not any(state.hands):
            state.terminal = True

        return state

    def get_playable_actions(self, hand, trick_cards):
        raise NotImplementedError('[-] This needs to be implemented by your Game class!')

    def update_scores(self, state):
        raise NotImplementedError('[-] This needs to be implemented by your Game class!')