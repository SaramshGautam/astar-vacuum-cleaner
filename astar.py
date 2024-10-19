import heapq
import itertools

# Define the initial state
initial_state = {
    "grid": (
        (0, 0, 0, 0, 0),  # 1 means dirty at position (1,5)
        (0, 0, 0, 0, 0),  # Dirty at position (2,5)
        (0, 0, 0, 0, 0),  # Dirty at position (3,5)
        (0, 0, 0, 0, 0),  # Dirty at position (4,5)
        (1, 1, 1, 1, 1)   # Dirty at position (5,5)
    ),
    "position": (1, 1)  # Initial position at bottom left (1,1)
}

# Define possible actions
actions = ['Up', 'Down', 'Left', 'Right', 'Suck']

# Successor function
def get_successor(state, action):
    new_grid = list(map(list, state['grid']))
    x, y = state['position']
    
    if action == 'Suck':
        new_grid[x - 1][y - 1] = 0  # Clean the square
    elif action == 'Up' and x < 5:
        x += 1
    elif action == 'Down' and x > 1:
        x -= 1
    elif action == 'Left' and y > 1:
        y -= 1
    elif action == 'Right' and y < 5:
        y += 1

    return {
        "grid": tuple(map(tuple, new_grid)),  # Convert back to tuples for immutability
        "position": (x, y)
    }

# Goal test function
def goal_test(state):
    return all(all(square == 0 for square in row) for row in state['grid'])

# Cost function
def cost_function(state, action, next_state):
    num_dirty = sum(sum(square for square in row) for row in next_state['grid'])
    return 1 + 2 * num_dirty

# Heuristic function h1 (Admissible)
def h1(state):
    x, y = state['position']
    min_distance = float('inf')  # Set to a large initial value
    num_dirty = 0
    
    for i in range(5):
        for j in range(5):
            if state['grid'][i][j] == 1:
                num_dirty += 1
                distance = abs((i + 1) - x) + abs((j + 1) - y)
                min_distance = min(min_distance, distance)
    
    # If no dirty squares remain, min_distance will stay inf; fix by returning 0 in that case.
    if num_dirty == 0:
        return 0
    
    # Otherwise, return the estimated cost to clean all dirty squares.
    return min_distance + 2 * num_dirty - 1

# Heuristic function h2 (Dominating h1)
def h2(state):
    x, y = state['position']
    min_distance = float('inf')
    num_dirty = 0
    
    for i in range(5):
        for j in range(5):
            if state['grid'][i][j] == 1:
                num_dirty += 1
                distance = abs((i + 1) - x) + abs((j + 1) - y)
                min_distance = min(min_distance, distance)
    
    # If no dirty squares remain, avoid returning inf by checking the condition
    if num_dirty == 0:
        return 0
    
    # Penalty for leaving squares dirty
    t2_penalty = 2 * num_dirty * min_distance + 2 * num_dirty * (num_dirty - 1)
    
    return h1(state) + t2_penalty

# Helper function to create a hashable state representation
def state_to_tuple(state):
    """ Convert state to a hashable tuple (position, grid) """
    return (state['position'], state['grid'])

# A* algorithm with tracking of f(n) values for all nodes in the optimal path
def astar(initial_state, heuristic):
    # Counter to ensure unique entries in heapq
    counter = itertools.count()
    
    frontier = []
    # Instead of storing the whole state directly, we store f(n) first for comparison
    heapq.heappush(frontier, (0, next(counter), initial_state, [], 0, 0))  # (f(n), counter, state, actions, cost, f_value)
    explored = set()
    num_expanded = 0
    f_values_on_path = []  # Track f(n) values for the optimal path
    states_on_path = []  # Track states on the optimal path
    actions_on_path = [] # Track actions leading to each node in the optimal path
    
    while frontier:
        f, _, state, path, g, f_value = heapq.heappop(frontier)  # g is the current cost (path cost)
        
        if goal_test(state):
            f_values_on_path.append(f_value)
            states_on_path.append(state)
            actions_on_path.append(path)
            print("Solution Path:", path)
            print("Node states, f(n) values, and actions leading to each node in the optimal path (including initial and final states):")
            for i, (fn_value, node_state, actions_taken) in enumerate(zip(f_values_on_path, states_on_path, actions_on_path)):
                print(f"Node {i + 1}: State = {node_state}, f(n) = {fn_value}, Actions = {actions_taken}")
            print(f"f(n) value at the final goal state: {f}")
            print(f"Number of nodes expanded: {num_expanded}")
            return path
        
        state_tuple = state_to_tuple(state)  # Create a hashable version of the state
        if state_tuple not in explored:
            explored.add(state_tuple)
            num_expanded += 1
        
            for action in actions:
                next_state = get_successor(state, action)
                next_state_tuple = state_to_tuple(next_state)
                
                if next_state_tuple not in explored:
                    new_cost = g + cost_function(state, action, next_state)
                    next_f_value = new_cost + heuristic(next_state)
                    # Push the tuple (f(n), counter, next_state, path, g, next_f_value) with f(n) = g + h(next_state)
                    heapq.heappush(frontier, (next_f_value, next(counter), next_state, path + [action], new_cost, next_f_value))
                    # Track f(n) value, state, and actions for nodes in the optimal path
                    f_values_on_path.append(next_f_value)
                    states_on_path.append(next_state)
                    actions_on_path.append(path + [action])
    
    return None

if __name__ == "__main__":
    print("Running A* with h1 (Admissible Heuristic):")
    solution_h1 = astar(initial_state, h1)
    
    print("\nRunning A* with h2 (Dominating Heuristic):")
    solution_h2 = astar(initial_state, h2)
