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
        self.pos = [0,0]
        self.direction = math.pi/4
        self.speed_vector = [(speed * math.cos(self.direction)),(speed * math.sin(self.direction))]
        self.speed_magnitude = speed
    def move_diagonal(self, time_interval):
        new_pos = [(self.pos[0] + self.speed_vector[0] * time_interval),(self.pos[1] + self.speed_vector[1] * time_interval)]
        if new_pos[0] < 0 or new_pos[1] > self.lake.side_length:
            self.direction = math.pi - self.direction  # Reflect direction horizontally
            self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
            new_pos[0] = max(0, min(new_pos[0], self.lake.side_length))
        if new_pos[1] < 0 or new_pos[1] > self.lake.side_length:
            self.direction = -self.direction  # Reflect direction vertically
            self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
            new_pos[1] = max(0, min(new_pos[1], self.lake.side_length))
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
    
    def get_position(self):
        return self.pos

class Fish:
    def __init__(self, lake, speed):
        self.lake = lake
        self.pos = [int(random.uniform(0, lake.side_length)),int(random.uniform(0, lake.side_length))]
        self.direction = random.uniform(0, 2 * math.pi) 
        self.speed_vector = [(speed * math.cos(self.direction)),(speed * math.sin(self.direction))]
        self.speed_magnitude = speed
    def move(self, time_interval):
        new_pos = [(self.pos[0] + self.speed_vector[0] * time_interval),(self.pos[1] + self.speed_vector[1] * time_interval)]
        if new_pos[0] < 0 or new_pos[0] > self.lake.side_length:
            self.direction = math.pi - self.direction  # Reflect direction horizontally
            self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
            new_pos[0] = max(0, min(new_pos[0], self.lake.side_length))

        if new_pos[1]< 0 or new_pos[1] > self.lake.side_length:
            self.direction = -self.direction  # Reflect direction vertically
            self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
            new_pos[1] = max(0, min(new_pos[1], self.lake.side_length))
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]

    def change_direction(self):
        self.direction = random.uniform(0, 2 * math.pi)
        print(f"New Direction: {self.direction}")
        self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
    def get_position(self):
        return self.pos

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
        change_time = 0
        def update(frame):
            fish_pos = fish.get_position()
            boat_pos = boat.get_position()
            nonlocal elapsed_time
            nonlocal change_time
            change_time += time_step
            elapsed_time += time_step
            print(f"Frame {frame}, Time {elapsed_time:.1f}s, Fish at {fish_pos}, Boat at {boat_pos}")
    # Move fish and boat
            boat.move_diagonal(time_step)
    # Change fish direction at intervals
            if change_time >= direction_change_interval:
                fish.change_direction()
                change_time = 0
                print("Fish changed direction")
            fish.move(time_step)
    # Update positions
            fish_marker.set_data([fish_pos[0]], [fish_pos[1]])
            boat_marker.set_data([boat_pos[0]], [boat_pos[1]])

    # Stop if they meet
            if math.sqrt((fish_pos[0] - boat_pos[0])**2) + ((fish_pos[1] - boat_pos[1])**2)<= 2 :
                ani.event_source.stop()
                print(f"Fish met boat at position {fish_pos[0]}','{fish_pos[1]} at time {elapsed_time:.1f} seconds.")

            return fish_marker, boat_marker
        ani = animation.FuncAnimation(fig, update, frames=200, interval=time_step * 1000, blit=False)
        plt.show()

    lake_area = 1000
    fish_speed = 9
    boat_speed = 10
    lake = Lake(lake_area)
    fish = Fish(lake, fish_speed)
    boat = Boat(lake, boat_speed)
    time_step = 0.1
    direction_change_interval = 0.8
    visualize_movement(lake, fish, boat, time_step, direction_change_interval)
    
