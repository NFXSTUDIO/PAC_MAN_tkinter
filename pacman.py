import json
from PIL import ImageTk, Image

class Pacman:
    def __init__(self, canvas, position_x, position_y):
        self.canvas = canvas
        self.position_x = position_x
        self.position_y = position_y
        self.speed = 10
        self.current_direction = "Right"
        self.pacman_image = self.load_images()
        
        self.image_sprite = self.canvas.create_image(
            self.position_x, self.position_y, image=self.pacman_image["Right"][0], anchor="center"
        )
        
    def load_images(self):
        with open("map.json", "r") as file:
            data = json.load(file)

        pacman_image = {}
        for pacman_direction, paths in data["pacman_directions"].items():
            pacman_image[pacman_direction] = [ImageTk.PhotoImage(Image.open(path)) for path in paths]
        
        return pacman_image
        
    def move(self, event):
        if event.keysym == "Right":         # The sprite go to the right
            self.position_x += self.speed
            self.current_direction = "Right"
        elif event.keysym == "Left":        # The sprite go to the left
            self.position_x -= self.speed
            self.current_direction = "Left"
        elif event.keysym == "Up":          # The sprite go up
            self.position_y -= self.speed
            self.current_direction = "Up"
        elif event.keysym == "Down":        # The sprite go down
            self.position_y += self.speed
            self.current_direction = "Down"
        
        # Update the position & the image
        self.canvas.coords(self.image_sprite, self.position_x, self.position_y)
        self.canvas.itemconfig(self.image_sprite, image=self.pacman_image[self.current_direction][0])