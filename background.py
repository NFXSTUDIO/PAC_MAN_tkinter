from PIL import ImageTk, Image
import json

class Background:
    def __init__(self, canvas):
        self.canvas = canvas
        self.background_image = self.load_images()
        
    def load_images(self):
        with open("map.json", "r") as file:
            data = json.load(file)
            
        background_image = ImageTk.PhotoImage(Image.open(data["background"]["background_images"][0]))
        
        return background_image
    
    def display_background(self, width, height):
        self.canvas.image = self.background_image
        self.canvas.create_image(width / 2, height / 2, image = self.background_image)