import random
import math
import time

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

#    def move_spiral(self.time_interval):
 #       pass


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
    lake_area = 100
    fish_speed = 9 
    time_step = 0.2  # Time interval for updates
    direction_change_interval = 2.0 
    boat_speed = 10
    lake = Lake(lake_area)
    fish = Fish(lake, fish_speed)
    boat = Boat(lake,boat_speed)
    #Fish movement
    print("Initial position of the fish:", fish.get_position())
    elapsed_time = 0
    while True:
        fish.move(time_step)
        boat.move_diagonal(time_step)
        elapsed_time += time_step

        # Change direction 
        if elapsed_time % direction_change_interval == 0:
            fish.change_direction()


        print(f"Time {elapsed_time:.1f} seconds: Fish position: {fish.get_position()} Boat position:{boat.get_position()}")

        if fish.get_position() == boat.get_position():
            print(f"Fish, met boat at {fish.get_position()} at time:{elapsed_time:.1f}")
            break
        time.sleep(time_step)
    
