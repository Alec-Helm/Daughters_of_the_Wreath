import pygame
import math
import csv
from sys import exit
import SkillTreeFunctions as X


#basic initializing stuff
pygame.init()
screen_size = (1800,920)
game_width = 1400
scale_factor = 1
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Daughters of the Wreath Character Builder')
clock = pygame.time.Clock()
center_point = (600,400)


#style formatting
font = pygame.font.SysFont(None, 25)
big_font = pygame.font.SysFont(None, 50)

#
#
#PULL IN THE DATA FOR ALL THE NODES AS GRAPH OBJECTS
#
#
#pull node data from a csv 
#outputs a partially filled dictionary 
#{"Image" : row[1], "Angle" : int(row[2]), "Radius" : int(row[3]), "Size" : int(row[4]), "ID" : None, "Neighbors" : None, "X" : None, "Y" : None, "Surface": None, "Rectangle": None, "State" : None, "Accessible" : None}
node_dict = X.nodeCompile('Node_Master_List_Radial.csv')
#get the cartesian location for all the nodes and fills in the X and Y keys of the dictionaries
node_cart_location = X.add_carts(center_point, node_dict)
#create the image obejcts and rectangles for the nodes, and add to the dictionaries
for node in node_dict:
    node_dict[str(node)]["Surface"] = pygame.Surface((node_dict[str(node)]["Size"], node_dict[str(node)]["Size"]))
    node_dict[str(node)]["Surface"].fill(node_dict[str(node)]["Color"])
    node_dict[str(node)]["Rectangle"] = node_dict[str(node)]["Surface"].get_rect(center = [node_dict[str(node)]["X"],node_dict[str(node)]["Y"]])

#change the starter nodes to be accessible
node_dict[str(101)]["Accessible"] = 1
node_dict[str(102)]["Accessible"] = 1
node_dict[str(103)]["Accessible"] = 1

node_dict[str(101)]["Color"] = (127, 16, 135)
node_dict[str(102)]["Color"] = (127, 16, 135)
node_dict[str(103)]["Color"] = (127, 16, 135)


node_dict[str(101)]["Surface"].fill(node_dict[str(101)]["Color"])
node_dict[str(102)]["Surface"].fill(node_dict[str(102)]["Color"])
node_dict[str(103)]["Surface"].fill(node_dict[str(103)]["Color"])


#
#
#PULL IN THE DATA FOR ALL THE NODES AS GAME OBJECTS
#
#
node_effects = X.effectCompile('BODY_nodes.csv')






#initialize variables
highlighted_node = 0
dragging = False
first_node = True
search_mode = False
search_text = ''

edit_mode = True
save_mode = False


#data structures for storing player attributes
character = X.characterCompile()



#build structures for informing players
current_node_text = "Current Node: "
current_node_location_text = "r:, a: "
skill_points_text = "Level: " + str(character[0]["Level"])




