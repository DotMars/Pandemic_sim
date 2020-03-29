import disease
import random
from covid import PADDING, WIN_WIDTH, WIN_HEIGHT, Active_cells, RECOVERY_TIME, SPEED

import pygame
from pygame import *

import random

import math
from math import *

import time
from time import *

UP_LEFT = 1
UP = 2
UP_RIGHT = 3
LEFT = 4
RIGHT = 6
DOWN_LEFT = 7
DOWN = 8
DOWN_RIGHT = 9


class Cell(object):
    def __init__(self, starting_pos_x=0, starting_pos_y=0, id=-1, disease=disease.Disease()):
        super().__init__()

        # Possible states { S for susceptible,  I for infectuous & R for removed }
        self.patient_id = id
        self.state = "S"

        self.trajectory = 5     # Initiallized at 5 meaning not moving yet
        #    1 2 3
        #    4   6
        #    7 8 9
        self.position = self.pick_random_position()
        self.destination = self.pick_random_position()

        self.x_vel = 0
        self.y_vel = 0
        self.speed = SPEED

        self.disease = disease
        self.infection_time = time.time()

    def set_position(self, x, y):
        self.position = (x, y)

    def set_trajectory(self, trajectory):
        self.trajectory = trajectory

    def set_state(self, state):
        self.state = state

    def pick_random_position(self):
        return (random.randint(PADDING, WIN_WIDTH - PADDING),
                random.randint(PADDING, WIN_HEIGHT - PADDING))

    def get_position(self):
        return list(self.position)
    def get_state(self):
        return self.state

    def is_infected(self):
        if self.state == "I":
            return True
        else:
            return False

    def infected_with(self, disease):

        if disease and self.state == "S":
            random_choice = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            if random_choice:
                self.disease = disease
                self.state = "I"
                self.infection_time = time.time()

    def distance(self, other_cell=[]):
        position = list(self.position)
        x = other_cell.get_position()[0]
        y = other_cell.get_position()[1]
        distance_x = sqrt((x - position[0])*(x - position[0]))
        distance_y = sqrt((y - position[1])*(y - position[1]))
        distance = (distance_x, distance_y)
        return distance

    def update_central_dest_random_dest(self):
        # Simulating disease spread in a population going to a central location

        # Check if it's time to recover
        if time.time() - self.infection_time >= RECOVERY_TIME and self.state == "I":
            self.set_state("R")

        # Update location
        position = list(self.position)
        x = position[0]
        y = position[1]
        destination = list(self.destination)
        z = destination[0]
        a = destination[1]

        distance = sqrt((x - z)*(x - z) + (y - a)*(y - a))

        if distance <= 5:
            # print("Destination reached : ", self.destination, end = " ")
            if random.choice([0, 0, 0, 1]):
                self.destination = (WIN_WIDTH / 2, WIN_HEIGHT/2)
            else:
                self.destination = self.pick_random_position()
            # print("New dest assigned : ", self.destination)

        else:
            if x - z > 0:
                x -= self.speed
            elif x - z < 0:
                x += self.speed
            if y - a > 0:
                y -= self.speed
            elif y - a < 0:
                y += self.speed

            self.position = (x, y)
            self.within_border

    def update_random_destination(self):

        # Check if it's time to recover
        if time.time() - self.infection_time >= RECOVERY_TIME and self.state == "I":
            self.set_state("R")

        # Update location
        position = list(self.position)
        x = position[0]
        y = position[1]
        destination = list(self.destination)
        z = destination[0]
        a = destination[1]

        distance = sqrt((x - z)*(x - z) + (y - a)*(y - a))

        if distance <= 5:
            # print("Destination reached : ", self.destination, end = " ")
            self.destination = self.pick_random_position()
            # print("New dest assigned : ", self.destination)

        else:
            if x - z > 0:
                x -= self.speed
            elif x - z < 0:
                x += self.speed
            if y - a > 0:
                y -= self.speed
            elif y - a < 0:
                y += self.speed

            self.position = (x, y)
            self.within_border

    def update(self):
        if (self.trajectory == UP_LEFT):
            self.x_vel = -1
            self.y_vel = 1
        elif (self.trajectory == UP):
            self.x_vel = 0
            self.y_vel = 1
        elif (self.trajectory == UP_RIGHT):
            self.x_vel = 1
            self.y_vel = 1
        elif (self.trajectory == LEFT):
            self.x_vel = -1
            self.y_vel = 0
        elif (self.trajectory == RIGHT):
            self.x_vel = 1
            self.y_vel = 0
        elif (self.trajectory == DOWN_LEFT):
            self.x_vel = -1
            self.y_vel = -1
        elif (self.trajectory == DOWN):
            self.x_vel = 0
            self.y_vel = -1
        elif (self.trajectory == DOWN_RIGHT):
            self.x_vel = 1
            self.y_vel = -1

        if random.randint(0, 1):
            self.trajectory = 5
        self.set_position(
            self.position[0] + self.speed * self.x_vel, self.position[1] + self.speed * self.y_vel)
        self.within_border

    def within_border(self):

        padding = PADDING

        position = list(self.position)
        x = position[0]
        y = position[1]

        if x <= padding:
            x = padding
        elif x >= 500 - padding:
            x = 500 - padding
        if y <= padding:
            y = padding
        elif y >= 500 - padding:
            y = 500 - padding

        self.position = (x, y)
