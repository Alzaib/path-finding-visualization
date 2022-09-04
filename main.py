import math
from multiprocessing import current_process
from tracemalloc import start
from turtle import width
import pygame

NODE_WIDTH = 40
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = 'WHITE'
        self.g = 0 #distance from the end pos
        self.h = 0 #distance from the start pos
        self.f = 0 #f = g+h 
        self.start_node = False
        self.end_node = False
        self.wall_node = False
        self.open_node = False
        self.closed_node = False
        self.parent = None

    def reset(self):
        self.color = 'WHITE'
        self.start_node = False
        self.end_node = False
        self.wall_node = False
        self.open_node = False
        self.closed_node = False

    def get_pos(self):
        row = math.floor(self.row/NODE_WIDTH)
        col = math.floor(self.col/NODE_WIDTH)
        return row, col
    
    def make_start(self):
        self.color = 'ORANGE'
        self.start_node = True

    def make_end(self):
        self.color = 'PURPLE'
        self.end_node = True

    def make_wall(self):
        if self.start_node == False and self.end_node == False:
            self.color = 'BLACK'
            self.wall_node = True
            

    def make_open(self):
        if self.start_node == False and self.end_node == False:
            self.color = 'RED'
            self.open_node = True

    def make_close(self):
        if self.start_node == False and self.end_node == False:
            self.color = 'GREEN'
            self.closed_node = True

    def is_start(self):
        if self.wall_node == False:
            return self.start_node()

    def is_end(self):
        if self.wall_node == False:
            return self.end_node()

    def is_wall(self):
        return self.wall_node

    def is_open(self):
        return self.open_node

    def is_closed(self):
        return self.closed_node

    def set_parent(self, parent_node):
        self.parent = parent_node

    def get_parent(self, parent_node):
        return parent_node

    def get_g_score(self):
        return self.g
    
    def set_g_score(self, g_score):
        self.g = g_score
    
    def get_h_score(self):
        return self.h
    
    def set_h_score(self, h_score):
        self.h = h_score
    
    def get_f_score(self):
        self.f = self.g + self.h
        return self.f
    



def draw_rect(surface,node):
    rect = pygame.Rect(node.row, node.col, NODE_WIDTH, NODE_WIDTH)
    pygame.draw.rect(surface,  node.color, rect)
    pygame.draw.rect(surface, 'GREY', rect, 2)
    
    f_score = str(node.get_f_score())
    font = pygame.font.Font(None, 20)
    f_score_surface = font.render(f_score, False,'Black')

    x_dis = rect[0] + NODE_WIDTH/2
    y_dis = rect[1] + NODE_WIDTH/2
    
    #if f_score != '0':
    surface.blit(f_score_surface, (x_dis, y_dis))

def get_f_score(node, start, end):
    x_pos, y_pos = node.get_pos()
    x_pos_start, y_pos_start = start.get_pos()
    x_pos_end, y_pos_end = end.get_pos()

    #g cost: distance from current node to end node
    g = ((x_pos - x_pos_end)*(x_pos - x_pos_end))+((y_pos-y_pos_end)*(y_pos-y_pos_end))
    #h cost: distance from current node to start node
    h = ((x_pos - x_pos_start)*(x_pos - y_pos_start))+((y_pos-x_pos_start)*(y_pos-y_pos_start))
    #f cost: g+h
    f = g + h
    return f, g, h

def get_node_distance (start_node, end_node):
    x_pos_start, y_pos_start = start_node.get_pos()
    x_pos_end, y_pos_end = end_node.get_pos()

    distance = ((x_pos_start - x_pos_end)*(x_pos_start - x_pos_end))+((y_pos_start-y_pos_end)*(y_pos_start-y_pos_end))

    return distance

    

def get_node(node_arr,loc):
    x, y = loc
    for i in range(len(node_arr)):
        node_x_pos, node_y_pos = node_arr[i].get_pos()
        if x == node_x_pos and y == node_y_pos:
            return node_arr[i]

def get_neighbor(node, num_nodes):
    x_pos, y_pos = node.get_pos()
    
    left, right, up, down = None, None, None, None

    if (x_pos-1>0):
        left = (x_pos -1, y_pos)

    if (x_pos+1<num_nodes):
        right = (x_pos +1, y_pos)

    if (y_pos-1>0):
        up = (x_pos, y_pos-1)

    if (y_pos+1<num_nodes):
        down = (x_pos, y_pos+1)

    return [left, right, up, down]

