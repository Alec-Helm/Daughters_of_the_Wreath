import pygame
import math
import csv
from nodeEffects import *
from sys import exit
#
#
#FUNCTIONS THAT RUN ONCE ON LOAD
#
#
#function to pull all the node data from the node master list and stores it in a dictionary which will eventually store all the node data
def nodeCompile(csv_path):
    node_dict = {}
    with open(csv_path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                next_node_dict = {"Image" : row[1], "Color" : 'Red', "Angle" : int(math.floor(float(row[2]))), "Radius" : int(row[3]), "Size" : int(row[4]), "ID" : row[5], "Neighbors" : None, "X" : None, "Y" : None, "Surface": None, "Rectangle": None, "State" : 0, "Accessible" : 0}
                neighbor_list = []
                for neighbor_index in [6,7,8,9]:
                    next_neighbor = row[neighbor_index]
                    if next_neighbor != '' and int(next_neighbor) != 0:
                        neighbor_list.append(int(next_neighbor))
                next_node_dict["Neighbors"] = neighbor_list
                node_dict.update({row[0] : next_node_dict})
    
    #take a moment to close the neighborhood sets under symmetry
    for node in node_dict:
        neighbors = node_dict[str(node)]["Neighbors"]
        for neighbor in neighbors:
            if node not in node_dict[str(neighbor)]["Neighbors"]:
                node_dict[str(neighbor)]["Neighbors"].append(node)
    
    return node_dict


#loads in all the node effects and descriptions
def effectCompile(csv_path):
    node_effects = {}
    with open(csv_path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                next_effect = {"Description": row[1], "Primary Effect": row[2], "Secondary Effect" : row[3], "Text Effect" : row[4], "Function": row[5]}
                node_effects.update({row[0] : next_effect})
    return node_effects

#function to instantiate the player character as a dictionary
def characterCompile():
    character = {"BODY": 0 , "SOUL" : 0, "SPEED": 0, "TALENT": 0 ,"HP": 0, "Slow Regen" : 0, "Fast Regen" : 0, "Precision": 0, "Damage" : 0, "Durability" : 0, "Strength" : 0, "SP" : 0 , "Soul Recovery" : 0, "Soul Precision" : 0, "Resilience" : 0, "Soul Efficiency" : 0, "Soul Attenuation" : 0, "Soul Range" : 0, "Speed" : 0, "Initiative" : 0 , "Skill" : 0, "Luck" : 0, "Wisdom" : 0, "Order" : 0, "Chaos" : 0 ,  "Other" : [], "Level" : 0}
    character_tertiary = {}
    return([character, character_tertiary])





#
#
#FUNCTIONS THAT RUN TO IMPLEMENT PLAYER INPUT
#
#
def left_click(highlighted_node, node_dict, node_effects, character, first_node):
    if highlighted_node != 0:
        if node_dict[str(highlighted_node)]["Accessible"] == 1 and node_dict[str(highlighted_node)]["State"] == 0:
            character[0]["Level"] += 1

            if not first_node:
                #we need to turn the node on, and make all its off-neighbor's accessible
                node_dict[str(highlighted_node)]["State"] = 1
                node_dict[str(highlighted_node)]["Color"] = (32,11,166)
                node_dict[str(highlighted_node)]["Surface"].fill((32,11,166))

                for neighbor in node_dict[str(highlighted_node)]["Neighbors"]:
                    if node_dict[str(neighbor)]["State"] == 0:
                        node_dict[str(neighbor)]["Accessible"] = 1
                        node_dict[str(neighbor)]["Color"] = (127, 16, 135)
                        node_dict[str(neighbor)]["Surface"].fill((127, 16, 135))
                
                #then we need to implement the effect into the character
                #grab the function name from the effect document and run it
                run_string = node_effects[node_dict[highlighted_node]["ID"]]["Function"] + "(character)"
                character = eval(run_string)

                return [node_dict, character, False]

                
            else:
                for starter in [101,102,103]:
                    if highlighted_node != starter:
                        node_dict[str(starter)]["Accessible"] = 0
                        node_dict[str(starter)]["Color"] = 'Red'
                        node_dict[str(starter)]["Surface"].fill('Red')

                    node_dict[str(highlighted_node)]["State"] = 1
                    node_dict[str(highlighted_node)]["Color"] = (32,11,166)
                    node_dict[str(highlighted_node)]["Surface"].fill((32,11,166))

                    for neighbor in node_dict[str(highlighted_node)]["Neighbors"]:
                        if node_dict[str(neighbor)]["State"] == 0:
                            node_dict[str(neighbor)]["Accessible"] = 1
                            node_dict[str(neighbor)]["Color"] = (127, 16, 135)
                            node_dict[str(neighbor)]["Surface"].fill((127, 16, 135))

                run_string = node_effects[node_dict[highlighted_node]["ID"]]["Function"] + "(character)"
                character = eval(run_string)

                first_node = False
                return [node_dict, character, first_node]
        else:
            return [node_dict, character, first_node]
    return [node_dict, character, first_node]










#returns a new list of all node locations of form [node_index, node_neighbors, [x-coor, y-coor]]
def add_carts(center_point, dict):
    for node in dict:
        dict[str(node)]["X"] = center_point[0] + dict[str(node)]["Radius"] * math.cos((dict[str(node)]["Angle"])*math.pi/180)
        dict[str(node)]["Y"] = center_point[1] - dict[str(node)]["Radius"] * math.sin((dict[str(node)]["Angle"])*math.pi/180)    
    return dict



#given a list of all the cartesian locations of the nodes, draw lines between them
def adjacent_node_lines(dict, screen):
    for node in dict:
        for neighbor in dict[str(node)]["Neighbors"]:
            adj = str(neighbor)
            pygame.draw.line(screen, (81, 81, 81), [dict[str(node)]["X"], dict[str(node)]["Y"]], [dict[adj]["X"], dict[adj]["Y"]])




#finds the radial locations of each node given a new centerpoint
def find_radials(new_center, dict):
    temp_dict = dict
    for node in dict:
        delta_x = new_center[0] - dict[str(node)]["X"]
        delta_y = new_center[1] - dict[str(node)]["Y"]
        temp_dict[str(node)]["Angle"] = math.atan2(delta_x,delta_y) + math.pi
        temp_dict[str(node)]["Radius"] = math.sqrt(delta_x*delta_x + delta_y*delta_y)
    return temp_dict

#finds the cartesian locations after scaling
def find_carts(center, temp_dict):
    for node in temp_dict:
        temp_dict[str(node)]["X"] = center[0] + temp_dict[str(node)]["Radius"] * math.cos((temp_dict[str(node)]["Angle"]))
        temp_dict[str(node)]["Y"] = center[1] - temp_dict[str(node)]["Radius"] * math.sin((temp_dict[str(node)]["Angle"]))

        temp_dict[str(node)]["Rectangle"] = temp_dict[str(node)]["Surface"].get_rect(center = [temp_dict[str(node)]["X"],temp_dict[str(node)]["Y"]])
    return temp_dict



#given text, a color, and a location - add it to the screen
def add_text(screen, font, text, color, location):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(topleft = location)
        screen.blit(text_obj, text_rect)

#same function but for centering instead of topleft
def add_textc(screen, font, text, color, location):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center = location)
        screen.blit(text_obj, text_rect)





#calculate actual player stats given modifiers
def calc_stats(character):
    output = character.copy()
    output["HP"] += 100 + 2*output["BODY"]
    output["Slow Regen"] += 2*math.floor(math.log2(1 + output["BODY"]))
    output["Damage"] += math.floor(math.log2(1 + output["BODY"]))
    output["Durability"] += math.floor(math.log2(1 + output["BODY"]))
    output["Strength"] += math.floor(math.log2(1 + output["BODY"]))
    output["SP"] += 100 + output["SOUL"]
    output["Soul Recovery"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Resilience"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Soul Efficiency"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Soul Attenuation"] += 10*math.floor(math.log2(1 + output["SOUL"]))
    output["Soul Range"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Speed"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Initiative"] += math.floor(math.log2(1 + output["SOUL"]))
    output["Skill"] += math.floor(math.log2(1 + output["TALENT"]))

    return output



def save_character(dict, char):
    #save the current state into a .txt file
    save_file = open("character_nodes.txt", "w")
    for node in dict:
        save_file.write(dict[node]["Accessible"] + "\n")
        save_file.write(dict[node]["State"] + "\n")
    
    save_file = open("character_stats.txt", "w")
    for 
