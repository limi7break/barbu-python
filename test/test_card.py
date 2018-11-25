import sys, unittest
sys.path.append('..')

class TestCard(unittest.TestCase):

    def test_create_from_value(self):
        from Card import Card
        
        for suit in Card.suits:
            for value in range(13):
                card = Card(suit, value)

                self.assertEqual(card.suit, suit)
                self.assertEqual(card.value, value)

    def test_create_from_label(self):
        from Card import Card
        
        for suit in Card.suits:
            for label in Card.labels:
                card = Card(suit, label)

                self.assertEqual(card.suit, suit)
                self.assertEqual(card.value, Card.labels.index(label))

    def test_invalid_value(self):
        from Card import Card

        with self.assertRaises(ValueError):
            Card('Diamonds', 13)
            Card('Clubs', -1)
            Card('Hearts', 1337)

    def test_invalid_label(self):
        from Card import Card

        with self.assertRaises(ValueError):
            Card('Spades', 'X')
            Card('Hearts', 'yolo')

    def test_invalid_suit(self):
        from Card import Card

        with self.assertRaises(ValueError):
            Card('insert', 6)
            Card('suit', 7)
            Card('here', 8)

    def test_deck(self):
        from Card import Card, Deck

        deck = Deck()
        self.assertEqual(len(deck.cards), Card.DIFFERENT_CARDS)

        drawn     = deck.draw(5)
        remaining = Card.DIFFERENT_CARDS - 5
        self.assertEqual(len(drawn), 5)
        self.assertEqual(len(deck.cards), remaining)

        deck.draw(remaining)
        self.assertTrue(deck.is_empty())

    def test_is_new_winner(self):
        from Card import Card, is_new_winner

        # No trump. Put higher value of same suit -> True
        self.assertTrue(is_new_winner(new_card=Card('Hearts', 8),
                                      winning_card=Card('Hearts', 7), trump_suit=None))
        
        # No trump. Put lower value of same suit -> False
        self.assertFalse(is_new_winner(new_card=Card('Clubs', 3),
                                       winning_card=Card('Clubs', 4), trump_suit=None))
        
        # No trump. Put other suit -> False
        self.assertFalse(is_new_winner(new_card=Card('Hearts', 12),
                                       winning_card=Card('Spades', 0), trump_suit=None))
        self.assertFalse(is_new_winner(new_card=Card('Diamonds', 12),
                                       winning_card=Card('Spades', 0), trump_suit=None))
        self.assertFalse(is_new_winner(new_card=Card('Clubs', 12),
                                       winning_card=Card('Spades', 0), trump_suit=None))
        
        # Trump = Diamonds. Put higher trump -> True
        self.assertTrue(is_new_winner(new_card=Card('Diamonds', 8),
                                      winning_card=Card('Diamonds', 7), trump_suit='Diamonds'))
        
        # Trump = Spades. Put lower trump -> False
        self.assertFalse(is_new_winner(new_card=Card('Spades', 3),
                                       winning_card=Card('Spades', 4), trump_suit='Spades'))
        
        # Trump = Hearts. Put trump over other suit -> True
        self.assertTrue(is_new_winner(new_card=Card('Hearts', 0),
                                      winning_card=Card('Diamonds', 12), trump_suit='Hearts'))
        self.assertTrue(is_new_winner(new_card=Card('Hearts', 0),
                                      winning_card=Card('Clubs', 12), trump_suit='Hearts'))
        self.assertTrue(is_new_winner(new_card=Card('Hearts', 0),
                                      winning_card=Card('Spades', 12), trump_suit='Hearts'))

    def test_get_trick_winner(self):
        from Card import Card, get_trick_winner

        # Normal trick, everyone follows suit. 3 wins
        self.assertEqual(get_trick_winner([Card('Clubs', 2),
                                           Card('Clubs', 7),
                                           Card('Clubs', 10),
                                           Card('Clubs', 12)]), 3)

        # Trump = Diamonds wins. 2 wins
        self.assertEqual(get_trick_winner([Card('Spades', 10),
                                           Card('Spades', 11),
                                           Card('Diamonds', 0),
                                           Card('Spades', 12)],
                                           trump_suit='Diamonds'), 2)

        # No one follows suit, no trump. 0 wins
        self.assertEqual(get_trick_winner([Card('Hearts', 0),
                                           Card('Diamonds', 12),
                                           Card('Clubs', 12),
                                           Card('Spades', 12)]), 0)

if __name__ == '__main__':
    unittest.main()