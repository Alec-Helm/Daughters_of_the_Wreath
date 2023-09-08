import pygame
import math
import csv
from sys import exit
import SkillTreeFunctions as X


#basic initializing stuff
pygame.init()
screen_size = (800,600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Daughters of the Wreath Character Builder')
clock = pygame.time.Clock()
center_point = (200,150)
angle_correction = 0


#style formatting
test_font = pygame.font.Font(None, 25)



#pull node data from a csv 
#node data is output as [ID, angle, radius, neighbors, color] 
node_array = X.nodeCompile('Node_Master_List_Radial.csv')
number_nodes = len(node_array)


#get the cartesian location for all the nodes
node_cart_location = X.rad_to_cart(center_point, angle_correction, node_array)



#create the image obejcts and rectangles for the nodes
node_images = [pygame.Surface((3,3)) for _ in range(number_nodes)]
for i in range(number_nodes): node_images[i].fill('Red')
node_rects = [(node_images[i]).get_rect(center = node_cart_location[i][2]) for i in range(number_nodes)]




#initialize all the nodes as off
#and only the starter nodes as accessibly
node_states = [0 for _ in range(number_nodes)]
node_accesability = [1]
for i in range(number_nodes): node_accesability.append(0)
     

#initialize variables
highlighted_node = number_nodes


while True:
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            pygame.quit()   
            exit()
        elif event.type == pygame.MOUSEMOTION:
            highlighted_node = number_nodes
            position = pygame.mouse.get_pos()
            #find what node is below it by looking for collisions
            #mark that as currently active node
            for i in range(number_nodes):
                if node_rects[i].collidepoint(position):
                    highlighted_node = i



    #when click a node, change its color
    if pygame.mouse.get_pressed()[0]:
        if node_accesability[highlighted_node] == 1:            
                if node_states[highlighted_node] == 0:
                    node_states[highlighted_node] = 1
                    node_images[highlighted_node].fill((32,11,166))
                    for j in node_array[highlighted_node][3]:
                        node_accesability[j] = 1
                        if node_states[j] == 0: node_images[j].fill((127, 16, 135))


    #draw the current stats
    pygame.draw.rect(screen, 'Blue', pygame.Rect(600,0,200,400))

    
    
    
    #draw lines between adjacent nodes
    X.adjacent_node_lines(node_cart_location, screen)

    #add the nodes to the screen
    for i in range(number_nodes):
        screen.blit(node_images[i],node_rects[i])



    #update the screen
    pygame.display.update()
    clock.tick(60)