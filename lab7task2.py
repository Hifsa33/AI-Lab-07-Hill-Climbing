
import tkinter as tk
from tkinter import messagebox
from collections import deque

# Exact layout from the Word document.
# Rows are written from top (y=5) to bottom (y=0).
maze = [
    ["#", "#", "W", "#", "X", "Y"],
    ["R", "S", "T", "U", "#", "V"],
    ["M", "N", "#", "O", "P", "Q"],
    ["H", "I", "J", "#", "K", "L"],
    ["F", "#", "G", "#", "#", "#"],
    ["A", "#", "B", "C", "D", "E"]
]

ROWS = len(maze)
COLS = len(maze[0])

positions = {
    maze[r][c]: (r, c)
    for r in range(ROWS)
    for c in range(COLS)
    if maze[r][c] != "#"
}

START = "A"
GOAL = "Y"

def neighbors(pos):
    r, c = pos
    result = []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc

        if (0 <= nr < ROWS and 0 <= nc < COLS
                and maze[nr][nc] != "#"):
            result.append((nr, nc))

    return result

def make_heuristic(goal):
    # Shortest traversable distance from every cell to the goal.
    goal_pos = positions[goal]
    distance = {goal_pos: 0}
    queue = deque([goal_pos])

    while queue:
        current = queue.popleft()

        for nxt in neighbors(current):
            if nxt not in distance:
                distance[nxt] = distance[current] + 1
                queue.append(nxt)

    return distance

def hill_climbing(start, goal):
    h = make_heuristic(goal)
    current = positions[start]
    goal_pos = positions[goal]
    path = [current]
    visited = {current}
    steps = []

    if current not in h:
        return path, steps, False

    while current != goal_pos:
        options = [
            p for p in neighbors(current)
            if p in h and p not in visited
        ]

        if not options:
            steps.append(
                f"Stopped at {maze[current[0]][current[1]]}: "
                "no unvisited neighbors."
            )
            return path, steps, False

        best = min(options, key=lambda p: h[p])

        current_name = maze[current[0]][current[1]]
        best_name = maze[best[0]][best[1]]

        steps.append(
            f"{current_name} (h={h[current]}) -> "
            f"{best_name} (h={h[best]})"
        )

        if h[best] >= h[current]:
            steps.append("Stopped: no improving neighbor.")
            return path, steps, False

        current = best
        path.append(current)
        visited.add(current)

    return path, steps, True

def run_search():
    start = start_entry.get().strip().upper()
    goal = goal_entry.get().strip().upper()

    if start not in positions or goal not in positions:
        messagebox.showerror(
            "Input Error",
            "Enter valid maze labels, such as A and Y."
        )
        return

    path, steps, success = hill_climbing(start, goal)
    draw_maze(path)

    path_names = [maze[r][c] for r, c in path]

    output.delete("1.0", tk.END)
    output.insert(tk.END, "Hill Climbing Search\n")
    output.insert(tk.END, "--------------------\n")
    output.insert(tk.END, "\n".join(steps))
    output.insert(tk.END, "\n\nPath: " + " -> ".join(path_names))
    output.insert(
        tk.END,
        "\n\nResult: " + ("Goal reached!" if success
                         else "Search stopped before goal.")
    )

def draw_maze(path=None):
    path = path or []
    path_set = set(path)

    for widget in maze_frame.winfo_children():
        widget.destroy()

    for r in range(ROWS):
        for c in range(COLS):
            cell = maze[r][c]

            if cell == "#":
                color = "blue"
                text = ""
                fg = "white"
            else:
                color = "white"
                text = cell
                fg = "black"

            if (r, c) in path_set and cell != "#":
                color = "lightgreen"

            if cell == START:
                color = "limegreen"
            elif cell == GOAL:
                color = "limegreen"

            tk.Label(
                maze_frame,
                text=text,
                width=6,
                height=2,
                bg=color,
                fg=fg,
                relief="solid",
                borderwidth=1,
                font=("Arial", 12, "bold")
            ).grid(row=ROWS - 1 - r, column=c, padx=1, pady=1)

root = tk.Tk()
root.title("Lab Task 2 - Maze Hill Climbing")
root.geometry("650x650")

tk.Label(
    root,
    text="Maze Problem - Hill Climbing",
    font=("Arial", 16, "bold")
).pack(pady=10)

controls = tk.Frame(root)
controls.pack(pady=5)

tk.Label(controls, text="Start:").grid(row=0, column=0, padx=5)
start_entry = tk.Entry(controls, width=6)
start_entry.insert(0, "A")
start_entry.grid(row=0, column=1, padx=5)

tk.Label(controls, text="Goal:").grid(row=0, column=2, padx=5)
goal_entry = tk.Entry(controls, width=6)
goal_entry.insert(0, "Y")
goal_entry.grid(row=0, column=3, padx=5)

tk.Button(
    controls,
    text="Run Search",
    command=run_search,
    bg="lightblue"
).grid(row=0, column=4, padx=10)

maze_frame = tk.Frame(root)
maze_frame.pack(pady=15)

output = tk.Text(root, width=75, height=12, font=("Consolas", 10))
output.pack(pady=10)

draw_maze()
root.mainloop()
