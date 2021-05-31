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

    def ai_shoots(self, y_coord, x_coord, player_1_board, ai_score, every_button):
        """
        AI shooting method
    
        :param y_coord: y coordinate to shoot at
        :param x_coord: x coordinate to shoot at
        :param player_1_board: board to shoot at
        :param ai_score: score of AI
        """
        # if score is 20, AI has won
        if ai_score == 20:
            self.popupwindow("The computer has won.")
        # if AI got one hit, destroy complete ship
        if player_1_board[y_coord][x_coord] == ': ':
            ai_score += 1
            player_1_board[y_coord][x_coord] = 'X '
            every_button[0][y_coord - 1][x_coord - 1].configure(text="X", fg="black", bg="red3")
            # depending of where the rest of the ship is located, shot it
            if player_1_board[y_coord - 1][x_coord] == ': ':
                self.ai_shoots(y_coord - 1, x_coord, player_1_board, ai_score)
            elif player_1_board[y_coord + 1][x_coord] == ': ':
                self.ai_shoots(y_coord + 1, x_coord, player_1_board, ai_score)
            elif player_1_board[y_coord][x_coord - 1] == ': ':
                self.ai_shoots(y_coord, x_coord - 1, player_1_board, ai_score)
            elif player_1_board[y_coord][x_coord + 1] == ': ':
                self.ai_shoots(y_coord, x_coord + 1, player_1_board, ai_score)
            else:
                # shot some random position if ship is destroyed
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                self.ai_shoots(y, x, player_1_board, ai_score)
        elif player_1_board[y_coord][x_coord] == 'X ' or player_1_board[y_coord][x_coord] == 'O ':
            # if position was already shoot at, try a new position
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            self.ai_shoots(y, x, player_1_board, ai_score)
        else:
            # if water was hit just change the button
            player_1_board[y_coord][x_coord] = 'O '
            self.every_button[0][y_coord - 1][x_coord - 1].configure(text="O", fg="white")
    
    def nr_players(self, number, every_button, p2_or_ai):
        """
        Set number of players
    
        :param number: number of needed players
        """
        global AI
        # activate player2 Buttons
        for bt_list in every_button[1]:
            for bt in bt_list:
                bt['state'] = 'normal'
        # if one player is needed activate AI
        if number == 1:
            p2_or_ai="AI"
            AI = True
        else:
            # activate player2 Buttons
            for bt_list in every_button[0]:
                for bt in bt_list:
                    bt['state'] = 'normal'
            p2_or_ai="Player 2"

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