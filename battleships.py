from tkinter import *
from tkinter.font import Font
import tkinter.messagebox as tkmessageBox
from functools import partial
import random
import time
import sys
import os
 
root = Tk()
root.wm_title("BATTLESHIPS")
root.configure(background='gray19')
font1 = Font(family='Helvetica', size=12, weight='bold')
font_big = Font(family='Helvetica', size=16, weight='bold')
font_normal = Font(family='Helvetica', size=10, weight='normal')
 
ships = {"Aircraft Carrier": 4, "Battleship": 3, "Submarine": 2, "Destroyer": 1}
AI = False
 
 
def restart_program():
    '''
    This method restarts the game script
    '''
    python = sys.executable
    os.execl(python, python, *sys.argv)
 
 
def player_board():
    """
    generating a 2 dimensional array representing one players board
 
    :return: two dimensional list
    """
    board = []
    t = []
    # creating the upper bounder
    t += (10 + 2) * ['# ']
    board.append(t)
 
    # creating one line in the board
    rad = ['# ']
    for r in range(0, 10):
        rad.append("~ ")
    # inserting the new line into the board
    rad.append('# ')
    for k in range(0, 10):
        board.append(list(rad))
    # inserting the lower bounder
    board.append(t)
    return board
 
 
def place_ship(ship, board):
    """
    place ship onto given board
 
    :param ship: given ships name
    :param board: board of given player
    """
    # w = 0
    while True:
        checkcoords = []
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        o = random.randint(0, 1)
        if o == 0:
            ori = "v"  # vertical
        else:
            ori = "h"  # horizontal
        # if ship would be placed outside of the board skip
        if (ori == "v" and y + ships[ship] > 10) or (ori == "h" and x + ships[ship] > 10):
            pass
            # w = 0
        else:
            if ori == "v":
                # vertical placement
                # if no ship is near this position place it
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + i][x + j])
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y + i][x] = ': '
                    break
            #                else:
            #                    w = 0
            elif ori == "h":
                # horizontal placement
                # if no ship is near this position place it
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + j][x + i])
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y][x + i] = ': '
                    break
 
 
#                else:
#                    w = 0
 
 
def place_all_ships(board):
    """
    Place all ships on the given board
 
    :param board: given player board
    """
    for ship in ships:
        for _ in range(0, (5 - ships[ship])):
            place_ship(ship, board)
 
 
def popupwindow(msg):
    """
    Pop up window if game is over
 
    :param msg: player name
    """
    answer = tkMessageBox.askquestion("Game Over", msg + " Would you like to play again?")
    if answer == "yes":
        restart_program()
    elif answer == "no":
        quit()
 
 
def nr_players(number):
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
        player2_or_AI.set("AI")
        AI = True
    else:
        # activate player2 Buttons
        for bt_list in every_button[0]:
            for bt in bt_list:
                bt['state'] = 'normal'
        player2_or_AI.set("Player 2")
 
 
info = StringVar()
player2_or_AI = StringVar()
every_button = []
 
 
def side_labels():
    """
    Create Buttons and Labels for the field
    """
    # info = StringVar()
    Label(root, text="BATTLESHIPS", fg="white", bg="gray19", font=font_big).grid(row=0, column=10, columnspan=9)
    Label(root, textvariable=info, fg="white", bg="gray19", font=font1).grid(row=12, column=6, columnspan=18)
 
    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=_, column=0)
    Button(root, width=7, height=1, text="1 Player", font=font1, fg="white", activebackground="gray19",
           bg="gray19", command=lambda: nr_players(1)).grid(row=2, column=1)
    Button(root, width=7, height=1, text="2 Players", font=font1, fg="white", activebackground="gray19",
           bg="gray19", command=lambda: nr_players(2)).grid(row=3, column=1)
    Label(root, text="Get 20 hits to win", font=font_normal, fg="white", bg="gray19").grid(row=5, column=1)
    Label(root, text="1 Battleship 4 units", font=font_normal, fg="white", bg="gray19").grid(row=6, column=1)
    Label(root, text="2 Battleships 3 units", font=font_normal, fg="white", bg="gray19").grid(row=7, column=1)
    Label(root, text="3 Battleships 2 units", font=font_normal, fg="white", bg="gray19").grid(row=8, column=1)
    Label(root, text="4 Battleships 1 unit  ", font=font_normal, fg="white", bg="gray19").grid(row=9, column=1)
 
    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=_, column=2)
 
    for _ in range(10):
        Label(root, width=20, text="   ", bg="gray19").grid(row=_, column=25)
 
 
