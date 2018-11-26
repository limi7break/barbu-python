import consts
from game.Game import Game
from Card import Card
from utils import int_input

class Domino(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

        # Ask dealer for Domino starting value
        self.starting_value = None
        while self.starting_value is None or self.starting_value not in range(13):
            self.starting_value = players[first_player].get_starting_value()
        
        print('(starting value: {})'.format(Card.labels[self.starting_value]))

    def get_next_state(self, state, action):
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
            played_card = state.hands[state.current_player].pop(action)
            print('{} played: {}'.format(state.current_player, played_card))

            # Attach the card to the list.
            state = self.attach_card(state, played_card)

            # If the current player has an empty hand
            # and still has a score == 0, update scores
            if not state.hands[state.current_player] and not state.scores[state.current_player]:
                state = self.update_scores(state)

        else:
            print('{} passed!'.format(state.current_player))

        state.current_player = (state.current_player + 1) % consts.NUM_PLAYERS

        # If all hands are empty, this state is terminal
        if not any(state.hands):
            state.terminal = True

        return state

    def get_playable_actions(self, hand, _):
        '''
            For this game, trick_cards is not used.
            played_cards is instead used to compute the playable
            actions. So, the parameter is ignored for clarity.
        '''
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

    def update_scores(self, state):
        '''
            Give the current player the highest current score.

            The highest current score is based on how many of
            the other players have already received theirs.
        '''
        scores = [45, 20, 10, -10]
        finished_num = sum([1 for score in state.scores if score])
        state.scores[state.current_player] += scores[finished_num]
        
        return state

    def attach_card(self, state, played_card):
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
        suit_cards = state.played_cards[played_card.suit]
        
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

        state.played_cards[played_card.suit] = suit_cards

        return state