def initilize(surface,num_nodes):
    node_arr =[]
    for col in range(num_nodes):
        for row in range(num_nodes):
            node = Node(row*NODE_WIDTH, col*NODE_WIDTH)
            node_arr.append(node)
            draw_rect(surface, node)
    return node_arr

def make_environment(surface, node_arr = []):
    mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
    mouse_x_pos = math.floor(mouse_x_pos/NODE_WIDTH)
    mouse_y_pos = math.floor(mouse_y_pos/NODE_WIDTH)
    
    for i in range(len(node_arr)):
        node_x_pos, node_y_pos = node_arr[i].get_pos()
        start_node = None
        end_node = None
        if mouse_x_pos == node_x_pos and mouse_y_pos == node_y_pos:
            if pygame.mouse.get_pressed()[0]:  
                node_arr[i].make_wall()
            elif pygame.mouse.get_pressed()[1]:
                node_arr[i].make_start()
                start_node = node_arr[i]
            elif pygame.mouse.get_pressed()[2]:
                node_arr[i].make_end()
                end_node = node_arr[i]
            draw_rect(surface, node_arr[i])
            break
    return start_node, end_node



def main():
    pygame.init()
    SCREEN_SIZE = 800
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()
    NUM_NODE = int(SCREEN_SIZE/NODE_WIDTH)

    node_arr = initilize(screen, NUM_NODE)
    start_node = None
    end_node = None

    open_set = []
    closed_set = []


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
                mouse_x_pos = math.floor(mouse_x_pos/NODE_WIDTH)
                mouse_y_pos = math.floor(mouse_y_pos/NODE_WIDTH)
                s_n, e_n = make_environment(screen, node_arr)
                if s_n != None:
                    start_node = s_n
                if e_n != None:
                    end_node = e_n
            
            if event.type == pygame.KEYDOWN:
                if len(open_set) == 0:
                    open_set.append(start_node)
                    current = None
                f_score_arr = []
                if event.key == pygame.K_SPACE:
                    for i in range(len(open_set)):
                        f_score_arr.append(open_set[i].get_f_score())
                
                index = f_score_arr.index(min(f_score_arr))
                current = open_set[index]
                
                closed_set.append(current)
                current.make_close()
                open_set.remove(current)
                draw_rect(screen, current)

                neighbor_arr = get_neighbor(current, NUM_NODE)
                for n in neighbor_arr:
                    neighbor_node = get_node(node_arr, n)
                    if n != None or neighbor_node.is_closed() == False:
                        if neighbor_node.is_wall() == False:
                            neighbor_node.set_parent(current)

                            if neighbor_node == end_node:
                                print("Success")
                                break
                            else:
                                neighbor_g_score = get_node_distance(current, start_node) + get_node_distance(neighbor_node, current)
                                neighbor_h_score = get_node_distance(neighbor_node, end_node)
                                neighbor_node.set_g_score(neighbor_g_score)
                                neighbor_node.set_h_score(neighbor_h_score)

                                new_neighbor_g_score = get_node_distance(neighbor_node, start_node)
                                
                                print('Total Score= ', neighbor_node.get_f_score(),'current_g: ',neighbor_g_score, ' new_g: ', new_neighbor_g_score)
                                if new_neighbor_g_score < neighbor_g_score or neighbor_node.is_open() == False:
                                    neighbor_node.set_g_score(new_neighbor_g_score)

                                    if neighbor_node.is_open() == False:
                                        neighbor_node.make_open()
                                        open_set.append(neighbor_node)


                    draw_rect(screen, neighbor_node)
                print('------------')





                                
                                    



                '''
                if current == end_node:
                    print ('Success')
                    break

                neighbor_arr = get_neighbor(current, NUM_NODE)

                for n in neighbor_arr:
                    neighbor_node = get_node(node_arr, n)
                    if n != None or neighbor_node.is_closed() == False:
                        if neighbor_node.is_wall() == False:

                            neighbor_node_g_score = get_node_distance(neighbor_node, start_node)
                            neighbor_node_h_score = get_node_distance(neighbor_node, end_node)

                            neighbor_node.set_g_score(neighbor_node_g_score + current.get_g_score())
                            neighbor_node.set_h_score(neighbor_node)



                            #get distance to re
                '''
                    
                

            

            

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

main()


