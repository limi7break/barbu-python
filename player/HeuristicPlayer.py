import sys

sys.path.append('..')

import random, consts
from copy import deepcopy
from player.Player import Player
from Card import Card, Deck, get_winning_card

def rescale(value, old_low, old_high, new_low, new_high):
    return int(round(((value-old_low)*(new_high-new_low)/(old_high-old_low)) + new_low))

class HeuristicPlayer(Player):
    '''
        A player that plays according to some expert-made
        heuristics. It implements a different action logic
        for every game.
    '''
    def __init__(self, ID, name=''):
        super().__init__(ID, name)

    def get_next_game(self):
        available_games = [game_num for game_num, played in self.played_games.items() if not played]
        heuristics = list(map(self.calculate_heuristic, available_games))
        return available_games[heuristics.index(max(heuristics))]

    def get_trump_suit(self):
        # Divide cards in different suits and get sum of values
        suit_values = [sum([card.value for card in self.hand if card.suit == '♥']),
                       sum([card.value for card in self.hand if card.suit == '♦']),
                       sum([card.value for card in self.hand if card.suit == '♣']),
                       sum([card.value for card in self.hand if card.suit == '♠'])]

        # Return suit corresponding to highest sum of values
        return Card.suits[suit_values.index(max(suit_values))]

    def get_starting_value(self):
        # Calculate spread for every card value
        spread_values = []
        for value in range(13):
            spread_values.append(self.calculate_spread(value, low_ace=True))

        # Return value corresponding to lowest spread
        return spread_values.index(min(spread_values))

    def get_next_action(self, state):
        if state.game == 'Atout':
            return self.get_next_action_atout(state)
        if state.game == 'NoTricks':
            return self.get_next_action_notricks(state)
        if state.game == 'NoHearts':
            return self.get_next_action_nohearts(state)
        if state.game == 'NoKingOfHearts':
            return self.get_next_action_nokingofhearts(state)
        if state.game == 'NoLastTwo':
            return self.get_next_action_nolasttwo(state)
        if state.game == 'NoQueens':
            return self.get_next_action_noqueens(state)
        if state.game == 'Domino':
            return self.get_next_action_domino(state)

        raise ValueError('[-] Game not valid! (game: {})'.format(state.game))

    def get_next_action_atout(self, state):
        '''
        Leading:
            - if we have the highest trump, play it
            - if we have any of the highest non-trump cards:
                - if there is no trump suit, play one of those cards
                - if there is a trump suit, play one of those cards but *only* if no one has
                  ran out of cards of that suit
            - else: play the lowest non-trump if any, or the lowest trump otherwise.

        Non-leading:
            - if we have to follow suit:
                - play higher only if that card is the highest of that suit.
                - if we cannot play higher, play the lowest card of that suit.
            - if we don't:
                - play the lowest trump, or the lowest card otherwise.
        '''
        state = self.fix_missing(state)

        if not state.trick_cards:
            # Leading
            highest_trump = [card for card in self.hand if card.suit == state.trump_suit and self.is_highest(state, card)]
            if highest_trump:
                return self.hand.index(highest_trump[0])
            
            highest_non_trumps = [card for card in self.hand if card.suit != state.trump_suit and self.is_highest(state, card)]
            for card in highest_non_trumps:
                players_after = [(self.ID + i + 1) % consts.NUM_PLAYERS for i in range(consts.NUM_PLAYERS - len(state.trick_cards))]
                if not state.trump_suit or (state.trump_suit and not any([state.missing_suits[card.suit][player] for player in players_after])):
                    return self.hand.index(card)
            
            if not highest_non_trumps:
                non_trumps = [card for card in self.hand if card.suit != state.trump_suit]
                if non_trumps:
                    lowest_non_trump = min(non_trumps, key=lambda x: x.value)
                    return self.hand.index(lowest_non_trump)

            return self.hand.index(min(self.hand, key=lambda x: x.value))
                
        else:
            # Non-leading
            same_suit = [card for card in self.hand if card.suit == state.trick_cards[0].suit]
            if same_suit:
                suit = state.trick_cards[0].suit
                highest_card = Card(suit, state.highest[suit])
                if highest_card in same_suit:
                    return self.hand.index(highest_card)
                else:
                    return self.hand.index(min(same_suit, key=lambda x: x.value))
            else:
                sorted_trumps = sorted([card for card in self.hand if card.suit == state.trump_suit], key=lambda x: x.value)
                if sorted_trumps:
                    return self.hand.index(sorted_trumps[0])
                else:
                    return self.hand.index(min(self.hand, key=lambda x: x.value))

    def get_next_action_notricks(self, state):
        '''
        Leading:
            - if we have a card that is not the highest card of that suit,
              and some players still have that suit, play it
            - else, play the lowest card we have.
        
        Non-leading:
            - if we have to follow suit:
                - if we *have* to play higher, play the highest card of that suit.
                - if we can go lower, play the highest card of that suit that goes lower.
            - if we don't:
                - play the highest card we have.
        '''
        state = self.fix_missing(state)

        if not state.trick_cards:
            # Leading
            other_players = [i for i in range(consts.NUM_PLAYERS) if i != self.ID]
            valid_suits = []
            for suit in Card.suits:
                suit_cards = [card for card in self.hand if card.suit == suit]
                if suit_cards:
                    if not all([state.missing_suits[suit][player] for player in other_players]) and \
                       not self.is_highest(state, min(suit_cards, key=lambda x: x.value)):
                        valid_suits.append(suit)

            if valid_suits:
                lowest_card = min([card for card in self.hand if card.suit == valid_suits[0]], key=lambda x: x.value)
                return self.hand.index(lowest_card)
            
            return self.hand.index(min(self.hand, key=lambda x: x.value))
        
        else:
            # Non-leading
            same_suit = [card for card in self.hand if card.suit == state.trick_cards[0].suit]
            if same_suit:
                winning_card = get_winning_card(state.trick_cards)
                lower_same_suit = [card for card in same_suit if card.value < winning_card.value]
                if lower_same_suit:
                    return self.hand.index(max(lower_same_suit, key=lambda x: x.value))    
                else:
                    return self.hand.index(max(same_suit, key=lambda x: x.value))
            
            return self.hand.index(max(self.hand, key=lambda x: x.value))

    def get_next_action_nohearts(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!\n{}\n{}'.format(self.ID, self.hand, state.hands[state.current_player])
        return random.choice(state.playable_actions)

    def get_next_action_nokingofhearts(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!\n{}\n{}'.format(self.ID, self.hand, state.hands[state.current_player])
        return random.choice(state.playable_actions)

    def get_next_action_nolasttwo(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!\n{}\n{}'.format(self.ID, self.hand, state.hands[state.current_player])
        return random.choice(state.playable_actions)

    def get_next_action_noqueens(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!\n{}\n{}'.format(self.ID, self.hand, state.hands[state.current_player])
        return random.choice(state.playable_actions)

    def get_next_action_domino(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!\n{}\n{}'.format(self.ID, self.hand, state.hands[state.current_player])
        return random.choice(state.playable_actions)

    def calculate_spread(self, pivot, low_ace=False):
        spread = 0
        for card in self.hand:
            # Fix ace value
            if low_ace and card.value == 12:
                current_value = -1
            else:
                current_value = card.value

            # Calculate spread
            spread += abs(pivot - current_value)

        return int(spread)

    def calculate_heuristic(self, game_num):
        if game_num == 0:
            # Atout
            return sum([card.value for card in self.hand])
        if game_num == 1:
            # NoTricks
            return 165 - sum([card.value for card in self.hand])
        if game_num == 2:
            # NoHearts
            diamonds = [card for card in self.hand if card.suit == '♦']
            clubs = [card for card in self.hand if card.suit == '♣']
            spades = [card for card in self.hand if card.suit == '♠']
            
            l = [len(diamonds), len(clubs), len(spades)]
            spread = max(l) - min(l)
            
            if spread > 5:
                return 141
            else:
                return 141 - (19*(5-spread))
        if game_num == 3:
            # NoKingOfHearts
            # TODO: Improve else case
            return 141 if Card('Hearts', 'K') in self.hand else 24
        if game_num == 4:
            #NoLastTwo
            spread = self.calculate_spread(6)
            return rescale(spread, 10, 73, 24, 141)
        if game_num == 5:
            # NoQueens
            hearts_values = [card.value for card in self.hand if card.suit == '♥']
            diamonds_values = [card.value for card in self.hand if card.suit == '♦']
            clubs_values = [card.value for card in self.hand if card.suit == '♣']
            spades_values = [card.value for card in self.hand if card.suit == '♠']

            is_bad_suit = lambda suit_values: 10 in suit_values and not any([i in suit_values for i in range(10)])
            bad_suits = sum(list(map(is_bad_suit, [hearts_values, diamonds_values, clubs_values, spades_values])))

            # TODO: improve else case
            return 24 if bad_suits else 140
        if game_num == 6:
            # Domino
            spread = [self.calculate_spread(value, low_ace=True) for value in range(13)]
            return rescale(min(spread), 10, 73, 24, 141)

    def fix_missing(self, state):
        other_players = [i for i in range(consts.NUM_PLAYERS) if i != self.ID]
        for suit in Card.suits:
            if sum([1 for card in state.played_cards if card.suit == suit]) + sum([1 for card in self.hand if card.suit == suit]) == 13:
                for player in other_players:
                    state.missing_suits[suit][player] = True

        return state

    def is_highest(self, state, card):
        for suit, value in state.highest.items():
            if card.suit == suit and card.value == value:
                return True

        return False