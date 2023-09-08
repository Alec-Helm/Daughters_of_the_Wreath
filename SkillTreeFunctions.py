import pygame
import math
import csv
from sys import exit

#function to pull all the node data from the node master list
#creates a 2D array where each entry is a node
#node data is then [index, angle, radius, neighbors, color]    #eventually need to change color to image path
#this structure should never be edited as the code runs
def nodeCompile(csv_path):
    node_list = []
    with open(csv_path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                next_node = [int(row[0]), int(row[2]), int(row[3]), [] , row[4]]
                for neighbor_index in [6,7,8,9]:
                    next_neighbor = row[neighbor_index]
                    if int(next_neighbor) != 0: 
                        next_node[3].append(int(next_neighbor))  
                node_list.append(next_node)
    
    return node_list



#returns a new list of all node locations of form [node_index, node_neighbors, x-coor, y-coor]
def rad_to_cart(center_point, angle_correction, list):
    node_cart_location = [[list[i][0],list[i][3],[center_point[0] + list[i][2] * math.cos((list[i][1] + angle_correction)*math.pi/180), center_point[1] - list[i][2] * math.sin((list[i][1] + angle_correction)*math.pi/180)]] for i in range(len(list))]
    return node_cart_location



#given a list of all the cartesian locations of the nodes, draw lines between them
def adjacent_node_lines(cartesian_location_list, screen):
    for node in cartesian_location_list:
        neighbors = node[1]
        for other_node in cartesian_location_list:
            if other_node[0] in neighbors:
                pygame.draw.line(screen, (81, 81, 81), node[2], other_node[2])



