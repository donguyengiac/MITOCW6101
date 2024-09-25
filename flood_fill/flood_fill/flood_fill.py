from collections import deque
from time import sleep
import time

def flood_fill(image, location, goal_color):
    """
    Given an image, replace the same-colored region around a given location
    with a given color.  Returns None but mutates the original image to
    reflect the change.

    Parameters:
      * image: the image to operate on
      * location: an (row, col) tuple representing the starting location of the
                  flood-fill process
      * new_color: the replacement color, as an (r, g, b) tuple where all values
                   are between 0 and 255, inclusive
    """
    start = time.time()
    def highlight_path(path):
        for pixel in path:
            set_pixel(image, *pixel, COLORS[pygame.K_p])

        
    def within_boundaries(location):
        if (location[0] < 0 or location[1] < 0 or location[0] >= get_height(image) or location[1] >= get_width(image)): return False
        return True
    
    print(f"You clicked at row {location[0]} col {location[1]}")
    path_list = deque()
    path_list.append([location])
    old_color = get_pixel(image, *location)
    #if (old_color == new_color): return
    visited = {location}
    pixel = location
    while(True) :
        
        #print(path_list)
        path = path_list.popleft()
        pixel = path[len(path)-1]
        #set_pixel(image, *pixel, COLORS[pygame.K_r])
        if (pixel[1] == get_width(image)-1): break
        DIR = [-1, 0, 1, 0, -1]
        for idx in range(4):
            new_location = (pixel[0]+DIR[idx], pixel[1]+DIR[idx+1])
            if within_boundaries(new_location) and (get_pixel(image, *new_location) != COLORS[pygame.K_k]) and new_location not in visited: 
                path.append(new_location)
                path_list.append(path[:])
                visited.add(new_location)
                path.pop()
    print(time.time()-start)
    highlight_path(path)
    pass # your code here


##### IMAGE REPRESENTATION WITH SIMILAR ABSTRACTIONS TO LAB 1 AND 2


def get_width(image):
    return image.get_width() // SCALE


def get_height(image):
    return image.get_height() // SCALE


def get_pixel(image, row, col):
    color = image.get_at((col * SCALE, row * SCALE))
    return (color.r, color.g, color.b)


def set_pixel(image, row, col, color):
    loc = row * SCALE, col * SCALE
    c = pygame.Color(*color)
    for i in range(SCALE):
        for j in range(SCALE):
            image.set_at((loc[1] + i, loc[0] + j), c)
    ## comment out the two lines below to avoid redrawing the image every time
    ## we set a pixel
    screen.blit(image, (0, 0))
    pygame.display.flip()
    #sleep(0.05)


##### USER INTERFACE CODE
##### DISPLAY AN IMAGE AND CALL flood_fill WHEN THE IMAGE IS CLICKED

import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pygame.locals import *

COLORS = {
    pygame.K_r: (255, 0, 0),
    pygame.K_w: (255, 255, 255),
    pygame.K_k: (0, 0, 0),
    pygame.K_g: (0, 255, 0),
    pygame.K_b: (0, 0, 255),
    pygame.K_c: (0, 255, 255),
    pygame.K_y: (255, 230, 0),
    pygame.K_p: (179, 0, 199),
    pygame.K_o: (255, 77, 0),
    pygame.K_n: (66, 52, 0),
    pygame.K_e: (152, 152, 152),
}

COLOR_NAMES = {
    pygame.K_r: "red",
    pygame.K_w: "white",
    pygame.K_k: "black",
    pygame.K_g: "green",
    pygame.K_b: "blue",
    pygame.K_c: "cyan",
    pygame.K_y: "yellow",
    pygame.K_p: "purple",
    pygame.K_o: "orange",
    pygame.K_n: "brown",
    pygame.K_e: "grey",
}

SCALE = 2
IMAGE = "maze1.png"

pygame.init()
image = pygame.image.load(IMAGE)
dims = (image.get_width() * SCALE, image.get_height() * SCALE)
screen = pygame.display.set_mode(dims)
image = pygame.transform.scale(image, dims)
screen.blit(image, (0, 0))
pygame.display.flip()
initial_color = pygame.K_g
cur_color = COLORS[initial_color]
print("current color:", COLOR_NAMES[initial_color])
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        else: 
            flood_fill(image, (1, 0), cur_color)
            screen.blit(image, (0, 0))
            pygame.display.flip()
        break
        if event.type == pygame.KEYDOWN:
            if event.key in COLORS:
                cur_color = COLORS[event.key]
                print("current color:", COLOR_NAMES[event.key])
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        #elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            