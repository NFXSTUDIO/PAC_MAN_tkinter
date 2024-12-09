class Map:
    """
    Class to manage the map game
    
    """
    def __init__(self, canvas):
        """
        Initialisation function of the class

        Args:
            canvas (tkinter canvas): canvas to display the map of the game
        """
        self.canvas = canvas
        self.wall_coords = self.generate_map()

    def generate_map(self):
        """
        Function to generate the map

        Returns:
            list: return where are the walls 
        """
        map_ = [
            "0000000000000000000000000",
            
            "0111111111111111111111110",
            "0100000000001000000000010",
            "0101110111101011110111010",
            "0101110111101011110111010",
            "0100000000000000000000010",
            "0101110110111110110111010",
            "0100000110001000110000010",
            "0111110111000001110111110",
            "0111110100000000010111110",
            "0111110101110111010111110",
            "0100000101000001010000010",
            "0101100001000001000011010",
            "0100000101000001010000010",
            "0111110101111111010111110",
            "0111110100000000010111110",
            "0111110111000001110111110",
            "0100000110001000110000010",
            "0101110110111110110111110",
            "0100000000000000000000010",
            "0101110111101011110111010",
            "0101110111101011110111010",
            "0100000000000000000000010",
            "0111111111111111111111110",
            
            "0000000000000000000000000"
        ]

        wall_coords = []
        cell_size = 30
        for y, row in enumerate(map_):
            for x, cell in enumerate(row):
                if cell == "1": # When the cell is equal to 1, it's a wall so we draw a line
                    x1, y1 = x * cell_size, y * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    self.canvas.create_line(x1, y1, x2, y1, fill="white", width=0.5)
                    self.canvas.create_line(x1, y1, x1, y2, fill="white", width=0.5)
                    self.canvas.create_line(x2, y1, x2, y2, fill="white", width=0.5)
                    self.canvas.create_line(x1, y2, x2, y2, fill="white", width=0.5)
                    wall_coords.append((x1, y1, x2, y2))
                
        return wall_coords

    def check_collision(self, new_x, new_y):
        """
        Check if the player hit a wall or not by the wall and the player coords.
        
        Args:
            new_x (int): x coords of the player
            new_y (int): y coords of the player

        Returns:
            bool : return True if the player hit a wall, False if not
        """
        for (x1, y1, x2, y2) in self.wall_coords:
            if x1 <= new_x <= x2 and y1 <= new_y <= y2: # Check if the player's coords (new_x, new_y) are between the coords of the wall
                return True # The player hit the wall
            
        return False