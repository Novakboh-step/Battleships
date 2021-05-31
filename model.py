import random
from controller import Controller
from tkinter import *
from functools import partial


class Model:
    """
    Model object that stores the values of the buttons in the field
    """
    def __init__(self):
        self.ships = {"Aircraft Carrier": 4, "Battleship": 3, "Submarine": 2, "Destroyer": 1}
        self.every_button = []
        self.win_counter = 20
        self.controller = Controller(win_counter=self.win_counter)
        


    def place_all_ships(self,board):
        """
        Place all ships on the given board
    
        :param board: given player board
        """
        for ship in self.ships:
            for _ in range(0, (5 - self.ships[ship])):
                self.place_ship(ship, board)

    def place_ship(self, ship, board):
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
            if (ori == "v" and y + self.ships[ship] > 10) or (ori == "h" and x + self.ships[ship] > 10):
                pass
            else:
                if ori == "v":
                    # vertical placement
                    # if no ship is near this position place it
                    for i in range(-1, (self.ships[ship] + 1)):
                        for j in range(-1, 2):
                            checkcoords.append(board[y + i][x + j])
                    if ': ' not in checkcoords:
                        for i in range(self.ships[ship]):
                            board[y + i][x] = ': '
                        break
                elif ori == "h":
                    # horizontal placement
                    # if no ship is near this position place it
                    for i in range(-1, (self.ships[ship] + 1)):
                        for j in range(-1, 2):
                            checkcoords.append(board[y + j][x + i])
                    if ': ' not in checkcoords:
                        for i in range(self.ships[ship]):
                            board[y][x + i] = ': '
                        break

    def player_board(self):
        """
        generating a 2 dimensional array representing one players board
    
        :return: two dimensional list
        """
        board = []
        t = []
        # creating the upper bound
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

    # def get_buttons(self, root, font):
    #     button_list = ["1 Player", "2 Players"]
    #     for i, button in enumerate(button_list, start=2):
    #         Button(root, width=7, height=1, text=button, font=font, fg="white", activebackground="gray19",
    #             bg="gray19").grid(row=i, column=1)

    def board_buttons(self, root, player1, player2, font):
        """
        create all buttons for one player
    
        :param root: Tk root object
        :param player1: Player 1 object
        :param player2: Player 2 object
        :param font: Tk font
        """
        allbuttons = []
        letter_dict = {
            0 : "A",
            1 : "B",
            2 : "C",
            3 : "D",
            4 : "E",
            5 : "F",
            6 : "G",
            7 : "H",
            8 : "I",
            9 : "J",
        }
        a = 0
        for i in range(10):
            b = 0
            buttons = []
            for j in range(10):
                txt = letter_dict[i]+str(j+1)
                cmd = partial(self.controller.hit_or_miss, a, b, player1, allbuttons, player2)
                button = Button(root, text=txt, width=2, height=1, font=font, bg="sky blue", activebackground="sky blue",
                                command=cmd)
                buttons.append(button)
                b += 1
            # create a 2 dimensional array with buttons representing the battle field
            allbuttons.append(list(buttons))
            a += 1
        # store each button matrix in a list
        self.every_button.append(allbuttons)
        self.side(player1, allbuttons, root, font)

    def side(self, player, allbuttons, root, font):
        """
        order the buttons of each player into a grid
    
        :param player: Player object
        :param allbuttons: All buttons of this player
        :param root: Tk root object
        :param font: Tk font
        """
        col = 4 if player.name == "player 1" else 15


        for row in range(10):
            for column in range(10):
                allbuttons[row][column].grid(row=1 + row, column=col + column)
        if player.name == "player 1":
            label2 = Label(root, text="Player 1", font=font, fg="white", bg="gray19")
            label2.grid(row=11, column=4, columnspan=10)
            label3 = Label(root, textvariable=player.score, font=font,fg="white", bg="gray19")
            label3.grid(row=12, column=4, columnspan=10)
        else:
            label4 = Label(root, text="Player 2", font=font, fg="white", bg="gray19")
            label4.grid(row=11, column=15, columnspan=10)
            label5 = Label(root, textvariable=player.score, font=font,fg="white", bg="gray19")
            label5.grid(row=12, column=15, columnspan=10)

class Player:
    """
    Player object that stores information about each player

    :param model: associated model
    :param name: Name string
    :param id: Player id int
    """
    def __init__(self, model, name, id) -> None:
        self.board = model.player_board()
        self.name = name
        self.hits = 0
        model.place_all_ships(self.board)
        self.id = id
        self.score = StringVar()
        self.score.set(f"Score: {self.hits}")
