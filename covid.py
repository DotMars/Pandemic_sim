"""
Author : THe tamaaaaaaaaaa
"""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from pygame import *

import pandas as pd
import numpy as np

import random
import Cell
import disease

import math
from math import *

import time

# SCREEN PARAMETERS
WIN_WIDTH = 500
WIN_HEIGHT = 340

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

PADDING = 20
SPEED = 1

#START TIME
START_TIME = time.time()


# SIMULATION PARAMETERS
POPULATION = 100
RECOVERY_TIME = 7
CELL_RADIUS = 5

ERADICATED = False

# STATS
INFECTED_COUNT = 1
NORMAL_COUNT = POPULATION - 1
REMOVED_COUNT = 0

SIMULATION_HISTORY = []

Active_cells = []  # An array to store {n = POPULATION} number of Cell objects

covid_29 = disease.Disease(arg_name="COVID-29")


# PYGAME COLORS
CELL_COLOR = pygame.Color(15, 82, 186)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREY = pygame.Color(128, 128, 128)
WHITE = pygame.Color(255, 255, 255)


def export_to_csv():
    data = pd.DataFrame(SIMULATION_HISTORY)
    print(data)
    # create a csv file
    data.to_csv("data.csv", index=False, header=False)
    print("Simulation data exported !")
 
    exit()

def statistics():
    SIMULATION_HISTORY.append([INFECTED_COUNT, NORMAL_COUNT, REMOVED_COUNT, 
                       (time.time() - START_TIME)])
    ERADICATED = True
    for cell in Active_cells:
        if cell.get_state() == "I":
            ERADICATED = False
    if ERADICATED:
        export_to_csv()


def draw_cells(screen):
    global Active_cells
    for cell in Active_cells:
        if cell.state == "S":
            pygame.draw.circle(screen, CELL_COLOR, cell.position, CELL_RADIUS)
        elif cell.state == "I":
            pygame.draw.circle(screen, RED, cell.position, CELL_RADIUS)
        elif cell.state == "R":
            pygame.draw.circle(screen, GREY, cell.position, CELL_RADIUS)


check_count = 0


def check_cell_overlap(x, y, z, a):
    global check_count
    check_count += 1
    print("Check count :", check_count)

    distance = sqrt((x - z)*(x - z) + (y - a)*(y - a))
    if distance < CELL_RADIUS:
        print("Overlapping because distance : " + str(distance))
        return True
    else:
        # print("Not overlapping because distance : " + str(distance))
        return False


def initialize_cells_uniformly(number_of_regions=4):
    global Active_cells
    initial_cell_positions = []
    region_size = (WIN_WIDTH/(number_of_regions/2),
                   WIN_HEIGHT/(number_of_regions/2))
    # Generating random non overlapping cells positions
    Active_cells.append(Cell.Cell(random.randint(
        PADDING, WIN_WIDTH - PADDING), random.randint(PADDING, WIN_HEIGHT - PADDING), 0))
    for i in range(POPULATION):
        Active_cells.append(Cell.Cell(id=i+1))


def initialize_cells():
    global Active_cells
    initial_cell_positions = []

    for i in range(POPULATION):
        Active_cells.append(
            Cell.Cell(id=i))

    Active_cells[0].set_state("I")
    Active_cells[0].infected_with(covid_29)


def spread():
    for cell in Active_cells:
        if cell.is_infected():
            for other_cell in Active_cells:
                # if cell != other_cell:
                distance = cell.distance(other_cell)
                if distance[0] <= cell.disease.get_radius() and distance[1] <= cell.disease.get_radius():
                    if distance[0] > 5 or distance[1] > 5:
                        # print("Infected distance : ", distance[0], " ", distance[1])
                        # print("Infected position : ", cell.get_position(), end = " ")
                        # print("Other cell position : ", other_cell.get_position())
                        other_cell.infected_with(cell.disease)


def initialize_world(screen):
    initialize_cells()
    draw_cells(screen)


def main():
    global INFECTED_COUNT, NORMAL_COUNT, REMOVED_COUNT

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption(
        "Tamagulating spread of disease : " + covid_29.name)
    timer = pygame.time.Clock()

    screen.fill((255, 255, 255))
    initialize_world(screen)
    while 1:
        timer.tick(30)  # around 33 FPS

        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit("Quit event!")
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                raise SystemExit("Escape button by user!")

        screen.fill((255, 255, 255))
        NORMAL_COUNT = 0
        REMOVED_COUNT = 0
        INFECTED_COUNT = 0
        for cell in Active_cells:
            # cell.set_trajectory(random.randint(1, 9))
            # cell.update_random_destination()
            cell.update_central_dest_random_dest()
            if cell.get_state() == "I":
                INFECTED_COUNT += 1                
            elif cell.get_state() == "R":
                REMOVED_COUNT += 1
            elif cell.get_state() == "S":
                NORMAL_COUNT += 1
                
        # print(INFECTED_COUNT, NORMAL_COUNT, REMOVED_COUNT, time.time() - START_TIME)
        

        spread()
        statistics()
        draw_cells(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
