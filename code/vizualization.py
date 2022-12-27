import pygame
import os
import numpy as np
import colorsys
import math
import sys


pygame.display.init()
pygame.init()
pygame.font.init()

# print('get_driver:', pygame.display.get_driver())

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("-----------")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (19, 138, 7)
BLUE = (0, 0, 255)
SHADOW_BLUE = (180, 190, 250) 
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

H_CELL_NUM = 7
V_CELL_NUM = 5
PLAYER_NUM = 0


SCORE_FONT = pygame.font.SysFont('comicsans', 25)


FPS = 10

def read_file(file_name, player_num):
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()

    lines = [line for line in lines if line.startswith(str(player_num))]
    return lines

def hsv_to_rgb(hsv_value):
    h,s,v = hsv_value
    return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h/255, s/255, v/255))

def draw_grid():

    WIN.fill(WHITE)  
    for i in range(0, WIDTH, WIDTH//H_CELL_NUM):
        pygame.draw.line(WIN, BLACK, (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, HEIGHT//V_CELL_NUM):
        pygame.draw.line(WIN, BLACK, (0, i), (WIDTH, i), 1)


def draw_triangle(x, y, color, size):
    pygame.draw.polygon(WIN, color, ((x, y), (x+20, y), (x+10, y+20)))

def draw_shadow(action, state):

    if state[H_CELL_NUM//2][V_CELL_NUM//2][1] <= 0:
        x = WIDTH//H_CELL_NUM * H_CELL_NUM/2
        y = HEIGHT//V_CELL_NUM * (V_CELL_NUM/2)
        if action == 0:

            pygame.draw.polygon(WIN, BLACK, ((x-5, y+25), (x, y+30), (x+5, y+25)))
            # pygame.draw.circle(WIN, SHADOW_BLUE, (WIDTH//H_CELL_NUM * H_CELL_NUM/2 , HEIGHT//V_CELL_NUM * (V_CELL_NUM/2-1) ), 20)
        elif action == 1:
            pygame.draw.polygon(WIN, BLACK, ((x-5, y-25), (x, y-30), (x+5, y-25)))
            # pygame.draw.circle(WIN, SHADOW_BLUE, (WIDTH//H_CELL_NUM * H_CELL_NUM/2 , HEIGHT//V_CELL_NUM * (V_CELL_NUM/2+1) ), 20)
        elif action == 2:
            pygame.draw.polygon(WIN, BLACK, ((x+25, y-5), (x+30, y), (x+25, y+5)))
            # pygame.draw.circle(WIN, SHADOW_BLUE, (WIDTH//H_CELL_NUM * (H_CELL_NUM/2-1) , HEIGHT//V_CELL_NUM * V_CELL_NUM/2 ), 20)
        elif action == 3:
            pygame.draw.polygon(WIN, BLACK, ((x-25, y-5), (x-30, y), (x-25, y+5)))
            # pygame.draw.circle(WIN, SHADOW_BLUE, (WIDTH//H_CELL_NUM * (H_CELL_NUM/2+1) , HEIGHT//V_CELL_NUM * V_CELL_NUM/2 ), 20)

    

def draw_players(state):
    #draw circle in the middle of the cell
    # for i in range(len(env)):
    #     player = env[i]
    #     x = player.x
    #     y = player.y
    #     pygame.draw.circle(WIN, BLACK, (x*100+50, y*100+50), 20)
    # pygame.draw.circle(WIN, RED, (WIDTH//H_CELL_NUM * H_CELL_NUM/2, HEIGHT//V_CELL_NUM * V_CELL_NUM/2), 30)

    sh = state.shape
    for i in range(sh[0]):
        for j in range(sh[1]):

            life = state[i][j][0]
            p1_life = state[i][j][1]
            p1_xp = state[i][j][2]
            p2_life = state[i][j][3]
            p2_xp = state[i][j][4]

            if( i== V_CELL_NUM//2 and j==H_CELL_NUM//2):
                draw_life(p1_life)
                draw_score(p1_xp)
                

            if life > 0:

                color = (100, 100-life, 50)
                color_rgb = hsv_to_rgb(color)
                print(color_rgb)

                pygame.draw.rect(WIN, color_rgb, (WIDTH//H_CELL_NUM * j , HEIGHT//V_CELL_NUM * i , WIDTH//H_CELL_NUM, HEIGHT//V_CELL_NUM))
            


            if p1_life > 0 and p2_life<=0:
                if( i== V_CELL_NUM//2 and j==H_CELL_NUM//2):
                    pygame.draw.circle(WIN, BLUE, (WIDTH//H_CELL_NUM * j + WIDTH//H_CELL_NUM//2, HEIGHT//V_CELL_NUM * i + HEIGHT//V_CELL_NUM//2), 20)
                else:
                    pygame.draw.circle(WIN, ORANGE, (WIDTH//H_CELL_NUM * j + WIDTH//H_CELL_NUM//2, HEIGHT//V_CELL_NUM * i + HEIGHT//V_CELL_NUM//2), 20)


            elif p1_life >0:

                pygame.draw.circle(WIN, BLUE, (WIDTH//H_CELL_NUM * j + 15, HEIGHT//V_CELL_NUM * i + 15), 10)
                pygame.draw.circle(WIN, ORANGE, (WIDTH//H_CELL_NUM * (j+1) - 15, HEIGHT//V_CELL_NUM * (i+1) -15 ), 10)
                 




def draw_life(life):
    bar_width = 100
    bar_height = 20

    pygame.draw.rect(WIN, GREY, (10, 10, bar_width, bar_height), border_radius=5)
    pygame.draw.rect(WIN, GREEN, (10, 10, life, bar_height), border_radius=5)
    pass

def draw_score(score):

    socre_text = SCORE_FONT.render(
        "SCORE: " + str(score), 1, BLACK)
    WIN.blit(socre_text, (WIDTH - socre_text.get_width() - 5, 10))


def get_game_records_files( dir_name):
    experience_dir  = os.path.join("..", "models",dir_name )
    files = os.listdir(experience_dir)
    files = [file for file in files if file.startswith("game_record")]
    files.sort(key = lambda x: int((x.split("_")[2]).split(".")[0]))
    print(files)
    return experience_dir , files

def next_line( files, exp_dir, player_num, index, file_index, lines):


    if index >= len(lines)-1:
        file_index+=1
        index=0


        if file_index<len(files):
            lines = read_file(os.path.join(exp_dir, files[file_index]), player_num)
        else:
            return None, None, None
    else:
        index+=1

    return file_index, index, lines[index]

    
        
    

def process_line(line):

    line = line.split(",")
    id = int(line[0])
    past = (line[1:176])
    past_arr = np.array([eval(i) for i in past])
    past_arr = past_arr.reshape(V_CELL_NUM, H_CELL_NUM, 5)
    
    action = int(line[176])
    current = (line[177:len(line)])
    current_arr = np.array([eval(i) for i in current])
    current_arr = current_arr.reshape(V_CELL_NUM, H_CELL_NUM, 5)
    return id, past_arr, action, current_arr


def draw_window(past, current, action):

    draw_grid()

    draw_players(current)
    draw_shadow(action, current)




    pygame.display.update()



def main():
    run = True
    pause= False
    PLAYER_NUM = int(sys.argv[1])
    clock = pygame.time.Clock()

    exp_dir, files = get_game_records_files("model_100000_pure_collect_seed_reward_3_gamma_0.99")


    index=-1
    file_index=0
    lines = read_file(os.path.join(exp_dir, files[file_index]), PLAYER_NUM)


    # for i in lines:
    #     print(i)
    #     print()
    #     print()
    #     print()

    past_past=np.array([])
    
    while run:
        if not pause:
            # pygame.time.wait(1000)
            clock.tick(5)
            
            file_index, index, line = next_line( files, exp_dir, PLAYER_NUM, index, file_index, lines)

            if line is None:
                print("end of files")
                pygame.time.wait(10000)

                break
            # print(line)
            id, past, action, current = process_line(line)

            

            # print(id)
            # print(past)
            # print(action)
            # print("dwadnaowidhawo")
            if id is not PLAYER_NUM:
                print("wrong player number")
                break

            draw_window(past, current, action)

        # if(np.all(past == past_past)):
        #     print("same state")
        #     break
        # past_past = np.array(current)
        
        # pygame.time.wait(1000)


        # pygame.draw.circle(WIN, color_rgb, (WIDTH//H_CELL_NUM * H_CELL_NUM/2, HEIGHT//V_CELL_NUM * V_CELL_NUM/2), 30)
        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                

                



    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
    input()
    