while True:
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            pygame.quit()   
            exit()
        elif event.type == pygame.MOUSEMOTION:
            current_node_text = "Current Node: "
            highlighted_node = 0
            position = pygame.mouse.get_pos()
            #find what node is below it by looking for collisions
            #mark that as currently active node
            for node in node_dict:
                if node_dict[str(node)]["Rectangle"].collidepoint(position):
                    highlighted_node = str(node)
                    current_node_text = "Current Node: " + highlighted_node
                    current_node_location_text = "r = " + str(node_dict[str(node)]["Radius"]) + "  , t = " + str(node_dict[str(node)]["Angle"])
            if dragging:
                screen.fill((0,0,0))
                end_pos = pygame.mouse.get_pos()
                displacement = [-end_pos[0] + start_pos[0], -end_pos[1] + start_pos[1]]
                for node in node_dict:
                    node_dict[str(node)]["X"] = node_dict[str(node)]["X"]+end_pos[0] - start_pos[0]
                    node_dict[str(node)]["Y"] = node_dict[str(node)]["Y"]+end_pos[1] - start_pos[1]
                            
                    node_dict[str(node)]["Rectangle"] = node_dict[str(node)]["Surface"].get_rect(center = [node_dict[str(node)]["X"],node_dict[str(node)]["Y"]])
                start_pos = end_pos   
            #if scrollwheel is used we want to zoom in (or out if negative)
            #to do this we first re-center the entire drawing around the current mouse position
            #then re-determine all the radial distances from the new centerpoint
            #it expands by a factor based on the scroll amount
            #finally sets the proper node cart locations
        elif event.type == pygame.MOUSEWHEEL:
            if event.y != 0:
                screen.fill((0,0,0))
                new_center = pygame.mouse.get_pos()
                dict_with_temporary_radials = X.find_radials(new_center, node_dict)
                scale_factor = 1  +  (event.y / 10)
                for node in dict_with_temporary_radials:
                    dict_with_temporary_radials[str(node)]["Radius"] = scale_factor*dict_with_temporary_radials[str(node)]["Radius"]
                    dict_with_temporary_radials[str(node)]["Angle"] = dict_with_temporary_radials[str(node)]["Angle"] - math.pi/2
                node_dict = X.find_carts(new_center, dict_with_temporary_radials)
                for node in node_dict:
                    node_dict[str(node)]["Size"] *= scale_factor
                    node_dict[str(node)]["Surface"] = pygame.Surface((node_dict[str(node)]["Size"], node_dict[str(node)]["Size"]))
                    node_dict[str(node)]["Surface"].fill(node_dict[str(node)]["Color"])    
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #holding down the right mouse button will shift drag the screen
            if pygame.mouse.get_pressed()[2]:
                start_pos = pygame.mouse.get_pos()
                dragging = True

            
            elif pygame.mouse.get_pressed()[0]:

                #clicking on a node should be an attempt to activate the node, clicking the search bar should enter us into search mode
                #if we were in search mode and we click anywhere but the search bar, we exit search mode
                if save_button_rect.collidepoint(position):
                    X.save_character(node_dict, character)
 
                elif load_button_rect.collidepoint(position):
                    #load in a character from .txt file
                elif not search_mode:
                    #if they click on the search_bar, enter search mode
                    if search_bar_rect.collidepoint(position):
                        search_mode = True

                    elif first_node:
                        output = X.left_click(highlighted_node, node_dict, node_effects, character, first_node)
                        node_dict = output[0]
                        character = output[1]
                        first_node = output[2]
                    else:
                        output = X.left_click(highlighted_node, node_dict, node_effects, character, False)
                        node_dict = output[0]
                        character = output[1]
                
                else:
                    if not node_dict[str(node)]["Rectangle"].collidepoint(position):
                        search_mode = False
                    
                    elif first_node:
                        output = X.left_click(highlighted_node, node_dict, node_effects, character, first_node)
                        node_dict = output[0]
                        character = output[1]
                        first_node = output[2]
                    else:
                        output = X.left_click(highlighted_node, node_dict, node_effects, character, False)
                        node_dict = output[0]
                        character = output[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.KEYDOWN:
            #if we are in search mode, update the search box
            if search_mode:
                if event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                else:
                    search_text += event.unicode





    #cleanse screen
    screen.fill((0,0,0))
    
    #draw lines between adjacent nodes
    X.adjacent_node_lines(node_dict, screen)

    #add the nodes to the screen
    for node in node_dict:
        screen.blit(node_dict[str(node)]["Surface"],node_dict[str(node)]["Rectangle"])


    #draw the screen to display the current stats
    stat_screen_location = [game_width, 0]
    stat_screen_dims = [screen_size[0]-game_width,screen_size[1]]
    pygame.draw.rect(screen, 'Blue', pygame.Rect(stat_screen_location[0],stat_screen_location[1],stat_screen_dims[0],stat_screen_dims[1]))

    stats_to_use = X.calc_stats(character[0])

    level_location = (stat_screen_location[0] + stat_screen_dims[0]/2, 50)
    X.add_textc(screen, font, "Level: " + str(stats_to_use["Level"]), 'White', level_location)

    data_location = [stat_screen_location[0] + stat_screen_dims[0]/5, 75]
    for attribute in character[0]:
        data_location[1] += 25
        if attribute != "Level":
            X.add_text(screen, font, attribute + ": " +  str(stats_to_use[str(attribute)]), 'White', data_location)




    #build the search bar
    search_bar = pygame.Surface((200, 40))
    search_bar.fill('White')
    search_bar_rect = search_bar.get_rect(topleft = [game_width - 300, screen_size[1] - 100])
    screen.blit(search_bar, search_bar_rect)

    #if we are currently searching, fill the text bar and highlighed searched nodes
    if search_text != '':
        X.add_text(screen, big_font, search_text, "Black", [game_width - 300, screen_size[1] - 100])
        for node in node_dict:
            if search_text.lower() in node_effects[node_dict[str(node)]["ID"]]["Description"].lower():
                highlight = pygame.Surface((node_dict[str(node)]["Size"]*1.5, node_dict[str(node)]["Size"]*1.5))
                highlight.fill((255, 255, 0))
                highlight.set_alpha(100)
                highlight_rect = highlight.get_rect(center = [node_dict[str(node)]["X"],node_dict[str(node)]["Y"]])
                screen.blit(highlight, highlight_rect)
    elif not search_mode:
        X.add_text(screen, big_font, "Search", "Gray", [game_width - 300, screen_size[1] - 100])

    
    #build the save and load buttons
    save_button = pygame.Surface((100, 40))
    save_button.fill('White')
    save_button_rect = save_button.get_rect(topleft = [game_width - 420, screen_size[1] - 100])
    screen.blit(save_button, save_button_rect)
    X.add_text(screen, big_font, "Save", "Black", [game_width - 420, screen_size[1] - 100])

    load_button = pygame.Surface((100, 40))
    load_button.fill('White')
    load_button_rect = load_button.get_rect(topleft = [game_width - 540, screen_size[1] - 100])
    screen.blit(load_button, load_button_rect)
    X.add_text(screen, big_font, "Load", "Black", [game_width - 540, screen_size[1] - 100])


    #add a smaller box to display information about current node
    data_location[1] += 25

    highlight_screen_location = [game_width, data_location[1] + 25]
    highlight_screen_dims = [screen_size[0]-game_width,screen_size[1]- (data_location[1])]
    pygame.draw.rect(screen, 'Gray', pygame.Rect(highlight_screen_location[0],highlight_screen_location[1],highlight_screen_dims[0],highlight_screen_dims[1]))

    if highlighted_node != 0:
        data_location[0] -= 25
        data_location[1] += 25
        X.add_text(screen, font, "Current Node: " + str(highlighted_node), "Black", data_location)
        data_location[1] += 25
        X.add_text(screen, font, current_node_location_text, "Black", data_location)
        data_location[1] += 25
        X.add_text(screen, font, node_effects[node_dict[str(highlighted_node)]["ID"]]["Description"], "Black", data_location)
    else:
        data_location[0] -= 25
        data_location[1] += 25
        X.add_text(screen, font, "Current Node: " + str(highlighted_node), "Black", data_location)
        data_location[1] += 25
        X.add_text(screen, font, current_node_location_text, "Black", data_location)
        data_location[1] += 25

    #X.add_text(screen, font, "Current Node: " + str(search_mode), "Black", data_location)

    




    #update the screen
    pygame.display.update()
    clock.tick(60)