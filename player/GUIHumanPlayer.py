import os, consts
from player.Player import HumanPlayer
from utils import is_valid_int
from Card import Card
from tkinter import *
from tkinter.simpledialog import askstring
from PIL import ImageTk, Image
from random import shuffle
from time import sleep

class GUIHumanPlayer(HumanPlayer):
    '''
        A human player that can play interactively
        and select actions via Graphical User Interface.
    '''
    APP_NAME   = 'barbu-python'
    IMG_DIR    = 'img'
    LEFT_BG    = '#369f4d'
    RIGHT_BG   = '#096c1f'
    INFO_LINES = 20

    def __init__(self, ID, name=""):
        super().__init__(ID, name)

        self.window = Tk()
        self.window.title(GUIHumanPlayer.APP_NAME)
        self.window.geometry('1050x600')

        # self.card_images is a dictionary associating each Card
        # to its corresponding ImageTk.PhotoImage.
        self.card_images = self.load_images()

        # Create main containers
        self.left_up = Frame(self.window, bg=GUIHumanPlayer.LEFT_BG)
        self.left_down = Frame(self.window, bg=GUIHumanPlayer.LEFT_BG)
        self.right = Frame(self.window, bg=GUIHumanPlayer.RIGHT_BG)

        # Layout main containers
        self.window.grid_rowconfigure(0, weight=500)
        self.window.grid_rowconfigure(1, weight=180)
        self.window.grid_columnconfigure(0, weight=1000)
        self.window.grid_columnconfigure(1, weight=200)

        self.left_up.grid(row=0, column=0, sticky='nswe')
        self.left_down.grid(row=1, column=0, sticky='nswe')
        self.right.grid(row=0, column=1, rowspan=2, sticky='nswe')

        # Create widgets
        self.game_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white', font=('Helvetica', 16))
        self.score0_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.score1_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.score2_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.score3_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.dealer_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.hand_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')
        self.info_label = Label(self.right, anchor='w', justify='left', text='', bg=GUIHumanPlayer.RIGHT_BG, fg='white')

        self.card_labels = []
        for _ in range(13):
            self.card_labels.append(Label(self.left_down, bg=GUIHumanPlayer.LEFT_BG))

        self.player_n_label = Label(self.left_up, anchor='w', justify='left', text='Player {}'.format((self.ID + 2) % consts.NUM_PLAYERS), bg=GUIHumanPlayer.LEFT_BG, fg='white', font=('Helvetica', 12, 'bold'))
        self.player_w_label = Label(self.left_up, anchor='w', justify='left', text='Player {}'.format((self.ID + 1) % consts.NUM_PLAYERS), bg=GUIHumanPlayer.LEFT_BG, fg='white', font=('Helvetica', 12, 'bold'))
        self.player_e_label = Label(self.left_up, anchor='w', justify='left', text='Player {}'.format((self.ID + 3) % consts.NUM_PLAYERS), bg=GUIHumanPlayer.LEFT_BG, fg='white', font=('Helvetica', 12, 'bold'))
        self.player_s_label = Label(self.left_up, anchor='w', justify='left', text='Player {}'.format(self.ID), bg=GUIHumanPlayer.LEFT_BG, fg='white', font=('Helvetica', 12, 'bold'))

        self.card_n_label = Label(self.left_up, bg=GUIHumanPlayer.LEFT_BG)
        self.card_w_label = Label(self.left_up, bg=GUIHumanPlayer.LEFT_BG)
        self.card_e_label = Label(self.left_up, bg=GUIHumanPlayer.LEFT_BG)
        self.card_s_label = Label(self.left_up, bg=GUIHumanPlayer.LEFT_BG)

        self.seats = {((self.ID + 2) % consts.NUM_PLAYERS): self.card_n_label,
                      ((self.ID + 1) % consts.NUM_PLAYERS): self.card_w_label,
                      ((self.ID + 3) % consts.NUM_PLAYERS): self.card_e_label,
                       self.ID:                             self.card_s_label}

        self.domino = False
        self.domino_labels = {}
        domino_order = [int(Card('Hearts',  'A'))] + list(range(12))    \
                     + [int(Card('Diamonds','A'))] + list(range(13,25)) \
                     + [int(Card('Clubs',   'A'))] + list(range(26,38)) \
                     + [int(Card('Spades',  'A'))] + list(range(39,51))
        x = 35
        y = -85
        for i, n in enumerate(domino_order):
            card = Card.int_to_card(n)
            label = Label(self.left_up, bg=GUIHumanPlayer.LEFT_BG, image=self.card_images[card])
            x += 49
            if i % 13 == 0:
                x  = 35
                y += 100
            self.domino_labels[card] = {'label': label, 'x': x, 'y': y}

        # Layout widgets
        self.game_label.grid(padx=5, pady=5)
        self.score0_label.grid(sticky='w', padx=5)
        self.score1_label.grid(sticky='w', padx=5)
        self.score2_label.grid(sticky='w', padx=5)
        self.score3_label.grid(sticky='w', padx=5)
        self.dealer_label.grid(sticky='w', padx=5)
        self.hand_label.grid(sticky='w', padx=5)
        self.info_label.grid(sticky='sw', padx=5)

        self.card_n_label.place(x=330, y=80)
        self.card_w_label.place(x=230, y=150)
        self.card_e_label.place(x=430, y=150)
        self.card_s_label.place(x=330, y=220)

        self.player_n_label.place(x=340, y=50)
        self.player_w_label.place(x=145, y=200)
        self.player_e_label.place(x=530, y=200)
        self.player_s_label.place(x=340, y=360)

        self.refresh()

    def get_next_game(self):
        self.show_hand(self.hand)
        self.refresh()
        
        available_games = [game_num for game_num, played in self.played_games.items() if not played]

        s = 'Choose game:\n'
        for i in available_games:
            s += '    {}: {}\n'.format(i, consts.GAMES[i].split('.')[1])
        
        game = None
        while not is_valid_int(game) or int(game) not in available_games:
            game = askstring(GUIHumanPlayer.APP_NAME, s)

        return int(game)

    def get_trump_suit(self):
        s = 'Choose trump suit:\n'
        for i in range(len(Card.suits)):
            s += '    {}: {}\n'.format(i, Card.suits[i])
        
        suit = None
        while not is_valid_int(suit) or int(suit) not in range(len(Card.suits)):
            suit = askstring(GUIHumanPlayer.APP_NAME, s)

        return Card.suits[int(suit)]

    def get_starting_value(self):
        s = 'Choose starting value (two: 0, ace: 12):'

        starting_value = None
        while not is_valid_int(starting_value) or int(starting_value) not in range(13):
            starting_value = askstring(GUIHumanPlayer.APP_NAME, s)

        return int(starting_value)

    def get_next_action(self, state):
        assert state.hands[state.current_player] == self.hand, '[-] Player {}\'s hand differs from their hand in the received state!'.format(self.ID)

        hand = state.hands[state.current_player]
        self.show_hand(hand)

        if state.playable_actions == [-1]:
            self.refresh()
            return -1

        # Create integer variable
        action = IntVar()

        func_ids = []
        for i in state.playable_actions:
            # Bind actions to playable cards that set the
            # action variable to the corresponding value
            func_id = self.card_labels[i].bind('<Button-1>', (lambda x: lambda _: action.set(x))(i)) # lambda closure
            func_ids.append(func_id)

            # Highlight playable cards by moving them up 10px
            if self.card_labels[i].place_info():
                x = int(self.card_labels[i].place_info()['x'])
                y = int(self.card_labels[i].place_info()['y'])
                self.card_labels[i].place(x=x, y=y-10)

        # Update labels with info from the received state
        self.game_label.configure(text=state.game)
        self.score0_label.configure(text='Player {}: {} points'.format(0, state.scores[0]))
        self.score1_label.configure(text='Player {}: {} points'.format(1, state.scores[1]))
        self.score2_label.configure(text='Player {}: {} points'.format(2, state.scores[2]))
        self.score3_label.configure(text='Player {}: {} points'.format(3, state.scores[3]))

        self.refresh()

        # Wait for user action
        self.left_down.wait_variable(action)
        action = action.get()

        for i, func_id in zip(state.playable_actions, func_ids):
            # Remove action bindings
            self.card_labels[i].unbind('<Button-1>', func_id)

            # Put the cards back down
            if self.card_labels[i].place_info():
                x = int(self.card_labels[i].place_info()['x'])
                y = int(self.card_labels[i].place_info()['y'])
                self.card_labels[i].place(x=x, y=y+10)

        # Remove image from card label in hand
        self.card_labels[action].place_forget()

        self.refresh()

        return action

    def begin_domino(self):
        self.domino = True
        self.player_n_label.place_forget()
        self.player_w_label.place_forget()
        self.player_e_label.place_forget()
        self.player_s_label.place_forget()

    def end_domino(self):
        self.domino = False
        
        for lxy in self.domino_labels.values():
            lxy['label'].place_forget()
        
        self.player_n_label.place(x=340, y=50)
        self.player_w_label.place(x=145, y=200)
        self.player_e_label.place(x=530, y=200)
        self.player_s_label.place(x=340, y=360)

    def tell(self, string):
        if 'Domino' in string:
            self.begin_domino()

        lines = self.info_label.cget('text').splitlines()
        
        if len(lines) == GUIHumanPlayer.INFO_LINES:
            lines.pop(0)
        
        lines.append(string)
        
        self.info_label.configure(text='\n'.join(lines))
        self.refresh()

    def notify_card(self, ID, card):
        if self.domino:
            lxy = self.domino_labels[card]

            lxy['label'].place(x=lxy['x'], y=lxy['y'])
            
            if all([lxy['label'].place_info() for lxy in self.domino_labels.values()]):
                sleep(3) # fix this
                self.end_domino()
            
            self.refresh()
            return

        self.seats[ID].configure(image=self.card_images[card])
        self.refresh()

        # If trick ended
        if all([label.cget('image') != '' for label in self.seats.values()]):
            sleep(1) # fix this
            for label in self.seats.values():
                label.configure(image='')

        self.refresh()

    def show_hand(self, hand):
        x = 35
        y = 15
        for i in range(len(self.card_labels)):
            if i < len(hand):
                self.card_labels[i].configure(image=self.card_images[hand[i]])
                self.card_labels[i].place(x=x, y=y)
                x += 49
            else:
                self.card_labels[i].place_forget()

    def load_images(self):
        images = {}

        for i in range(consts.DIFFERENT_CARDS):
            card = Card.int_to_card(i)
            img = ImageTk.PhotoImage(Image.open('{}/{}.png'.format(GUIHumanPlayer.IMG_DIR, i)))
            images[card] = img

        return images

    def refresh(self):
        self.window.update_idletasks()
        self.window.update()