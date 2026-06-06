import pygame
import random
import math
from queue import PriorityQueue, Queue, deque

def h_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current, draw):
    cost = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        cost += current.weight
        draw()
    return cost

def a_star(draw, grid, start, end, heuristic_type="manhattan"):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    
    h = h_manhattan if heuristic_type == "manhattan" else h_euclidean
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    nodes_explored = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_explored += 1

        if current == end:
            cost = reconstruct_path(came_from, end, draw)
            end.make_end()
            return cost, nodes_explored

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
        pygame.time.delay(2)

    return None, nodes_explored

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}
    nodes_explored = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_explored += 1

        if current == end:
            cost = reconstruct_path(came_from, end, draw)
            end.make_end()
            return cost, nodes_explored

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
        pygame.time.delay(2)

    return None, nodes_explored

def bfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}
    nodes_explored = 0

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()
        nodes_explored += 1

        if current == end:
            cost = reconstruct_path(came_from, end, draw)
            end.make_end()
            return cost, nodes_explored

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
        pygame.time.delay(2)

    return None, nodes_explored

def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}
    nodes_explored = 0

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        nodes_explored += 1

        if current == end:
            cost = reconstruct_path(came_from, end, draw)
            end.make_end()
            return cost, nodes_explored

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
        pygame.time.delay(2)

    return None, nodes_explored

def generate_maze(draw, grid):
    """Recursive Backtracking Maze Generation."""
    for row in grid:
        for node in row:
            node.make_barrier()
    
    def get_neighbors(node):
        r, c = node.get_pos()
        neighbors = []
        if r > 1: neighbors.append(grid[r-2][c])
        if r < len(grid) - 2: neighbors.append(grid[r+2][c])
        if c > 1: neighbors.append(grid[r][c-2])
        if c < len(grid[0]) - 2: neighbors.append(grid[r][c+2])
        return neighbors

    def remove_wall(node1, node2):
        r1, c1 = node1.get_pos()
        r2, c2 = node2.get_pos()
        grid[(r1 + r2) // 2][(c1 + c2) // 2].reset()

    start_node = grid[1][1]
    start_node.reset()
    stack = [start_node]
    visited = {start_node}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack[-1]
        neighbors = [n for n in get_neighbors(current) if n not in visited]

        if neighbors:
            next_node = random.choice(neighbors)
            remove_wall(current, next_node)
            next_node.reset()
            visited.add(next_node)
            stack.append(next_node)
        else:
            stack.pop()
        
        draw()
