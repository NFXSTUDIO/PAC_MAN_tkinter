import tkinter as tk
import random
from itertools import cycle


class Ghost:
    def __init__(self, canvas, x, y, animation_frames, all_ghosts, frame_interval=100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.all_ghosts = all_ghosts  # Keep track of all ghosts for collision detection
        self.frame_interval = frame_interval
        self.animation_running = False  # Flag to prevent multiple timers

        # Load images and store iterators for animations
        self.animations = {
            direction: cycle([tk.PhotoImage(file=frame) for frame in frames])
            for direction, frames in animation_frames.items()
        }
        self.current_image = self.canvas.create_image(x, y, image=next(self.animations["down"]), anchor=tk.CENTER)
        self.current_animation = "down"

    def move(self, dx, dy, direction):
        """Move the ghost and play the animation in the given direction."""
        self.current_animation = direction
        self.x += dx
        self.y += dy
        self.canvas.move(self.current_image, dx, dy)
        if not self.animation_running:
            self.animate()

    def animate(self):
        """Update the animation frame."""
        frame = next(self.animations[self.current_animation])
        self.canvas.itemconfig(self.current_image, image=frame)

        # Set a timer to call animate again after the interval
        self.animation_running = True
        self.canvas.after(self.frame_interval, self.update_animation)

    def update_animation(self):
        """Continue animation by calling animate."""
        self.animation_running = False
        self.animate()

    def move_down(self):
        self.move(0, 10, "down")

    def move_up(self):
        self.move(0, -10, "up")

    def move_left(self):
        self.move(-10, 0, "left")

    def move_right(self):
        self.move(10, 0, "right")

    def move_to(self, target_x, target_y):
        """Move to the target coordinates following the x-axis first, then the y-axis."""
        dx = target_x - self.x
        dy = target_y - self.y

        # Move horizontally first
        if dx > 0:
            self._move_right(abs(dx/10), target_y)  # Move right
        elif dx < 0:
            self._move_left(abs(dx/10), target_y)  # Move left

    def _move_horizontally(self, dx, target_y):
        """Move the ghost along the x-axis to target_x first."""
        if dx > 0:
            self._move_right(abs(dx/10), target_y)  # Move right
        elif dx < 0:
            self._move_left(abs(dx/10), target_y)  # Move left

    def _move_vertically(self, dy):
        """Once horizontal movement is done, move vertically to target_y."""
        if dy > 0:
            self._move_down(abs(dy/10))  # Move down
        elif dy < 0:
            self._move_up(abs(dy/10))  # Move up

    def _move_right(self, steps, target_y):
        """Move right step by step until the x-coordinate is reached."""
        if steps > 0:
            self.move(10, 0, "right")
            self.canvas.after(self.frame_interval, self._move_right, steps - 1, target_y)
        else:
            # Once horizontal movement is done, move vertically to target_y
            self.canvas.after(500, self._move_vertically, target_y - self.y)

    def _move_left(self, steps, target_y):
        """Move left step by step until the x-coordinate is reached."""
        if steps > 0:
            self.move(-10, 0, "left")
            self.canvas.after(self.frame_interval, self._move_left, steps - 1, target_y)
        else:
            # Once horizontal movement is done, move vertically to target_y
            self.canvas.after(500, self._move_vertically, target_y - self.y)

    def _move_down(self, steps):
        """Move down step by step."""
        if steps > 0:
            self.move(0, 10, "down")
            self.canvas.after(self.frame_interval, self._move_down, steps - 1)
        else:
            self.canvas.after(500, self.move_to_next_random)

    def _move_up(self, steps):
        """Move up step by step."""
        if steps > 0:
            self.move(0, -10, "up")
            self.canvas.after(self.frame_interval, self._move_up, steps - 1)
        else:
            self.canvas.after(500, self.move_to_next_random)

    def move_to_next_random(self):
        """Move the ghost to a random position, checking for collisions before moving."""
        while True:
            target_x = random.randint(10, self.canvas.winfo_width() - 10)
            target_y = random.randint(30, self.canvas.winfo_height() - 10)

            # Check for collision with other ghosts
            if not self.check_collision(target_x, target_y):
                break  # No collision, exit the loop

        # Move the ghost to the first location
        self.move_to(target_x, target_y)

    def check_collision(self, target_x, target_y):
        """Check if a position is already occupied by another ghost."""
        for ghost in self.all_ghosts:
            if ghost != self:  # Don't check collision with itself
                ghost_x, ghost_y = ghost.x, ghost.y
                distance = ((target_x - ghost_x) ** 2 + (target_y - ghost_y) ** 2) ** 0.5
                if distance < 50:  # Adjust the threshold for collision detection
                    return True  # Collision detected
        return False


# Example usage
if __name__ == "__main__":
    # Sample frame paths for each direction
    animation_frames = {
        "down": ["down_blinky_1.png", "down_blinky_2.png"],
        "up": ["up_blinky_1.png", "up_blinky_2.png"],
        "left": ["left_blinky_1.png", "left_blinky_2.png"],
        "right": ["right_blinky_1.png", "right_blinky_2.png"]
    }

    root = tk.Tk()
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black")
    canvas.pack()

    # Create a list of all ghosts for collision detection
    ghosts = [
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()), animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()), animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()), animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()), animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()), animation_frames, []),
    ]

    # Update the `all_ghosts` list for each ghost
    for ghost in ghosts:
        ghost.all_ghosts = ghosts

    def start_random_movement(event):
        """Start moving the ghost to random positions when the "E" key is pressed."""
        for ghost in ghosts:
            ghost.move_to_next_random()  # Start the movement sequence

    # Bind the "E" key to start the random movement
    root.bind("<e>", start_random_movement)

    root.mainloop()
