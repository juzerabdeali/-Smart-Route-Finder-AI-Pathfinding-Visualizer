import pygame
import math
from components import Node, WHITE, BLACK, GREY, TURQUOISE, ORANGE, BLUE, PURPLE, GOLD, MUD, SIDEBAR_BG
from algorithms import a_star, dijkstra, bfs, dfs, generate_maze

# Configuration
GRID_WIDTH = 630  
SIDEBAR_WIDTH = 300
WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
ROWS = 35

pygame.init()
WIN = pygame.display.set_mode((WIDTH, GRID_WIDTH))
pygame.display.set_caption("Smart Route Finder - A* Search Visualization")
FONT = pygame.font.SysFont("inter", 18)
FONT_BOLD = pygame.font.SysFont("inter", 20, bold=True)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, win):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        text_surf = FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_sidebar(win, buttons, stats, selected_algo, diagonal):
    sidebar_rect = pygame.Rect(GRID_WIDTH, 0, SIDEBAR_WIDTH, GRID_WIDTH)
    pygame.draw.rect(win, SIDEBAR_BG, sidebar_rect)
    
    # Title
    title = FONT_BOLD.render("CONTROL PANEL", True, BLACK)
    win.blit(title, (GRID_WIDTH + 20, 20))
    
    # Stats
    y_offset = 60
    for key, value in stats.items():
        stat_text = FONT.render(f"{key}: {value}", True, BLACK)
        win.blit(stat_text, (GRID_WIDTH + 20, y_offset))
        y_offset += 25
    
    # Selected Info
    algo_text = FONT.render(f"Algorithm: {selected_algo}", True, BLUE)
    win.blit(algo_text, (GRID_WIDTH + 20, y_offset))
    y_offset += 22
    diag_text = FONT.render(f"Diagonal: {'ON' if diagonal else 'OFF'}", True, PURPLE)
    win.blit(diag_text, (GRID_WIDTH + 20, y_offset))
    
    # Buttons
    for btn in buttons:
        btn.draw(win)

def draw(win, grid, rows, width, buttons, stats, selected_algo, diagonal):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    draw_sidebar(win, buttons, stats, selected_algo, diagonal)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    if y >= width: return None # Outside grid
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    grid = make_grid(ROWS, width)
    start = None
    end = None
    
    selected_algo = "A*"
    diagonal_enabled = False
    placement_mode = "Wall"  
    stats = {"Nodes Explored": 0, "Path Cost": 0}
    
    def create_buttons(algo, diag, mode):
        btn_x = GRID_WIDTH + 20
        return [
            Button(btn_x, 210, 260, 35, "A* Search", (59, 130, 246), (37, 99, 235)),
            Button(btn_x, 250, 260, 35, "Dijkstra", (99, 102, 241), (79, 70, 229)),
            Button(btn_x, 290, 260, 35, "BFS (Unweighted)", (139, 92, 246), (124, 58, 237)),
            Button(btn_x, 330, 260, 35, "DFS", (168, 85, 247), (147, 51, 234)),
            Button(btn_x, 370, 260, 35, "Toggle Diagonal", (20, 184, 166), (13, 148, 136)),
            Button(btn_x, 410, 260, 35, f"Mode: {mode}", (120, 113, 108), (100, 93, 88)),
            Button(btn_x, 450, 260, 35, "Generate Maze", (249, 115, 22), (234, 88, 12)),
            Button(btn_x, 490, 125, 35, "Clear Grid", (239, 68, 68), (220, 38, 38)),
            Button(btn_x + 135, 490, 125, 35, "Clear Path", (107, 114, 128), (75, 85, 99)),
            Button(btn_x, 535, 260, 50, "START PATHFINDING", (34, 197, 94), (22, 163, 74)),
        ]

    buttons = create_buttons(selected_algo, diagonal_enabled, placement_mode)

    run = True
    while run:
        draw(win, grid, ROWS, width, buttons, stats, selected_algo, diagonal_enabled)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Button Hover
            for btn in buttons:
                btn.check_hover(mouse_pos)

            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                row_col = get_clicked_pos(mouse_pos, ROWS, width)
                if row_col:
                    row, col = row_col
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()

                    elif not end and node != start:
                        end = node
                        end.make_end()

                    elif node != end and node != start:
                        if placement_mode == "Mud" or pygame.key.get_pressed()[pygame.K_m]:
                            node.make_mud()
                        else:
                            node.make_barrier()
                else: # Check Sidebar Buttons
                    for btn in buttons:
                        if btn.is_hovered:
                            if btn.text == "A* Search": selected_algo = "A*"
                            elif btn.text == "Dijkstra": selected_algo = "Dijkstra"
                            elif btn.text == "BFS (Unweighted)": selected_algo = "BFS"
                            elif btn.text == "DFS": selected_algo = "DFS"
                            elif btn.text == "Toggle Diagonal": diagonal_enabled = not diagonal_enabled
                            elif "Mode:" in btn.text:
                                placement_mode = "Mud" if placement_mode == "Wall" else "Wall"
                            elif btn.text == "Generate Maze":
                                generate_maze(lambda: draw(win, grid, ROWS, width, buttons, stats, selected_algo, diagonal_enabled), grid)
                                start = end = None
                            elif btn.text == "Clear Grid":
                                start = end = None
                                grid = make_grid(ROWS, width)
                                stats = {"Nodes Explored": 0, "Path Cost": 0}
                            elif btn.text == "Clear Path":
                                for row in grid:
                                    for node in row:
                                        if node.color in [BLUE, PURPLE, GOLD]: node.reset()
                                stats = {"Nodes Explored": 0, "Path Cost": 0}
                            elif btn.text == "START PATHFINDING" and start and end:
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid, diagonal_enabled)
                                
                                cost, explored = None, 0
                                draw_fn = lambda: draw(win, grid, ROWS, width, buttons, stats, selected_algo, diagonal_enabled)
                                if selected_algo == "A*":
                                    cost, explored = a_star(draw_fn, grid, start, end, "euclidean" if diagonal_enabled else "manhattan")
                                elif selected_algo == "Dijkstra":
                                    cost, explored = dijkstra(draw_fn, grid, start, end)
                                elif selected_algo == "BFS":
                                    cost, explored = bfs(draw_fn, grid, start, end)
                                elif selected_algo == "DFS":
                                    cost, explored = dfs(draw_fn, grid, start, end)
                                
                                if cost is not None:
                                    stats["Path Cost"] = round(cost, 2)
                                    stats["Nodes Explored"] = explored
                                else:
                                    stats["Path Cost"] = "N/A"
                                    stats["Nodes Explored"] = explored
                            
                            # Refresh buttons to update text (Mode, etc.)
                            buttons = create_buttons(selected_algo, diagonal_enabled, placement_mode)

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                row_col = get_clicked_pos(mouse_pos, ROWS, width)
                if row_col:
                    row, col = row_col
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

    pygame.quit()

if __name__ == "__main__":
    main(WIN, GRID_WIDTH)
