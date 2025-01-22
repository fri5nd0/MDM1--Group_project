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
    def set_position(self):
        self.pos = [0,0]

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
        self.speed_vector = [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
    def get_position(self):
        return self.pos
    def set_position(self):
        self.pos = [int(random.uniform(0, self.lake.side_length)),int(random.uniform(0, self.lake.side_length))]

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
            boat_pos = boat.get_position()# Update positions
            nonlocal elapsed_time
            if math.sqrt((fish_pos[0] - boat_pos[0])**2) + ((fish_pos[1] - boat_pos[1])**2)<= 2 :
                ani.event_source.stop()
                print(f"Fish met boat at position {fish_pos[0]}','{fish_pos[1]} at time {elapsed_time:.1f} seconds.")#stop if they have met before the update in position   
            fish_marker.set_data([fish_pos[0]], [fish_pos[1]])
            boat_marker.set_data([boat_pos[0]], [boat_pos[1]])
            nonlocal change_time #FOr direction change
            change_time += time_step
            elapsed_time += time_step
            print(f"Frame {frame}, Time {elapsed_time:.1f}s, Fish at {fish_pos}, Boat at {boat_pos}")
            boat.move_diagonal(time_step)# Move fish and boat
            if change_time >= direction_change_interval:
                fish.change_direction()
                change_time = 0# Change fish direction at intervals
                print("Fish changed direction")
            fish.move(time_step)
            return fish_marker, boat_marker
        ani = animation.FuncAnimation(fig, update, frames=200, interval=time_step * 1000, blit=False)
        plt.show()
        fish.set_position()
        boat.set_position()
        return elapsed_time
    def quick_simulation(fish, boat, time_step, direction_change_interval):
        elapsed_time = 0
        change_time = 0
        while True:
            fish_pos = fish.get_position()
            boat_pos = boat.get_position()
            elapsed_time += time_step
            change_time += time_step

        # Move boat and fish
            boat.move_diagonal(time_step)
            fish.move(time_step)
            if change_time >= direction_change_interval:
                fish.change_direction()
                change_time = 0         # Change fish direction at intervals

            if math.sqrt((fish_pos[0] - boat_pos[0]) ** 2 + (fish_pos[1] - boat_pos[1]) ** 2) <= 2:
                print(f"Fish met boat at position {fish_pos} when boat was at {boat_pos} at time {elapsed_time:.1f} seconds.")
                break # Check if they meet and end this sample
        fish.set_position()#reset positions for the next sample
        boat.set_position()
        return elapsed_time
    
    def get_samples(change_var):
        average_times = []
        change_var_list = []
        ranges = {
            'a': range(20, 1001, 20),  # Lake Area
            'f': range(1, 31),         # Fish Speed
            'b': range(1, 31)          # Boat Speed
        }#defined ranges for all samples
        for value in ranges[change_var]:
            lake_area = 1000 #default values
            fish_speed = 9
            boat_speed = 12
            if change_var == 'a':
                lake_area = value
            elif change_var == 'f':
                fish_speed = value
            elif change_var == 'b':
                boat_speed = value#value is set depending on the independent variable('change_var')
            lake = Lake(lake_area)
            fish = Fish(lake, fish_speed)
            boat = Boat(lake, boat_speed)
            time = 0
            samples = 0
            while samples <= 1000:
                time += quick_simulation(fish, boat, time_step, direction_change_interval)
                samples += 1
            average = time / samples
            average_times.append(average)
            change_var_list.append(value)
            print(f"Average time to meet was: {average:.2f} \nFor {change_var} value: {value}")# Store results
        return [average_times,change_var_list]
                
    time_step = 0.1
    direction_change_interval = 0.8
    mode = input('Sample mode? Y/n: ')
    if mode.lower() != 'n':
        change_var = input("Which variable is independent? Area(A),Fish speed(f),boat speed,(b): ").lower()
        change_var_list = []
        average_times = []
        if change_var == 'a':
            data_points = get_samples(change_var)
            change_var = 'Lake Area'
        elif change_var == 'f':
            data_points = get_samples(change_var)
            change_var = 'Fish speed'
        elif change_var == 'b':
            data_points = get_samples(change_var)
            change_var = 'Boat speed'
        areas = []
        #Graph plottin
        plt.figure(figsize=(12, 8))
        plt.plot(data_points[1], data_points[0], marker='o', linestyle='-', color='b', label='Average time')
        plt.xlabel(f'{change_var}', fontsize=14)
        plt.ylabel('Average Time to meet (seconds)', fontsize=14)
        plt.title(f'Average Time to meet v {change_var}', fontsize=16)
        plt.grid(True)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.show()
        
    else: 
        lake_area = 1000
        fish_speed = 9
        boat_speed = 12
        lake = Lake(lake_area)
        fish = Fish(lake, fish_speed)
        boat = Boat(lake, boat_speed)
        time = visualize_movement(lake, fish, boat, time_step, direction_change_interval)