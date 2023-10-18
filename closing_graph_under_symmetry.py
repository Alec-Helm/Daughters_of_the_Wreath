import pygame
import math
import csv
from sys import exit


with open('Node_Master_List_Radial-Copy.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        output = {}
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                next_index = row[0]

                neighbor_list = []
                for neighbor_index in [6,7,8,9]:
                    next_neighbor = row[neighbor_index]
                    if next_neighbor != '' and int(next_neighbor) != 0:
                        neighbor_list.append(int(next_neighbor))
                output.update({next_index: neighbor_list})
