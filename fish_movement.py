import random
import math
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Lake:
    def __init__(self, area):
        self.area = area
        self.side_length = math.sqrt(area)  # Calculate the side length of the square lake

class Boat:
    def __init__(self,lake,speed):
        self.lake = lake
        self.speed = speed
        self.x = 0
        self.y = 0
        self.direction = math.pi/4
    
    def move_diagonal(self, time_interval):
        speed_x = self.speed * math.cos(self.direction)
        speed_y = self.speed * math.sin(self.direction)
        new_x = self.x + speed_x * time_interval
        new_y = self.y + speed_y * time_interval
        if new_x < 0 or new_x > self.lake.side_length:
            self.direction = math.pi - self.direction  # Reflect direction horizontally
            new_x = max(0, min(new_x, self.lake.side_length))
        if new_y < 0 or new_y > self.lake.side_length:
            self.direction = -self.direction  # Reflect direction vertically
            new_y = max(0, min(new_y, self.lake.side_length))
        self.x = new_x
        self.y = new_y
    
    def get_position(self):
        return [round(self.x), round(self.y)]



class Fish:
    def __init__(self, lake, speed):

        self.lake = lake
        self.speed = speed
        self.x = int(random.uniform(0, lake.side_length))
        self.y = int(random.uniform(0, lake.side_length))
        self.direction = random.uniform(0, 2 * math.pi) 

    def move(self, time_interval):
        speed_x = self.speed * math.cos(self.direction)
        speed_y = self.speed * math.sin(self.direction)
        new_x = self.x + speed_x * time_interval
        new_y = self.y + speed_y * time_interval
        if new_x < 0 or new_x > self.lake.side_length:
            self.direction = math.pi - self.direction  # Reflect direction horizontally
            new_x = max(0, min(new_x, self.lake.side_length))

        if new_y < 0 or new_y > self.lake.side_length:
            self.direction = -self.direction  # Reflect direction vertically
            new_y = max(0, min(new_y, self.lake.side_length))

        self.x = new_x
        self.y = new_y

    def change_direction(self):
        self.direction = random.uniform(0, 2 * math.pi)

    def get_position(self):
        return [round(self.x), round(self.y)]

# Example Usage
if __name__ == "__main__":
    def visualize_movement(lake, fish, boat, time_step, direction_change_interval):
        fig, ax = plt.subplots()
        ax.set_xlim(0, lake.side_length)
        ax.set_ylim(0, lake.side_length)
        ax.set_title("Fish and Boat Movement in a Lake")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
    
        fish_marker, = ax.plot([], [], 'bo', label="Fish")  # Blue for Fish
        boat_marker, = ax.plot([], [], 'ro', label="Boat")  # Red for Boat
        ax.legend()

        elapsed_time = 0

        def update(frame):
            nonlocal elapsed_time
            elapsed_time += time_step
            print(f"Frame {frame}, Time {elapsed_time:.1f}s, Fish at {fish.get_position()}, Boat at {boat.get_position()}")

    # Move fish and boat
            fish.move(time_step)
            boat.move_diagonal(time_step)

    # Change fish direction at intervals
            if elapsed_time % direction_change_interval == 0:
                fish.change_direction()
                print("Fish changed direction")

    # Update positions
            fish_marker.set_data([fish.x], [fish.y])
            boat_marker.set_data([boat.x], [boat.y])

    # Stop if they meet
            if round(fish.x) == round(boat.x) and round(fish.y) == round(boat.y):
                ani.event_source.stop()
                print(f"Fish met boat at position {fish.get_position()} at time {elapsed_time:.1f} seconds.")

            return fish_marker, boat_marker
        ani = animation.FuncAnimation(fig, update, frames=200, interval=time_step * 1000, blit=False)
        plt.show()

    lake_area = 1000
    fish_speed = 9
    boat_speed = 10
    lake = Lake(lake_area)
    fish = Fish(lake, fish_speed)
    boat = Boat(lake, boat_speed)
    time_step = 0.2
    direction_change_interval = 2.0
    visualize_movement(lake, fish, boat, time_step, direction_change_interval)
    
