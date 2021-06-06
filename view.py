from tkinter import *
from tkinter.font import Font
from controller import Controller
from functools import partial



class View:
    """
    View object which creates the user interface
    """
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BATTLESHIPS")
        self.root.configure(background='gray19')
        self.font1 = Font(family='Helvetica', size=12, weight='bold')
        self.font_big = Font(family='Helvetica', size=16, weight='bold')
        self.font_normal = Font(family='Helvetica', size=10, weight='normal')
        self.controller = Controller()
        players = self.controller.get_players()

        # insert side labels
        self.side_labels()
    
        # create the buttons
        self.board_buttons(player1=players[0], player2=players[1], font=self.font1)
        self.middle_board_space()
        self.board_buttons(player1=players[1], player2=players[0], font=self.font1)
        

    
    def middle_board_space(self):
        """
        Insert the middel space
        """
        for _ in range(10):
            Label(self.root, text="   ", bg="gray19").grid(row=1 + _, column=14)
 
    
    def side_labels(self):
        """
        Create Buttons and Labels for the field
        """
        Label(self.root, text="BATTLESHIPS", fg="white", bg="gray19", font=self.font_big).grid(row=0, column=10, columnspan=9)
    
        for _ in range(10):
            Label(self.root, text="   ", bg="gray19").grid(row=_, column=0)
        Label(self.root, text=f"Get {self.controller.win_counter} hits to win", font=self.font_big, fg="white", bg="gray19").grid(row=3, column=1)
        Label(self.root, textvariable=self.controller.get_turn(), font=self.font_big, fg="white", bg="gray19").grid(row=5, column=1)
        Label(self.root, textvariable=self.controller.get_info(), font=self.font_big, fg="white", bg="gray19", width=25).grid(row=7, column=1)
        cmd = partial(self.controller.restart_program)
        Button(self.root, text="Restart game", font=self.font_big, fg="white", bg="gray19", command=cmd).grid(row=9, column=1)
    
        for _ in range(10):
            Label(self.root, text="   ", bg="gray19").grid(row=_, column=2)
    
        for _ in range(10):
            Label(self.root, width=20, text="   ", bg="gray19").grid(row=_, column=25)
 
    def board_buttons(self, player1, player2, font):
            """
            create all buttons for one player
        
            :param player1: Player 1 object
            :param player2: Player 2 object
            :param font: Tk font
            """
            all_buttons = []
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
                    cmd = partial(self.controller.hit_or_miss, a, b, player1, all_buttons, player2, self.root)
                    button = Button(self.root, text=txt, width=2, height=1, font=font, bg="sky blue", activebackground="sky blue",
                                    command=cmd)
                    buttons.append(button)
                    b += 1
                # create a 2 dimensional array with buttons representing the battle field
                all_buttons.append(list(buttons))
                a += 1
            # store each button matrix in a list

            self.controller.add_buttons(all_buttons)
            self.side(player1, all_buttons, font)

    def side(self, player, allbuttons, font):
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
            label2 = Label(self.root, text="Player 1", font=font, fg="white", bg="gray19")
            label2.grid(row=11, column=4, columnspan=10)
            label3 = Label(self.root, textvariable=player.score, font=font,fg="white", bg="gray19")
            label3.grid(row=12, column=4, columnspan=10)
        else:
            label4 = Label(self.root, text="Player 2", font=font, fg="white", bg="gray19")
            label4.grid(row=11, column=15, columnspan=10)
            label5 = Label(self.root, textvariable=player.score, font=font,fg="white", bg="gray19")
            label5.grid(row=12, column=15, columnspan=10)
