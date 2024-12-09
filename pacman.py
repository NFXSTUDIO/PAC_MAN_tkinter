import json
from PIL import ImageTk, Image

class Pacman:
    """
    Class to manage the pacman
    
    """
    def __init__(self, canvas, position_x, position_y, map_):
        """
        Initialisation function of the class

        Args:
            canvas (tkinter): canvas to create the pacman
            position_x (int): position of pacman on x
            position_y (int): position of pacman on y
            map_ (None): map of the game
        """
        self.canvas = canvas
        self.position_x = position_x
        self.position_y = position_y
        self.speed = 10
        self.current_direction = "Right"
        self.pacman_image = self.load_images()
        self.map_ = map_
        
        self.image_sprite = self.canvas.create_image(
            self.position_x, self.position_y, image=self.pacman_image["Right"][0], anchor="center"
        )
        
    def load_images(self):
        """
        Function to load the images of pacman
        
        Return the image wanted according to the json file
        """
        with open("map.json", "r") as file:
            data = json.load(file)

        pacman_image = {}
        for pacman_direction, paths in data["pacman_directions"].items():
            pacman_image[pacman_direction] = [ImageTk.PhotoImage(Image.open(path)) for path in paths]
        
        return pacman_image
        
    def move(self, event):
        """
        Function to move the pacman

        Args:
            event (tkinter event): use to use the keyboard
        """
        new_x = self.position_x
        new_y = self.position_y
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if event.keysym == "Right":         # The sprite go to the right
            new_x += self.speed
            self.current_direction = "Right"
        elif event.keysym == "Left":        # The sprite go to the left
            new_x -= self.speed
            self.current_direction = "Left"
        elif event.keysym == "Up":          # The sprite go up
            new_y -= self.speed
            self.current_direction = "Up"
        elif event.keysym == "Down":        # The sprite go down
            new_y += self.speed
            self.current_direction = "Down"
            
        # Check if the player hit a wall
        if 1 <= new_x <= canvas_width - 1 and 1 <= new_y <= canvas_height - 1:
            if not self.map_.check_collision(new_x, new_y):
                self.position_x, self.position_y = new_x, new_y
        
        # Update the position & the image
        self.canvas.coords(self.image_sprite, self.position_x, self.position_y)
        self.canvas.itemconfig(self.image_sprite, image=self.pacman_image[self.current_direction][0])
