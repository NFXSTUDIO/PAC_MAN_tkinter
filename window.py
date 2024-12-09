from customtkinter import CTkCanvas
from pacman import Pacman
from map import Map

class Window:
    """
    Class to manage the main window
    """
    def __init__(self, master):
        """
        Initialisation of the class

        Args:
            master (tkinter): main tkinter window
        """
        self.master = master
        self.show_game()
        
    def show_game(self):
        """
        Function to display the game
        """
        master_width, master_height = 600, 600
        self.master.geometry(f"{master_width}x{master_height}")

        main_canvas = CTkCanvas(self.master, width=master_width, height=master_height, bg="black")
        main_canvas.pack(fill="both", expand=True)
    
        #background = Background(main_canvas, master_width, master_height)
        #background.display_background()
        
        map_ = Map(main_canvas)
        
        pacman = Pacman(main_canvas, 375, 375, map_)

        self.master.bind("<KeyPress>", pacman.move)
