from tkinter import *
import random
from model import Model, Player
import subprocess


class Controller:
    """
    Controller object that controls in game actions

    :param win_counter : Decides number of hits to victory
    """
    def __init__(self, win_counter : int = 3):
        self.turn = random.randint(1,2)
        self.win_counter = win_counter
        self.turn_label_info = StringVar()
        self.turn_label_info.set(f"Player turn: {self.turn}")
        self.info = StringVar()
        self.info.set(f"Game begins!")
        self.model = Model()


    def hit_or_miss(self, a, b, rival, all_buttons, player, root):
        """
        check if there was a hit or a missed done by the player
    
        :param a: clicked y position
        :param b: clicked x position
        :param rival: Rival player
        :param all_buttons: all buttons of the rival player's board
        :param player: Current player
        """

        #In case the player that clicks is out of turn
        if player.id != self.turn:
            self.info.set(f"Wait for your turn, {player.name}")
            return

        if rival.board[a + 1][b + 1] == ': ':
            # if a ship was hit change the button and the players board
            self.info.set(f"{player.name} hit!")
            rival.board[a + 1][b + 1] = 'X '
            all_buttons[a][b].configure(text="X", fg="black", bg="red3", activebackground="red3", state="disabled")
            # increase the hit counter and go again
            player.hits += 1
            player.score.set(f"Score: {player.hits}")
            self.turn = player.id
        else:
            self.info.set(f"{player.name} miss...")
            rival.board[a + 1][b + 1] = 'O '
            all_buttons[a][b].configure(text="O", fg="White", activeforeground="white", state="disabled")
            self.turn = rival.id
            self.turn_label_info.set(f"Player turn: {self.turn}")

        if player.hits == self.win_counter:
            # if current player got a number of hits that equals to the win_counter he won
            self.info.set(f"Game over, {player.name} won!")
            self.disable_buttons(root)

    def restart_program(self):
        '''
        This method restarts the game script
        '''
        try:
            subprocess.Popen(["python", "game.py"])
        except:
            subprocess.Popen(["python3", "game.py"])
        exit()

    def get_players(self):
        player_list = []
        player1 = Player(name="player 1", model=self.model, id=1)
        player2 = Player(name="player 2", model=self.model, id=2)
        player_list.append(player1)
        player_list.append(player2)
        return player_list

    def get_turn(self):
        return self.turn_label_info

    def get_info(self):
        return self.info

    def add_buttons(self, all_buttons):
        return self.model.every_button.append(all_buttons)

    def disable_buttons(self, root):
        for widget in root.winfo_children():
            if type(widget) == type(Button()) and widget['text'] != "Restart game":
                widget.configure(state="disabled")
