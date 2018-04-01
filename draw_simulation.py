import pygame
import numpy as np
from Nodes import *

width = 100
height = 100
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), 60)
id_font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

def clear_screen():
    screen.fill((0,0,0))


def draw_warehouse(g):
    for (x,y), node in np.ndenumerate(g):
        xCord = (width * y)
        yCord = (height * x)
        color = (0,0,0)
        if node.type == NodeType.DEFAULT:
            color = (0,255,0)
        elif node.type == NodeType.OBSTACLE:
            color = (255,0,0)
        elif node.type == NodeType.PICKUP:
            color = (0,0,255)
        pygame.draw.rect(screen, color, pygame.Rect(xCord, yCord, width-10, height-10))

def print_number_of_steps(i):
    textsurface = myfont.render(str(i), False, (255, 255, 255))
    screen.blit(textsurface, (0,900))

def draw(agent_list, g):
    simulating = True
    i = 0
    while simulating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulating = False
                #pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i -= 1
                if event.key == pygame.K_RIGHT:
                    i += 1
        clear_screen()
        draw_warehouse(g)
        print_number_of_steps(i)
        if 0 <= i < len(agent_list[0].actualWalking):
            #Draw the new position of the agents
            for j in range(0,len(agent_list)):
                agent_coordinates = (width * agent_list[j].actualWalking[i].coordinates[1], height * agent_list[j].actualWalking[i].coordinates[0])
                agent_target_coordinates = (width * agent_list[j].goal.coordinates[1], height * agent_list[j].goal.coordinates[0])


                pygame.draw.rect(screen, (255, 102, 0), pygame.Rect(agent_target_coordinates[0], agent_target_coordinates[1], width-10, height-10))
                text_goal = id_font.render(str(agent_list[j].id) + " goal", False, (255, 255, 255))
                screen.blit(text_goal, agent_target_coordinates)

                pygame.draw.rect(screen, (0,0,255), pygame.Rect(agent_coordinates[0], agent_coordinates[1], width-10, height-10))
                text_id = id_font.render(str(agent_list[j].id), False, (255, 255, 255))
                screen.blit(text_id, agent_coordinates)
                
        pygame.display.flip()
        clock.tick(30)
        