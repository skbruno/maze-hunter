
import pygame
import random
import heapq
import collections
import time
import matplotlib.pyplot as plt


def game(algorithm='bfs'):
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
    try:
        treasure_image = pygame.image.load('treasure.png')
        treasure_image = pygame.transform.scale(
            treasure_image, (block_size, block_size))
    except pygame.error:
        print(f"Error loading treasure image")
        return

    # Player and treasures
    player_pos = (random.randint(0, maze_size-1),
                  random.randint(0, maze_size-1))
    treasures = tuple((random.randint(
        0, maze_size-1), random.randint(0, maze_size-1)) for _ in range(NUM_TREASURES))

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

    def bfs_move(player_pos, treasures, walls):

        def is_valid_move(x, y):
            if 0 <= x < maze_size and 0 <= y < maze_size:
                if (x, y) not in walls:
                    return True
            return False

        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = collections.deque([(player_pos, [])])
        visited = set()
        visited.add(player_pos)

        while queue:
            current_pos, path = queue.popleft()
            if current_pos in treasures:
                # Return the first step in the path to the treasure
                return path[0] if path else None
            for direction in directions:
                next_x = current_pos[0] + direction[0]
                next_y = current_pos[1] + direction[1]
                if is_valid_move(next_x, next_y):
                    next_pos = (next_x, next_y)
                    if next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, path + [direction]))

        return None

    def dijkstra_move(player_pos, treasures, walls):

        def is_valid_move(x, y):
            if 0 <= x < maze_size and 0 <= y < maze_size:
                if (x, y) not in walls:
                    return True
            return False

        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        pq = [(0, player_pos, [])]  # (cost, current_pos, path)
        visited = set()

        while pq:
            cost, current_pos, path = heapq.heappop(pq)
            if current_pos in treasures:
                # Return the first step in the path to the treasure
                return path[0] if path else None
            if current_pos in visited:
                continue
            visited.add(current_pos)
            for direction in directions:
                next_x = current_pos[0] + direction[0]
                next_y = current_pos[1] + direction[1]
                if is_valid_move(next_x, next_y):
                    next_pos = (next_x, next_y)
                    if next_pos not in visited:
                        next_cost = cost + 1  # Each move costs 1
                        heapq.heappush(
                            pq, (next_cost, next_pos, path + [direction]))

        return None

    # Choose the move function based on the algorithm
    move_function = bfs_move if algorithm == 'bfs' else dijkstra_move

    # Game loop
    running = True
    score = 0
    steps = 0
    treasures_collected = 0
    start_time = time.perf_counter()

    while running:
        if treasures_collected > 7:
            running = False
            break

        # Get next move from the chosen algorithm
        next_move = move_function(player_pos, treasures, walls)
        if not next_move:
            print("No valid move found!")
            running = False
            break

        direction = next_move
        score -= 1
        next_pos = player_pos

        if direction == (-1, 0):
            next_pos = (player_pos[0] - 1, player_pos[1])  # UP
        elif direction == (1, 0):
            next_pos = (player_pos[0] + 1, player_pos[1])  # DOWN
        elif direction == (0, -1):
            next_pos = (player_pos[0], player_pos[1] - 1)  # LEFT
        elif direction == (0, 1):
            next_pos = (player_pos[0], player_pos[1] + 1)  # RIGHT
        elif direction == "NONE":
            score += 1
            steps -= 1
        else:
            print("Giving up")
            running = False

        px, py = next_pos

        if (px, py) not in walls and 0 <= next_pos[0] < maze_size and 0 <= next_pos[1] < maze_size:
            player_pos = next_pos
        else:
            print("Invalid move!", next_pos)
            continue

        # Drawing
        screen.fill(BLACK)
        for row in range(maze_size):
            for col in range(maze_size):
                rect = pygame.Rect(col * block_size, row *
                                   block_size, block_size, block_size)
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
                    screen.blit(treasure_image,
                                (col * block_size, row * block_size))

        if (px, py) in treasures:
            treasures = tuple(t for t in treasures if t != (px, py))
            treasures_collected += 1
            print(f"Treasure found! missing {
                  (NUM_TREASURES - 4) - treasures_collected} Treasures")

        if (px, py) in water and direction == "NONE":
            score -= 5
            print("In water! Paying heavier price:", (px, py))

        pygame.display.flip()
        pygame.time.wait(100)  # Slow down the game a bit
        steps += 1

    end_time = time.perf_counter()
    total_time = end_time - start_time

    found_treasures = NUM_TREASURES - len(treasures)
    print(f"Found {found_treasures} treasures")
    final_score = (found_treasures * 50) + score
    print(f"Final score: {final_score}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total steps: {steps}")
    pygame.quit()

    return found_treasures, final_score, total_time, steps


def run_comparisons(num_runs=10):
    results = {'bfs': [], 'dijkstra': []}

    for _ in range(num_runs):
        treasures, final_score, total_time, steps = game(algorithm='bfs')
        results['bfs'].append((treasures, final_score, total_time, steps))

        treasures, final_score, total_time, steps = game(algorithm='dijkstra')
        results['dijkstra'].append((treasures, final_score, total_time, steps))

    return results


def plot_results(results):
    bfs_results = results['bfs']
    dijkstra_results = results['dijkstra']

    metrics = ['Treasures', 'Score', 'Time', 'Steps']
    for i, metric in enumerate(metrics):
        plt.figure(figsize=(10, 5))
        bfs_data = [result[i] for result in bfs_results]
        dijkstra_data = [result[i] for result in dijkstra_results]

        plt.plot(range(len(bfs_data)), bfs_data, label='BFS', marker='o')
        plt.plot(range(len(dijkstra_data)), dijkstra_data,
                 label='Dijkstra', marker='x')
        plt.title(f'Comparison of {metric}')
        plt.xlabel('Run')
        plt.ylabel(metric)
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    results = run_comparisons(num_runs=10)
    plot_results(results)
