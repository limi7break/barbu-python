import consts
from copy import deepcopy
from game.Game import Game
from Card import Card
from utils import int_input, tell_everyone

class Domino(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

        # Ask dealer for Domino starting value
        self.starting_value = None
        while self.starting_value is None or self.starting_value not in range(13):
            self.starting_value = players[first_player].get_starting_value()
        
        tell_everyone(self.players, '(starting value: {})'.format(Card.labels[self.starting_value]))

    def get_next_state(self, action):
        '''
            Domino overrides get_next_state because it has special rules.

            This game is *not* trick-taking, so the following attributes
            are *not* used in the state:
                - first_player
                - trick_cards
                - missing_suits
                - highest
                - trump_suit

            The played cards are recorded in played_cards, which is a
            dictionary of suits of the form:

            {'♥': [...],
             '♦': [...],
             '♣': [...],
             '♠': [...]}

            Every suit is mapped to a list of cards of that suit that
            have been played so far.

            When a card is played, the card is appended or prepended to
            the list of the corresponding suit.

            In Domino, unlike all other games, the ace has the lowest
            value (lower than the 2). So, it will be prepended to the 2
            of the corresponding suit.

            The starting value is the only value that can be played
            when a suit has not been 'opened' yet.
        '''
        if action > -1:
            # Get card from action number and remove it from player's hand
            played_card = self.state.hands[self.state.current_player].pop(action)
            self.players[self.state.current_player].hand.pop(action)

            # Notify players of the played card
            for i in range(len(self.players)):
                self.players[i].notify_card(self.state.current_player, deepcopy(played_card))

            # Attach the card to the list.
            self.attach_card(played_card)

            # If the current player has an empty hand
            # and still has a score == 0, update scores
            if not self.state.hands[self.state.current_player] and not self.state.scores[self.state.current_player]:
                self.update_scores()

        else:
            tell_everyone(self.players, '{} passed!'.format(self.state.current_player))

        self.state.current_player = (self.state.current_player + 1) % consts.NUM_PLAYERS

        # If all hands are empty, this state is terminal
        if not any(self.state.hands):
            self.state.terminal = True

    def get_playable_actions(self):
        hand = self.state.hands[self.state.current_player]

        playable_actions = []
        for i, card in enumerate(hand):
            # Check starting cards
            if card.value == self.starting_value:
                playable_actions.append(i)
                continue

            suit_cards = self.state.played_cards[card.suit]

            # Besides starting cards,
            if suit_cards:
                # Ace (value: 12) can be put *only* before a 2 (value: 0)
                if card.value == 12:
                    if suit_cards[0].value == 0:
                        playable_actions.append(i)
                # King (value: 11) can be put *only* after a Q (value: 10)
                elif card.value == 11:
                    if suit_cards[-1].value == 10:
                        playable_actions.append(i)
                # Two can be put *also* after an Ace (value: 12)
                elif card.value == 0 and suit_cards[0].value == 12:
                    playable_actions.append(i)
                # Other cards can be put when there is an adjacent value
                elif card.value == suit_cards[0].value - 1 or card.value == suit_cards[-1].value + 1:
                    playable_actions.append(i)

        if not playable_actions:
            return [-1]

        return playable_actions

    def update_scores(self):
        '''
            Give the current player the highest current score.

            The highest current score is based on how many of
            the other players have already received theirs.
        '''
        scores = [45, 20, 10, -10]
        finished_num = sum([1 for score in self.state.scores if score])
        self.state.scores[self.state.current_player] += scores[finished_num]

    def attach_card(self, played_card):
        '''
            Adds the played card to the state's played cards,
            keeping into account that these are special cards
            in this game:

                - Ace (value: 12) *must* be added at the beginning of the list.
                - Two (value: 0) *must* be added at the beginning of the list,
                  except if an Ace is already present at the beginning.
                  In that case, the Two is added at index 1 instead.
                - King (value: 11) *must* be added at the end of the list.

            The played card is assumed valid, because the action
            passed to get_next_state is validated in the play() method
            against the actions returned by get_playable_actions.
        '''
        suit_cards = self.state.played_cards[played_card.suit]
        
        if not suit_cards:
            suit_cards = [played_card]
        elif played_card.value == 12:
            suit_cards = [played_card] + suit_cards
        elif played_card.value == 0:
            if suit_cards[0].value == 12:
                suit_cards.insert(1, played_card)
            else:
                suit_cards = [played_card] + suit_cards
        elif played_card.value == 11:
            suit_cards.append(played_card)
        elif played_card.value > suit_cards[-1].value:
            suit_cards.append(played_card)
        elif played_card.value < suit_cards[0].value:
            suit_cards = [played_card] + suit_cards
        else:
            raise ValueError('[-] The selected card cannot be appended nor prepended to the corresponding suit! (suit: {}, value: {})'.format(played_card.suit, played_card.value))

        self.state.played_cards[played_card.suit] = suit_cards