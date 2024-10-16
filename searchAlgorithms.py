import heapq
from collections import deque, defaultdict
import re
from itertools import count

# Global variables for input and output file names
input_file = "input.txt"
output_file = "output.txt"

# Function to validate state names
def is_valid_state_name(state_name):
    return bool(re.match(r'^[a-zA-Z0-9/]+$', state_name))

# Function to read the input file
def read_input(file_name=input_file):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        algo = lines[0].strip()
        start_state = lines[1].strip()
        goal_state = lines[2].strip()

        if not start_state or not goal_state:
            raise ValueError("Start state or goal state cannot be empty.")

        if not is_valid_state_name(start_state) or not is_valid_state_name(goal_state):
            raise ValueError("Invalid state names.")

        num_live_traffic_lines = int(lines[3].strip())
        live_traffic = defaultdict(list)
        seen_entries = set()

        for i in range(4, 4 + num_live_traffic_lines):
            state1, state2, time = lines[i].strip().split()
            time = int(time)

            if time < 0:
                raise ValueError("Travel times must be non-negative.")
            if not is_valid_state_name(state1) or not is_valid_state_name(state2):
                raise ValueError("Invalid state names.")
            if (state1, state2) in seen_entries:
                raise ValueError(f"Duplicate entry: {state1} -> {state2}.")
            seen_entries.add((state1, state2))

            live_traffic[state1].append((state2, time))

        sunday_traffic = {}
        num_sunday_traffic_lines = int(lines[4 + num_live_traffic_lines].strip())
        for i in range(5 + num_live_traffic_lines, 5 + num_live_traffic_lines + num_sunday_traffic_lines):
            state, time = lines[i].strip().split()
            sunday_traffic[state] = int(time)

        for state in live_traffic.keys():
            if state not in sunday_traffic:
                raise ValueError(f"No Sunday traffic data for state: {state}")

        return algo, start_state, goal_state, live_traffic, sunday_traffic
    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{file_name}' was not found.")
    except ValueError as e:
        raise ValueError(f"Input error: {e}")

# Function to write the output file
def write_output(path, costs, file_name=output_file):
    with open(file_name, 'w') as file:
        file.write(f"{path[0]} 0\n")
        for i in range(1, len(path)):
            file.write(f"{path[i]} {costs[i]}\n")

# Function to reconstruct the path
def reconstruct_path(parent, goal_state):
    path = []
    current = goal_state
    while current:
        path.append(current)
        current = parent.get(current)
    return path[::-1]

# BFS Algorithm
def bfs(start, goal, live_traffic):
    frontier = deque([start])
    parent = {start: None}
    cost = {start: 0}
    explored = set()

    while frontier:
        current = frontier.popleft()
        if current == goal:
            return reconstruct_path(parent, goal), [cost[state] for state in reconstruct_path(parent, goal)]

        explored.add(current)
        # Add neighbors in the order they appear in live_traffic
        for neighbor, travel_time in live_traffic.get(current, []):
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
                parent[neighbor] = current
                cost[neighbor] = cost[current] + travel_time
    return None

# DFS Algorithm
def dfs(start, goal, live_traffic):
    frontier = [start]
    parent = {start: None}
    cost = {start: 0}
    explored = set()

    while frontier:
        current = frontier.pop()
        if current == goal:
            return reconstruct_path(parent, goal), [cost[state] for state in reconstruct_path(parent, goal)]

        explored.add(current)
        # Add neighbors in the order they appear in live_traffic
        for neighbor, travel_time in live_traffic.get(current, []):
            if neighbor not in explored:
                frontier.append(neighbor)
                parent[neighbor] = current
                cost[neighbor] = cost[current] + travel_time
    return None

# UCS Algorithm
def ucs(start, goal, live_traffic):
    counter = count()  # Tie-breaking counter
    pq = [(0, next(counter), start, [start])]  # (cost, counter, state, path)
    cost = {start: 0}
    parent = {start: None}

    while pq:
        current_cost, _, current, path = heapq.heappop(pq)

        if current == goal:
            return path, [cost[state] for state in path]

        for neighbor, travel_time in live_traffic.get(current, []):
            new_cost = current_cost + travel_time
            # If a cheaper or first-time path to the neighbor is found
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, next(counter), neighbor, path + [neighbor]))

    return None

# A* Algorithm
def a_star(start, goal, live_traffic, sunday_traffic):
    counter = count()  # Tie-breaking counter
    pq = [(sunday_traffic[start], 0, next(counter), start, [start])]  # (f(n), g(n), counter, state, path)
    cost = {start: 0}
    parent = {start: None}

    while pq:
        estimated_total_cost, current_cost, _, current, path = heapq.heappop(pq)

        if current == goal:
            return path, [cost[state] for state in path]

        for neighbor, travel_time in live_traffic.get(current, []):
            new_cost = current_cost + travel_time
            heuristic = new_cost + sunday_traffic[neighbor]
            # If this is a cheaper path to the neighbor or the first time we reach it
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic, new_cost, next(counter), neighbor, path + [neighbor]))

    return None

# Main Function
if __name__ == "__main__":
    try:
        algo, start, goal, live_traffic, sunday_traffic = read_input()

        if algo == "BFS":
            path, costs = bfs(start, goal, live_traffic)
        elif algo == "DFS":
            path, costs = dfs(start, goal, live_traffic)
        elif algo == "UCS":
            path, costs = ucs(start, goal, live_traffic)
        elif algo == "A*":
            path, costs = a_star(start, goal, live_traffic, sunday_traffic)
        else:
            print("Invalid algorithm. Please choose from: BFS, DFS, UCS, A*.")

        if path:
            write_output(path, costs)
        else:
            print("No path found.")
    except Exception as e:
        print(f"Error: {e}")
