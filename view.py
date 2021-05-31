from tkinter import *
from model import Model, Player
from tkinter.font import Font


class View:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BATTLESHIPS")
        self.root.configure(background='gray19')
        self.font1 = Font(family='Helvetica', size=12, weight='bold')
        self.font_big = Font(family='Helvetica', size=16, weight='bold')
        self.font_normal = Font(family='Helvetica', size=10, weight='normal')
        self.model = Model()
        player1 = Player(name="player 1", model=self.model, id=1)
        player2 = Player(name="player 2", model=self.model, id=2)
        self.info = "some text"

        # insert side labels
        self.side_labels()
    
        # create the buttons
        self.model.board_buttons(root=self.root, player1=player1, player2=player2, font=self.font1)
        self.middle_board_space()
        self.model.board_buttons(root=self.root, player1=player2, player2=player1, font=self.font1)

    
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
        # info = StringVar()
        Label(self.root, text="BATTLESHIPS", fg="white", bg="gray19", font=self.font_big).grid(row=0, column=10, columnspan=9)
        Label(self.root, textvariable=self.info, fg="white", bg="gray19", font=self.font1).grid(row=12, column=6, columnspan=18)
    
        for _ in range(10):
            Label(self.root, text="   ", bg="gray19").grid(row=_, column=0)
        # self.model.get_buttons(root=self.root, font=self.font1)
        Label(self.root, text=f"Get {self.model.win_counter} hits to win", font=self.font_normal, fg="white", bg="gray19").grid(row=5, column=1)
    
        for _ in range(10):
            Label(self.root, text="   ", bg="gray19").grid(row=_, column=2)
    
        for _ in range(10):
            Label(self.root, width=20, text="   ", bg="gray19").grid(row=_, column=25)
 