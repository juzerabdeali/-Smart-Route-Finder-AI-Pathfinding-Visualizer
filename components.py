import pygame

# Standard Modern Color Palette
WHITE = (248, 249, 250)
BLACK = (33, 37, 41)       # Barrier
GREY = (173, 181, 189)      # Grid lines
TURQUOISE = (20, 184, 166)  # Start
ORANGE = (249, 115, 22)    # End
BLUE = (59, 130, 246)      # Open Set
PURPLE = (139, 92, 246)    # Closed Set
GOLD = (234, 179, 8)       # Path
MUD = (120, 113, 108)      # Weighted terrain (Mud)
SIDEBAR_BG = (241, 245, 249)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == PURPLE

    def is_open(self):
        return self.color == BLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == TURQUOISE

    def is_end(self):
        return self.color == ORANGE
    
    def is_mud(self):
        return self.color == MUD

    def reset(self):
        self.color = WHITE
        self.weight = 1

    def make_start(self):
        self.color = TURQUOISE

    def make_closed(self):
        self.color = PURPLE

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = GOLD
        
    def make_mud(self):
        self.color = MUD
        self.weight = 5

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, allow_diagonal=False):
        self.neighbors = []
        # Standard Neighbors
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        # Diagonal Neighbors
        if allow_diagonal:
            # DOWN-RIGHT
            if self.row < self.total_rows - 1 and self.col < self.total_rows - 1:
                if not grid[self.row + 1][self.col + 1].is_barrier():
                    self.neighbors.append(grid[self.row + 1][self.col + 1])
            # DOWN-LEFT
            if self.row < self.total_rows - 1 and self.col > 0:
                if not grid[self.row + 1][self.col - 1].is_barrier():
                    self.neighbors.append(grid[self.row + 1][self.col - 1])
            # UP-RIGHT
            if self.row > 0 and self.col < self.total_rows - 1:
                if not grid[self.row - 1][self.col + 1].is_barrier():
                    self.neighbors.append(grid[self.row - 1][self.col + 1])
            # UP-LEFT
            if self.row > 0 and self.col > 0:
                if not grid[self.row - 1][self.col - 1].is_barrier():
                    self.neighbors.append(grid[self.row - 1][self.col - 1])

    def __lt__(self, other):
        return False
