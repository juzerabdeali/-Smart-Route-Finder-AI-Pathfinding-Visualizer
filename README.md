# 📍 Smart Route Finder — AI Pathfinding Visualizer

A sleek, interactive, and modern AI-driven Pathfinding Visualizer built using Python and Pygame. This application provides real-time visualization of classic search algorithms operating on both unweighted and weighted grid systems, complete with custom maze generation and diagonal movement options.

---

<p align="center">
  <img src="banner.png" alt="Smart Route Finder Banner" width="100%">
</p>

---

<p align="center">
  <a href="#-features">✨ Features</a> •
  <a href="#-algorithms-comparison">🧠 Algorithms</a> •
  <a href="#-controls-guide">🎮 Controls</a> •
  <a href="#-installation--setup">⚙️ Installation</a> •
  <a href="#-the-team">👥 The Team</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Pygame-2.0%2B-green?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame Version">
  <img src="https://img.shields.io/badge/Algorithms-A%2A%20%7C%20Dijkstra%20%7C%20BFS%20%7C%20DFS-orange?style=for-the-badge" alt="Algorithms Support">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge" alt="License Badge">
</p>

---

## ✨ Features

- **🎮 Dynamic Controls**: Intuitive sidebar UI to control the visualization settings.
- **🛣️ Weighted Terrain (Mud Tiles)**: Add complexity to the routing by painting weighted tiles (cost = 5) versus standard walls (blocking).
- **📐 Diagonal Traversal**: Toggle between 4-directional and 8-directional movement in real-time.
- **🌀 Procedural Maze Generation**: Automatic maze generation using recursive backtracking.
- **📊 Real-time Stats**: Tracks the count of **Nodes Explored** and the total **Path Cost** to measure and compare algorithm efficiency.
- **🎨 Modern Design System**: Refined dark and light color accents (indigo, turquoise, gold, stone) instead of harsh primary colors.

---

## 🧠 Algorithms Comparison

Compare how different search strategies find paths:

| Algorithm | Type | Shortest Path Guarantee? | Weighted Terrain Support? | Best Use Case |
| :--- | :--- | :---: | :---: | :--- |
| **⭐ A* Search** | Informed (Heuristic) | **Yes** (using Manhattan / Euclidean) | **Yes** | Optimal pathfinding on general terrain maps |
| **⚡ Dijkstra** | Uninformed | **Yes** | **Yes** | Finding the shortest path with varying cost/weights |
| **🔍 BFS (Breadth-First)** | Uninformed | **Yes** (on unweighted grids only) | *No* | Simple shortest paths on grids without weights |
| **🪜 DFS (Depth-First)** | Uninformed | *No* | *No* | Exploring paths to the absolute depth, maze generation |

### Heuristics Mode (A* Specific)
- **Manhattan Distance**: Used when diagonal movement is **Disabled**.
- **Euclidean Distance**: Used when diagonal movement is **Enabled** to ensure admissibility.

---

## 🎮 Controls Guide

The application uses mouse clicks for canvas drawing and sidebar button triggers.

### Canvas Controls
- **Left-Click (1st Click)**: Set **Start Node** (Turquoise tile)
- **Left-Click (2nd Click)**: Set **End Node** (Orange tile)
- **Left-Click & Drag**: Paint obstacles based on current **Mode**:
  - `Wall Mode`: Paints impassable black barriers.
  - `Mud Mode`: Paints weighted grey tiles (movement cost = 5).
  - *Note: Hold down the `M` key while dragging to paint mud tiles directly!*
- **Right-Click**: Erase nodes or barriers to reset the grid cells.

### Control Panel Buttons
- **Algorithm Selectors**: Pick between `A* Search`, `Dijkstra`, `BFS`, or `DFS`.
- **Toggle Diagonal**: Enable 8-way movement.
- **Mode: Wall / Mud**: Toggle the current drawing paint.
- **Generate Maze**: Automatically builds a randomized maze using recursive backtracking.
- **Clear Grid**: Resets the entire grid (removes walls, path, and stats).
- **Clear Path**: Resets the solved path and explored nodes while keeping barriers intact.
- **START PATHFINDING**: Runs the selected algorithm step-by-step with real-time visualization.

---

## ⚙️ Installation & Setup

Ensure you have Python 3.8+ installed on your computer.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/smart-route-finder.git
cd smart-route-finder
```

### 2. Install Dependencies
Install the required library (`pygame`):
```bash
pip install pygame
```

### 3. Run the Visualizer
Execute the main application file:
```bash
python main.py
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
