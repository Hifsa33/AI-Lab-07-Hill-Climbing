
import tkinter as tk
from tkinter import messagebox

# Romania road map: road distances in km
graph = {
    "Arad": {"Zerind": 75, "Timisoara": 118, "Sibiu": 140},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Dobreta": 75},
    "Dobreta": {"Mehadia": 75, "Craiova": 120},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99,
              "Rimnicu Vilcea": 80},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97,
                       "Craiova": 146},
    "Craiova": {"Dobreta": 120, "Rimnicu Vilcea": 146,
                "Pitesti": 138},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138,
                "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101,
                  "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98,
                 "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

# Straight-line distance to Bucharest from the lab figure
heuristic = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160,
    "Dobreta": 242, "Eforie": 161, "Fagaras": 176,
    "Giurgiu": 77, "Hirsova": 151, "Iasi": 226,
    "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193,
    "Sibiu": 253, "Timisoara": 329, "Urziceni": 80,
    "Vaslui": 199, "Zerind": 374
}

# Approximate positions for drawing the Romania map
positions = {
    "Arad": (90, 190), "Zerind": (140, 110),
    "Oradea": (210, 55), "Timisoara": (105, 285),
    "Lugoj": (185, 330), "Mehadia": (185, 390),
    "Dobreta": (185, 455), "Sibiu": (285, 210),
    "Rimnicu Vilcea": (340, 280), "Craiova": (350, 430),
    "Fagaras": (405, 190), "Pitesti": (435, 320),
    "Bucharest": (540, 365), "Giurgiu": (515, 455),
    "Urziceni": (620, 325), "Hirsova": (720, 320),
    "Eforie": (770, 405), "Vaslui": (680, 210),
    "Iasi": (650, 130), "Neamt": (580, 75)
}

def hill_climbing(start, goal):
    current = start
    path = [current]
    steps = []

    while current != goal:
        neighbors = graph[current]
        best = min(neighbors, key=lambda city: heuristic[city])

        steps.append(
            f"{current} (h={heuristic[current]}) -> "
            f"{best} (h={heuristic[best]})"
        )

        if heuristic[best] >= heuristic[current]:
            steps.append("Stopped: no better neighboring city.")
            break

        current = best
        path.append(current)

    return path, steps, current == goal

def run_search():
    start = start_var.get()
    goal = goal_var.get()

    if start not in graph or goal not in graph:
        messagebox.showerror("Error", "Select valid cities.")
        return

    path, steps, success = hill_climbing(start, goal)
    draw_map(path)

    output.delete("1.0", tk.END)
    output.insert(tk.END, "Hill Climbing Search\n")
    output.insert(tk.END, "--------------------\n")
    output.insert(tk.END, "\n".join(steps))
    output.insert(tk.END, "\n\nPath: " + " -> ".join(path))
    output.insert(
        tk.END,
        "\n\nResult: " + ("Goal reached!" if success
                         else "Search stopped before goal.")
    )

def draw_map(path=None):
    path = path or []
    canvas.delete("all")
    path_edges = set()

    for i in range(len(path) - 1):
        path_edges.add(frozenset((path[i], path[i + 1])))

    # Draw roads
    for city, neighbors in graph.items():
        x1, y1 = positions[city]
        for neighbor in neighbors:
            if city < neighbor:
                x2, y2 = positions[neighbor]
                color = "red" if frozenset((city, neighbor)) in path_edges else "gray"
                width = 4 if color == "red" else 2
                canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    # Draw cities
    for city, (x, y) in positions.items():
        color = "lightgreen" if city in path else "white"
        if city == "Arad":
            color = "lightblue"
        if city == "Bucharest":
            color = "orange"

        canvas.create_oval(x-6, y-6, x+6, y+6,
                           fill=color, outline="black", width=2)
        canvas.create_text(x, y-15, text=city, font=("Arial", 8, "bold"))

root = tk.Tk()
root.title("Lab Task 1 - Romania Map Hill Climbing")
root.geometry("1050x780")

tk.Label(root, text="Romania Map: Hill Climbing",
         font=("Arial", 16, "bold")).pack(pady=8)

controls = tk.Frame(root)
controls.pack()

tk.Label(controls, text="Start city:").grid(row=0, column=0, padx=5)
start_var = tk.StringVar(value="Arad")
tk.OptionMenu(controls, start_var, *sorted(graph)).grid(row=0, column=1)

tk.Label(controls, text="Goal city:").grid(row=0, column=2, padx=5)
goal_var = tk.StringVar(value="Bucharest")
tk.OptionMenu(controls, goal_var, *sorted(graph)).grid(row=0, column=3)

tk.Button(controls, text="Run Hill Climbing",
          command=run_search, bg="lightblue").grid(
              row=0, column=4, padx=10)

canvas = tk.Canvas(root, width=850, height=500, bg="white")
canvas.pack(pady=8)

output = tk.Text(root, height=8, width=110, font=("Consolas", 10))
output.pack(pady=8)

draw_map()
root.mainloop()