def ai_shoots(y_coord, x_coord, player_1_board, ai_score):
    """
    AI shooting method
 
    :param y_coord: y coordinate to shoot at
    :param x_coord: x coordinate to shoot at
    :param player_1_board: board to shoot at
    :param ai_score: score of AI
    """
    # if score is 20, AI has won
    if ai_score == 20:
        popupwindow("The computer has won.")
    # if AI got one hit, destroy complete ship
    if player_1_board[y_coord][x_coord] == ': ':
        ai_score += 1
        player_1_board[y_coord][x_coord] = 'X '
        every_button[0][y_coord - 1][x_coord - 1].configure(text="X", fg="black", bg="red3")
        # depending of where the rest of the ship is located, shot it
        if player_1_board[y_coord - 1][x_coord] == ': ':
            ai_shoots(y_coord - 1, x_coord, player_1_board, ai_score)
        elif player_1_board[y_coord + 1][x_coord] == ': ':
            ai_shoots(y_coord + 1, x_coord, player_1_board, ai_score)
        elif player_1_board[y_coord][x_coord - 1] == ': ':
            ai_shoots(y_coord, x_coord - 1, player_1_board, ai_score)
        elif player_1_board[y_coord][x_coord + 1] == ': ':
            ai_shoots(y_coord, x_coord + 1, player_1_board, ai_score)
        else:
            # shot some random position if ship is destroyed
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            ai_shoots(y, x, player_1_board, ai_score)
    elif player_1_board[y_coord][x_coord] == 'X ' or player_1_board[y_coord][x_coord] == 'O ':
        # if position was already shoot at, try a new position
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        ai_shoots(y, x, player_1_board, ai_score)
    else:
        # if water was hit just change the button
        player_1_board[y_coord][x_coord] = 'O '
        every_button[0][y_coord - 1][x_coord - 1].configure(text="O", fg="white")
 
 
def hit_or_miss(a, b, board, all_buttons, info, player, player_1_hits, player_2_hits, ai_score, board2):
    """
    check if there was a hit or a missed done by the player
 
    :param a: clicked y position
    :param b: clicked x position
    :param board: opponents player board
    :param all_buttons: all buttons of the opponent board
    :param info: write some info to the screen
    :param player: player name
    :param player_1_hits: number of player_1_hits
    :param player_2_hits: number of player_2_hits
    :param ai_score: number of AI hits
    :param board2: own players board
    """
    global AI
    # if a already hit place was clicked again write message
    if board[a + 1][b + 1] == 'O ' or board[a + 1][b + 1] == 'X ':
        info.set("You have already fired there, " + player + "!")
    elif board[a + 1][b + 1] == ': ':
        # if a ship was hit change the button and the players board
        info.set("A hit, nice shot " + player + "!")
        board[a + 1][b + 1] = 'X '
        all_buttons[a][b].configure(text="X", fg="black", bg="red3", activebackground="red3")
        # increase the hit counter and go again
        if player == "player 1":
            player_1_hits += 1
        else:
            player_2_hits += 1
    else:
        # in case of a miss change the button and trigger the AI
        info.set("Seems like you missed that one, " + player + "!")
        board[a + 1][b + 1] = 'O '
        all_buttons[a][b].configure(text="O", fg="White", activeforeground="white")
        # print(AI)
        if AI:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            ai_shoots(y, x, board2, ai_score)
    if player_1_hits == 20 or player_2_hits == 20:
        # if one player got 20 hits he won
        popupwindow(player + " has won!")
 
 
def side(player, allbuttons):
    """
    order the buttons of each player into a grid
 
    :param player: players name
    :param allbuttons: all buttons of this player
    """
    print(player)
    col = 4 if player == "player 1" else 15
    for row in range(10):
        for column in range(10):
            allbuttons[row][column].grid(row=1 + row, column=col + column)
    if player == "player 1":
        label2 = Label(root, text="Player 1", font=font1, fg="white", bg="gray19")
        label2.grid(row=11, column=4, columnspan=10)
    else:
        label3 = Label(root, textvariable=player2_or_AI, font=font1, fg="white", bg="gray19")
        label3.grid(row=11, column=15, columnspan=10)
 
 
def board_buttons(board, info, player, player_1_hits, player_2_hits, ai_score, board2):
    """
    create all buttons for one player
 
    :param board: players board
    :param info: writing info to the screen
    :param player: players name
    :param player_1_hits: number of player 1 hits
    :param player_2_hits: number of player 2 hits
    :param ai_score: AI score
    :param board2: opponents board
    """
    allbuttons = []
    a = 0
    print(AI)
    for i in range(10):
        b = 0
        buttons = []
        for j in range(10):
            button = Button(root, width=2, height=1, font=font1, bg="sky blue", activebackground="sky blue",
                            command=partial(hit_or_miss, a, b, board, allbuttons,
                                            info, player, player_1_hits, player_2_hits, ai_score, board2), state="disable")
            buttons.append(button)
            b += 1
        # create a 2 dimensional array with buttons representing the battle field
        allbuttons.append(list(buttons))
        a += 1
    # store each button matrix in a list for later and global access
    every_button.append(allbuttons)
    side(player, allbuttons)
 
 
def middle_board_space():
    """
    Insert the middel space
    """
    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=1 + _, column=14)
 
 
def main():
    """
    primary game method
    """
    player_1_hits = 0
    player_2_hits = 0
    ai_hits = 0
 
    # initialize the player boards
    player_1_board = player_board()
    player_2_board = player_board()
 
    # place all ships on the boards
    place_all_ships(player_1_board)
    place_all_ships(player_2_board)
 
    # instert side labels
    info = StringVar()
    side_labels()
 
    # create the buttons
    board_buttons(player_1_board, info, "player 1", player_1_hits, player_2_hits, ai_hits, player_2_board)
    middle_board_space()
    board_buttons(player_2_board, info, "player 2", player_1_hits, player_2_hits, ai_hits, player_1_board)
 
 
main()
root.mainloop()