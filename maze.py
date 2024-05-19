import pygame
import random
import math
import collections

# Initialize Pygame
pygame.init()

# Maze dimensions
width, height = 500, 500
maze_size = 20  # Adjust for a more complex maze
block_size = width // maze_size

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

NUM_TREASURES = 12

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Maze Treasure Hunt')

# Load treasure image
treasure_image = pygame.image.load('treasure.png')
treasure_image = pygame.transform.scale(treasure_image, (block_size, block_size))

# Player and treasures
player_pos = (random.randint(0, maze_size-1), random.randint(0, maze_size-1))
treasures = tuple((random.randint(0, maze_size-1), random.randint(0, maze_size-1)) for _ in range(NUM_TREASURES))

# Generating walls and obstacles dynamically
def generate_walls():
    walls = []

    for i in range(1, maze_size-1):  # Avoid placing walls on the border
        for j in range(1, maze_size-1):
            if (i, j) != player_pos and (i, j) not in treasures and random.choice([True, False, False]):
                walls.append((i, j))
    return walls

def generate_water(slope):
    water = []
    water_size = min(maze_size, maze_size) // 2
    start_x = random.randint(0, maze_size - water_size)
    start_y = random.randint(0, maze_size - water_size)

    # Fill the square with water
    for i in range(start_x, start_x + water_size // 2):
        for j in range(start_y, start_y + water_size):
            water.append((i, j))
    return water

slope = 0.5  # This is a placeholder; adjust your slope logic as needed
water = generate_water(slope)
walls = generate_walls()


#### Player movement
#
# Adicione aqui a lógica de seu jogador
#
# O objetivo de uma função de callback de movimento do jogador
# é determinar a próxima ação do jogador com base no estado atual
# do jogo. Ela deve ser capaz de interagir com o estado do jogo, 
# como a posição atual do jogador e o layout do labirinto, para
# tomar decisões de movimento inteligentes ou aleatórias.
# 
# - Pode acessar mais não modificar variáveis globais -
#
#  A posição de agua e de parede é dada por variáveis globais:
#
#  water = generate_water(slope)
#
#  walls = generate_walls()
#
#  Sugestão 1: Juntar todas campos em um único grafo (grid)
#  para percorrer de maneira única
#
#  Sugestão 2: Cria uma classe para representar o modelo de mundo e outra
#  para encapsular a tomada de decisão
#

class Planner:
    def __init__(self):
        self.plano = []

planner = Planner()
planner.plano.append(3)

def move_player():
    # Você pode acessar qualquer variável global
    # Incluindo o grid
    global player_pos
    
    if random.randint(0, 5500) == 0:
        return 'GIVEUP'
    
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def manual_move():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return "GIVEUP"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                return "UP"
            elif event.key == pygame.K_s:
                return "DOWN"
            elif event.key == pygame.K_a:
                return "LEFT"
            elif event.key == pygame.K_d:
                return "RIGHT"
            elif event.key == pygame.K_ESCAPE:
                return "GIVEUP"
    return "NONE"

def bfs_move():
    pass

# Game loop
running = True
score = 0
steps = 0
while running:
    # Random movement for now    
    #direction = move_player()
    direction = manual_move() # Usar WASD
    score -= 1
    
    next_pos = player_pos
    if direction == 'UP':
        next_pos = (player_pos[0], player_pos[1] - 1) 
    elif direction == 'DOWN':
        next_pos = (player_pos[0], player_pos[1] + 1) 
    elif direction == 'LEFT':
        next_pos = (player_pos[0] - 1, player_pos[1]) 
    elif direction == 'RIGHT':
        next_pos = (player_pos[0] + 1, player_pos[1]) 
    elif direction == "NONE":
        score += 1
        steps -= 1
    else:
        print("Giving up")
        running = False;   
        
    px, py = next_pos          
    if (px, py) not in walls \
       and 0 <= next_pos[0] < maze_size \
       and 0 <= next_pos[1] < maze_size:
        player_pos = next_pos
    else:
        print("Invalid move!", next_pos)
        continue        

    # Drawing
    screen.fill(BLACK)
    for row in range(maze_size):
        for col in range(maze_size):
            rect = pygame.Rect(col*block_size, row*block_size, block_size, block_size)
            if (col, row) in walls:
                pygame.draw.rect(screen, BLACK, rect)
            elif (col, row) in water:
                pygame.draw.rect(screen, BLUE, rect)            
            else:
                pygame.draw.rect(screen, WHITE, rect)
            if (col, row) == (px, py):
                pygame.draw.rect(screen, RED, rect)
            elif (col, row) in treasures:
                pygame.draw.rect(screen, WHITE, rect)
                screen.blit(treasure_image, (col*block_size, row*block_size))

    if (px, py) in treasures:
        treasures = tuple(t for t in treasures if t != (px, py))
        print("Treasure found! Treasures left:", len(treasures))
        
    if len(treasures) <= 4:
        running = False   

    if (px, py) in water and direction != "NONE":
        score -= 5
        print("In water! Paying heavier price:", (px, py))
                
    pygame.display.flip()
    pygame.time.wait(100)  # Slow down the game a bit
    steps += 1
    if not treasures:
        running = False

found_treasures = NUM_TREASURES - len(treasures)
print(f"Found {found_treasures} treasures")
final_score = (found_treasures * 50) + score
print(f"Final score: {final_score}") 
pygame.quit()
