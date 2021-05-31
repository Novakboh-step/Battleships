from tkinter import *
import random
import os
import sys
import tkinter.messagebox as tkMessageBox


class Controller:
    """
    Controller object that controls in game actions

    :param win_counter : Decides number of hits to victory
    """
    def __init__(self, win_counter : int = 20):
        self.turn = random.randint(1,2)
        self.win_counter = win_counter
        print(f"Game begins, player {self.turn} starts")


    def hit_or_miss(self, a, b, rival, all_buttons, player):
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
            print(f"Wait for your turn, {player.name}")
            return

        if rival.board[a + 1][b + 1] == ': ':
            # if a ship was hit change the button and the players board
            print("A hit, nice shot " + player.name + "!")
            rival.board[a + 1][b + 1] = 'X '
            all_buttons[a][b].configure(text="X", fg="black", bg="red3", activebackground="red3", state="disabled")
            # increase the hit counter and go again
            player.hits += 1
            player.score.set(f"Score: {player.hits}")
            self.turn = player.id
        else:
            print("Seems like you missed that one, " + player.name + "!")
            rival.board[a + 1][b + 1] = 'O '
            all_buttons[a][b].configure(text="O", fg="White", activeforeground="white", state="disabled")
            self.turn = rival.id
        print(f"Player {self.turn} turn")

        if player.hits == self.win_counter:
            # if one player got 20 hits he won
            self.popupwindow(player.name + " has won!")

    def restart_program(self):
        '''
        This method restarts the game script
        '''
        python = sys.executable
        os.execl(python, python, *sys.argv)
        pass

    def popupwindow(self, msg):
        """
        Pop up window if game is over
    
        :param msg: player name
        """
        answer = tkMessageBox.askquestion("Game Over", msg + " Would you like to play again?")
        if answer == "yes":
            self.restart_program()
        elif answer == "no":
            quit()