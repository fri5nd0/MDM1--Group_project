import random
import math
import time
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Lake:
    def __init__(self, area):
        self.area = area
        self.side_length = math.sqrt(area)  # Calculate the side length of the square lake

class Boat:
    def __init__(self,lake,speed,mode):
        self.lake = lake
        self.pos = [0,0]
        self.direction = 0.0
        self.speed_vector = [0,0]
        self.speed_magnitude = speed
        self.mode = mode
        self.lake_center = self.lake.side_length/2
        if mode == 'Diagonal':
            self.direction = math.pi/4
            self.speed_vector = self.update_speed()
        if mode == 'Spiral':
            self.spiral_inward = True
            self.radius = 0
            self.max_radius = lake.side_length/2
            self.direction = 0.0
            self.speed_vector = self.update_speed()
            self.move_distance = 0     
            self.step_size = self.lake.side_length / 10
        elif mode == 'Area Cut Off':
            self.lake_center = lake.side_length / 2
            self.pos = [self.lake_center, self.lake_center]
            self.current_phase = 'radial'
            self.radial_distance_remaining = 2
            self.current_radius = 0
            self.angle = 0.0
            self.expanding = True  # New state variable
            self.speed_vector = self.update_speed()
    def move_diagonal(self, time_interval):
        new_pos = [(self.pos[0] + self.speed_vector[0] * time_interval),(self.pos[1] + self.speed_vector[1] * time_interval)]
        if new_pos[0] < 0 or new_pos[1] > self.lake.side_length:
            self.direction = math.pi - self.direction  # Reflect direction horizontally
            self.speed_vector = self.update_speed()
            new_pos[0] = max(0, min(new_pos[0], self.lake.side_length))
        if new_pos[1] < 0 or new_pos[1] > self.lake.side_length:
            self.direction = -self.direction  # Reflect direction vertically
            self.speed_vector = self.update_speed()
            new_pos[1] = max(0, min(new_pos[1], self.lake.side_length))
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
    #####LOOKING INTO THIS
    def move_spiral(self, time_interval):
        if self.spiral_inward:
            self.radius = max(0, self.radius - self.speed_magnitude * time_interval)
        else:
            self.radius = min(self.max_radius, self.radius + self.speed_magnitude * time_interval)
        # Increment the angle for rotation
        self.direction += self.speed_magnitude * time_interval / self.radius if self.radius > 0 else 0.1
        self.speed_vector = self.update_speed()  # Prevent division by zero
        # Convert polar coordinates (radius, angle) to Cartesian coordinates (x, y)
        self.pos[0] = self.lake_center + self.radius * math.cos(self.direction)
        self.pos[1] = self.lake_center + self.radius * math.sin(self.direction)
        # Check if radius needs to reverse direction
        if self.radius == 0:
            self.spiral_inward = False  
        elif self.radius == self.max_radius:
            self.spiral_inward = True   
        # Convert polar coordinates to Cartesian
        self.new_pos = [(self.lake_center + self.radius * math.cos(self.direction)),(self.lake_center + self.radius * math.sin(self.direction))]
        self.pos[0] = max(0, min(self.pos[0], self.lake.side_length))
        self.pos[1] = max(0, min(self.pos[1], self.lake.side_length))
    def move_cut_off_area(self, time_interval):
        # Initialize expanding state if not already set (for backward compatibility)
        if not hasattr(self, 'expanding'):
            self.expanding = True
            
        if self.current_phase == 'radial':
            # Calculate possible movement distance
            distance = self.speed_magnitude * time_interval
            actual_move = min(distance, self.radial_distance_remaining)
            
            # Handle movement direction based on expansion/contraction
            if self.expanding:
                new_x = self.pos[0] + actual_move
                # Check if hitting right boundary
                if new_x >= self.lake.side_length:
                    actual_move = self.lake.side_length - self.pos[0]
                    self.expanding = False  # Switch to contracting
                    self.current_radius = self.lake_center  # Max possible radius
            else:
                new_x = self.pos[0] - actual_move
                # Check if hitting left boundary
                if new_x <= 0:
                    actual_move = self.pos[0]
                    self.expanding = True  # Switch to expanding
                    self.current_radius = 0  # Reset to center

            # Update position and remaining distance
            if self.expanding:
                self.pos[0] += actual_move
            else:
                self.pos[0] -= actual_move
                
            self.radial_distance_remaining -= actual_move

            # Check if radial movement completed
            if self.radial_distance_remaining <= 0:
                self.current_phase = 'circular'
                # Update radius based on direction
                if self.expanding:
                    self.current_radius += 2
                else:
                    self.current_radius -= 2

                # Check if reached center during contraction
                if not self.expanding and self.current_radius <= 0:
                    # Reset to initial expanding state
                    self.expanding = True
                    self.current_radius = 0
                    self.pos = [self.lake_center, self.lake_center]
                    self.current_phase = 'radial'
                    self.radial_distance_remaining = 2
                else:
                    self.angle = 0.0  # Reset angle for new circle

        else:  # Circular phase
            # Handle zero radius case (shouldn't normally happen)
            safe_radius = max(self.current_radius, 0.1)
            delta_angle = (self.speed_magnitude * time_interval) / safe_radius
            self.angle += delta_angle

            # Check if circle completed
            if self.angle >= 2 * math.pi:
                self.angle -= 2 * math.pi
                self.current_phase = 'radial'
                self.radial_distance_remaining = 2

                # Check if near center after contraction circle
                if not self.expanding and self.current_radius <= 2:
                    self.current_radius = 0
                    self.expanding = True
                    self.pos = [self.lake_center, self.lake_center]

            # Update circular position
            self.pos[0] = self.lake_center + self.current_radius * math.cos(self.angle)
            self.pos[1] = self.lake_center + self.current_radius * math.sin(self.angle)

        # Ensure we stay within lake boundaries
        self.pos[0] = max(0, min(self.pos[0], self.lake.side_length))
        self.pos[1] = max(0, min(self.pos[1], self.lake.side_length))
    def get_position(self):
        return self.pos
    def set_position(self):
        self.pos = [0,0]
    def update_speed(self):
        return [(self.speed_magnitude * math.cos(self.direction)),(self.speed_magnitude * math.sin(self.direction))]
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
    def visualize_movement(lake, fish, boat, time_step, direction_change_interval,model):
        fig, ax = plt.subplots()
        ax.set_xlim(0, lake.side_length)
        ax.set_ylim(0, lake.side_length)
        ax.set_title("Fish and Boat Movement in a Lake")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        fish_marker, = ax.plot([], [], 'bo', label="Fish")  # Blue for Fish
        boat_marker, = ax.plot([], [], 'ro', label="Boat")  # Red for Boat
        boat_trail, = ax.plot([], [], 'r-', linewidth=1.5)  # Red line for boat trail
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
            print(f"Time {elapsed_time:.1f}s, Fish at {fish_pos}, Boat at {boat_pos}")
            if model == 's':
                boat.move_spiral(time_step)
            if model == 'c':
                boat.move_cut_off_area(time_step)
            else:
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
    def quick_simulation(fish, boat, time_step, direction_change_interval,model):
        elapsed_time = 0
        change_time = 0
        while True:
            fish_pos = fish.get_position()
            boat_pos = boat.get_position()
            elapsed_time += time_step
            change_time += time_step
            if model == 'd':
                boat.move_diagonal(time_step)
            if model == 's':
                boat.move_spiral(time_step)
            if model == 'c':
                boat.move_cut_off_area(time_step)
            fish.move(time_step)        # Move boat and fish
            if change_time >= direction_change_interval:
                fish.change_direction()
                change_time = 0         # Change fish direction at intervals
            if math.sqrt((fish_pos[0] - boat_pos[0]) ** 2 + (fish_pos[1] - boat_pos[1]) ** 2) <= 2:
                print(f"Fish met boat at position {fish_pos} when boat was at {boat_pos} at time {elapsed_time:.1f} seconds.")
                break # Check if they meet and end this sample
        fish.set_position()#reset positions for the next sample
        boat.set_position()
        return elapsed_time
    

    def get_samples(change_var,model):    #YOU CAN PLAY AROUND WITH THIS PART OF THE CODE 
        average_times = []
        change_var_list = []
        ranges = {
            'a': range(20, 1001, 20),  # Lake Area
            'f': range(1, 50),         # Fish Speed (the third number is the step. We can play around with it)
            'b': range(1, 150)          # Boat Speed
        }#defined ranges for all samples
        for value in ranges[change_var]:
            lake_area = 1000 #default values
            fish_speed = 9
            boat_speed = 30
            if change_var == 'a':
                lake_area = value
            elif change_var == 'f':
                fish_speed = value
            elif change_var == 'b':
                boat_speed = value#value is set depending on the independent variable('change_var')
            lake = Lake(lake_area)
            fish = Fish(lake, fish_speed)
            if model == 'd':
                boat = Boat(lake, boat_speed,'Diagonal')
            if model == 's':
                boat = Boat(lake, boat_speed,'Spiral')
            if model == 'c':
                boat = Boat(lake,boat_speed,'Area Cut Off')
            time = 0
            samples = 0
            while samples <= 1000:
                time += quick_simulation(fish, boat, time_step, direction_change_interval,model)
                samples += 1
            average = time / samples
            average_times.append(average)
            change_var_list.append(value)
            print(f"Average time to meet was: {average:.2f} \nFor {change_var} value: {value}")# Store results
        return [average_times,change_var_list]
                
    time_step = 0.05
    direction_change_interval = 0.8
    model = input('Spiral(S) or Diagonal(D) or Area Cut off(C)?').lower()
    mode = input('Sample mode? Y/n: ')
    if mode.lower() != 'n':
        change_var = input("Which variable is independent? Area(A),Fish speed(f),boat speed,(b): ").lower()
        change_var_list = []
        average_times = []
        if change_var == 'a':
            data_points = get_samples(change_var,model)   
            change_var = 'Lake area'
        elif change_var == 'f':
            data_points = get_samples(change_var,model)
            change_var = 'Fish speed'
        elif change_var == 'b':
            data_points = get_samples(change_var,model)
            change_var = 'Boat speed'
        areas = []
        #Graph plottin
        plt.figure(figsize=(10, 6))
        plt.scatter(data_points[1], data_points[0], color='b', marker='x', label='Average time')
        plt.xlabel(f'{change_var}', fontsize=14)
        plt.ylabel('Average Time to meet (seconds)', fontsize=14)
        print(np.corrcoef(data_points[1],data_points[0])[0,1])
        m,b = np.polyfit(data_points[1],data_points[0],1)
        print('regression line: ', m,'x','+',b)
        plt.title(f'Average Time to meet v {change_var}', fontsize=16)
        plt.grid(True)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.show()
        
    else: 
        lake_area = 1000
        fish_speed = 9
        boat_speed = 12
        lake = Lake(lake_area)
        fish = Fish(lake, fish_speed)
        if model == 's':
            boat = Boat(lake,boat_speed,'Spiral')
        elif model == 'c':
            boat = Boat(lake,boat_speed,'Area Cut Off')
        else:
            boat = Boat(lake, boat_speed,'Diagonal')
        time = visualize_movement(lake, fish, boat, time_step, direction_change_interval,model)