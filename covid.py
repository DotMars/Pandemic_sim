"""
Author : THe tamaaaaaaaaaa
"""

import pygame
from pygame import *
from math import *
import numpy as np

import random
import Cell
import disease


# SCREEN PARAMETERS
WIN_WIDTH = 500
WIN_HEIGHT = 500

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

PADDING = 20

# SIMULATION PARAMETERS
POPULATION = 100
CELL_RADIUS = 5

Active_cells = []  # An array to store {n = POPULATION} number of Cell objects


# PYGAME COLORS
CELL_COLOR = pygame.Color(15, 82, 186)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREY = pygame.Color(128, 128, 128)
WHITE = pygame.Color(255, 255, 255)


def represente_cells(screen):
    global Active_cells
    for cell in Active_cells:
        if cell.state == "S":
            pygame.draw.circle(screen, CELL_COLOR, cell.position, CELL_RADIUS)
        elif cell.state == "I":
            pygame.draw.circle(screen, RED, cell.position, CELL_RADIUS)


check_count = 0


def check_cell_overlap(x, y, z, a):
    global check_count
    check_count += 1
    print("Check count :", check_count)

    distance = sqrt( (x - z)*(x - z) + (y - a)*(y- a) )
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
        Active_cells.append(Cell.Cell(id = i+1))


def initialize_cells():
    global Active_cells
    initial_cell_positions = []

    for i in range(POPULATION):
        Active_cells.append(
            Cell.Cell(id = i))
    
    Active_cells[0].set_state("I")

def spread():
    # for current_cell in Active_cells:
    #     for other_cell in Active_cells:
    #         if current_cell != other_cell:
    #             distance = current_cell.distance(other_cell)
    #             if distance <= current_cell.disease.get_radius():
    #                 print("Infected distance : ", distance)
    #                 print("Infected position : ", current_cell.get_position(), end = " ")
    #                 print("Other cell position : ", other_cell.get_position())
    #                 other_cell.infected_with(current_cell.disease)
    pass
  


def initialize_world(screen):
    initialize_cells()
    represente_cells(screen)


def main():

    covid_29 = disease.Disease(arg_name = "COVID-29")
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

        for cell in Active_cells:
            # cell.set_trajectory(random.randint(1, 9))
            cell.update_random_destination()
        
        spread()

        represente_cells(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
