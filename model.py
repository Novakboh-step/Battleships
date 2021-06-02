import random
from tkinter import *


class Model:
    """
    Model object that stores the values of the buttons in the field
    """
    def __init__(self):
        self.every_button = []
        pass

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


    
class Player(Model):
    """
    Player object that stores information about each player

    :param model: associated model
    :param name: Name string
    :param id: Player id int
    """
    def __init__(self, model, name, id) -> None:
        super()
        self.ships = {"Aircraft Carrier": 4, "Battleship": 3, "Submarine": 2, "Destroyer": 1}

        self.board = self.player_board()
        self.name = name
        self.hits = 0
        self.place_all_ships(self.board)
        self.id = id
        self.score = StringVar()
        self.score.set(f"Score: {self.hits}")
