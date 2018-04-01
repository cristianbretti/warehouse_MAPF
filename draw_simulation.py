import pygame
import numpy as np

width = 150
height = 150
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)

def clear_screen():
    screen.fill((0,0,0))


def draw_warehouse(wh):
    for (x,y), value in np.ndenumerate(wh):
        xCord = (width * y)
        yCord = (height * x)
        color = (0,0,0)
        if value == 1:
            color = (255,0,0)
        elif value == 0:
            color = (0,255,0)
        pygame.draw.rect(screen, color, pygame.Rect(xCord, yCord, width-10, height-10))

def print_number_of_steps(i):
    textsurface = myfont.render(str(i), False, (255, 255, 255))
    screen.blit(textsurface, (0,900))

def draw(agent_list, wh):
    for i in range(0,len(agent_list[0].actualWalking)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clear_screen()
        draw_warehouse(wh)
        print_number_of_steps(i)
        #Draw the new position of the agents
        for j in range(0,len(agent_list)):
            agent_coordinates = (width * agent_list[j].actualWalking[i].coordinates[1], height * agent_list[j].actualWalking[i].coordinates[0])
            pygame.draw.rect(screen, (255*j,0,255), pygame.Rect(agent_coordinates[0], agent_coordinates[1], width-10, height-10))
       
        clock.tick(1)
        pygame.display.flip()