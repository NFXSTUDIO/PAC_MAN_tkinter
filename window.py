from customtkinter import CTk, CTkCanvas
from background import Background
from pacman import Pacman

class Window:
    def __init__(self, master):
        self.master = master
        self.show_game()
        
    def show_game(self):
        master_width, master_height = 600, 600
        self.master.geometry(f"{master_width}x{master_height}")

        main_canvas = CTkCanvas(self.master, width=master_width, height=master_height, bg="black")
        main_canvas.pack(fill="both", expand=True)

        background = Background(main_canvas)
        background.display_background(master_width, master_height)

        pacman = Pacman(main_canvas, 200, 200)

        self.master.bind("<KeyPress>", pacman.move)

        self.master.mainloop()