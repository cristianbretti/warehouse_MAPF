import pygame
import numpy as np
from Nodes import *

width = 35
height = 35
gap = 5
text_offset = 5
pygame.init()
screen = pygame.display.set_mode((1920,1080), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), 30)
id_font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
small_id_font = pygame.font.SysFont(pygame.font.get_default_font(), 15)

def clear_screen():
    screen.fill((0,0,0))


def draw_warehouse(g):
    for (x,y), node in np.ndenumerate(g):
        xCord = (width * y)
        yCord = (height * x)
        color = (0,0,0)
        id_text = str(node.id)
        if node.type == NodeType.DEFAULT:
            color = (255,255,255)
        elif node.type == NodeType.OBSTACLE:
            color = (0,0,0)
        elif node.type == NodeType.PICKUP:
            color = (0,191,255)
        elif node.type == NodeType.DROPOFF:
            color = (255,0,255)
        pygame.draw.rect(screen, color, pygame.Rect(xCord, yCord, width-gap, height-gap))
        text_id = small_id_font.render(id_text, False, (0, 0, 0))
        screen.blit(text_id, (xCord + text_offset, yCord + text_offset))

def print_number_of_steps(i):
    textsurface = myfont.render(str(i), False, (255, 255, 255))
    screen.blit(textsurface, (0,900))

def print_fps(fps):
    textsurface = myfont.render(str(fps), False, (255, 255, 255))
    screen.blit(textsurface, (0,950))

def draw(agent_list, g):
    simulating = True
    i = 0
    fps = 10
    while simulating:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            i -= 1
            if i < 0:
                i = 0
        if keys[pygame.K_RIGHT]:
            i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulating = False
                #pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    fps -= 5
                    if fps <= 5:
                        fps = 5
                if event.key == pygame.K_UP:
                    fps += 5
        clear_screen()
        draw_warehouse(g)
        print_number_of_steps(i)
        print_fps(fps)
        #Draw the new position of the agents
        for a in agent_list:
            if i < len(a.walking_path):
                agent_coordinates = (width * a.walking_path[i].coordinates[1], height * a.walking_path[i].coordinates[0])
                #agent_target_id = a.target_path[i]
                #agent_target_coordinates = (width * a.goal.coordinates[1], height * a.goal.coordinates[0])


                #pygame.draw.rect(screen, (255, 127, 80), pygame.Rect(agent_target_coordinates[0], agent_target_coordinates[1], width-gap, height-gap))
                #text_goal = id_font.render(str(a.id) + " goal", False, (255, 255, 255))
                #screen.blit(text_goal, agent_target_coordinates)

                pygame.draw.rect(screen, (154, 205, 50), pygame.Rect(agent_coordinates[0], agent_coordinates[1], width-gap, height-gap))
                text_id = id_font.render(str(a.id), False, (255, 255, 255))
                screen.blit(text_id, agent_coordinates)
                #text_target_id = id_font.render("Agent: " + str(a.id) + " has target:" + str(agent_target_id), False, (255,255,255))
                #screen.blit(text_target_id, (1750, 100 + (50*agent_list.index(a))))

        pygame.display.flip()
        clock.tick(fps)
