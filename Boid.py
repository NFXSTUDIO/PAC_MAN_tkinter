import tkinter as tk
import random
from itertools import cycle
import math


class Ghost:
    def __init__(self, canvas, x, y, animation_frames, all_ghosts, frame_interval=100, max_speed=10,
                 perception_radius=100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.all_ghosts = all_ghosts  # Keep track of all ghosts for collision detection
        self.frame_interval = frame_interval
        self.animation_running = False  # Flag to prevent multiple timers
        self.max_speed = max_speed  # Maximum speed of the ghost
        self.perception_radius = perception_radius  # Radius within which other ghosts are "perceived"

        # Load images and store iterators for animations
        self.animations = {
            direction: cycle([tk.PhotoImage(file=frame) for frame in frames])
            for direction, frames in animation_frames.items()
        }
        self.current_image = self.canvas.create_image(x, y, image=next(self.animations["down"]), anchor=tk.CENTER)
        self.current_animation = "down"
        self.velocity = [0, 0]  # Initial velocity of the ghost

    def move(self, dx, dy, direction):
        """Move the ghost and play the animation in the given direction."""
        self.current_animation = direction
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collisions before moving
        if self.check_collision(new_x, new_y):
            return  # If collision is detected, don't move

        # Move the ghost
        self.x = new_x
        self.y = new_y
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

    def update_velocity(self):
        """Update the ghost's velocity based on Boid behaviors."""
        alignment = self.align()
        cohesion = self.cohesion()
        separation = self.separate()

        # Apply the behaviors to velocity
        self.velocity[0] += alignment[0] + cohesion[0] + separation[0]
        self.velocity[1] += alignment[1] + cohesion[1] + separation[1]

        # Limit velocity to max speed
        speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if speed > self.max_speed:
            self.velocity[0] = (self.velocity[0] / speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed) * self.max_speed

        # Move the ghost
        self.move(self.velocity[0], self.velocity[1], "down" if self.velocity[1] > 0 else "up")

    def align(self):
        """Align with the average direction of nearby ghosts."""
        steering = [0, 0]
        count = 0
        for ghost in self.all_ghosts:
            if ghost != self and self.distance(ghost) < self.perception_radius:
                steering[0] += ghost.velocity[0]
                steering[1] += ghost.velocity[1]
                count += 1

        if count > 0:
            steering[0] /= count
            steering[1] /= count

        # Avoid too much alignment
        speed = math.sqrt(steering[0] ** 2 + steering[1] ** 2)
        if speed > self.max_speed:
            steering[0] = (steering[0] / speed) * self.max_speed
            steering[1] = (steering[1] / speed) * self.max_speed

        return steering

    def cohesion(self):
        """Move towards the average position of nearby ghosts."""
        center_of_mass = [0, 0]
        count = 0
        for ghost in self.all_ghosts:
            if ghost != self and self.distance(ghost) < self.perception_radius:
                center_of_mass[0] += ghost.x
                center_of_mass[1] += ghost.y
                count += 1

        if count > 0:
            center_of_mass[0] /= count
            center_of_mass[1] /= count

            # Move towards the center of mass
            steering = [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
            return steering
        return [0, 0]

    def separate(self):
        """Avoid crowding or colliding with nearby ghosts."""
        steering = [0, 0]
        count = 0
        for ghost in self.all_ghosts:
            if ghost != self and self.distance(ghost) < self.perception_radius / 2:
                diff = [self.x - ghost.x, self.y - ghost.y]
                distance = self.distance(ghost)
                if distance > 0:
                    diff[0] /= distance
                    diff[1] /= distance

                steering[0] += diff[0]
                steering[1] += diff[1]
                count += 1

        if count > 0:
            steering[0] /= count
            steering[1] /= count

        return steering

    def distance(self, ghost):
        """Calculate the distance between this ghost and another ghost."""
        return math.sqrt((self.x - ghost.x) ** 2 + (self.y - ghost.y) ** 2)

    def check_collision(self, target_x, target_y):
        """Check if a position is already occupied by another ghost."""
        for ghost in self.all_ghosts:
            if ghost != self:  # Don't check collision with itself
                ghost_x, ghost_y = ghost.x, ghost.y
                distance = ((target_x - ghost_x) ** 2 + (target_y - ghost_y) ** 2) ** 0.5
                if distance < 50:  # Adjust the threshold for collision detection
                    return True  # Collision detected
        return False

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
            self._move_right(abs(dx / 10), target_y)  # Move right
        elif dx < 0:
            self._move_left(abs(dx / 10), target_y)  # Move left

    def _move_horizontally(self, dx, target_y):
        """Move the ghost along the x-axis to target_x first."""
        if dx > 0:
            self._move_right(abs(dx / 10), target_y)  # Move right
        elif dx < 0:
            self._move_left(abs(dx / 10), target_y)  # Move left

    def _move_vertically(self, dy):
        """Once horizontal movement is done, move vertically to target_y."""
        if dy > 0:
            self._move_down(abs(dy / 10))  # Move down
        elif dy < 0:
            self._move_up(abs(dy / 10))  # Move up

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
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()),
              animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()),
              animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()),
              animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()),
              animation_frames, []),
        Ghost(canvas, random.randint(0, canvas.winfo_screenwidth()), random.randint(0, canvas.winfo_screenheight()),
              animation_frames, []),
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


    # Start Boid-like behavior
    def update():
        for ghost in ghosts:
            ghost.update_velocity()  # Update the ghost's movement based on Boid behaviors
        root.after(50, update)  # Update every 50ms


    update()  # Start the update loop

    root.mainloop()
