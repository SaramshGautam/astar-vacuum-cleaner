import heapq
import itertools

# Define the initial state
initial_state = {
    "grid": (             # 1 means dirty at position (1,5)
        (0, 0, 0, 0, 0),  
        (0, 0, 0, 0, 0),  
        (0, 0, 0, 0, 0),  
        (0, 0, 0, 0, 0),  
        (1, 1, 1, 1, 1)   # Dirty at position (x,5), all squares in row 5
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

# Cost function matches optimal code
def cost_function(state, action, next_state):
    remaining_dirty = sum(sum(square for square in row) for row in next_state['grid'])
    return 1 + 2 * remaining_dirty

# Heuristic function h1 (matches optimal code)
def h1(state):
    agent_pos = state['position']
    dirty_squares = [(i + 1, j + 1) for i in range(5) for j in range(5) if state['grid'][i][j] == 1]

    if not dirty_squares:
        return 0
    nearest_dirty_dist = min(abs(agent_pos[0] - d[0]) + abs(agent_pos[1] - d[1]) for d in dirty_squares)
    num_dirty = len(dirty_squares)
    
    return nearest_dirty_dist + 2 * num_dirty - 1

# Helper function to create a hashable state representation
def state_to_tuple(state):
    """ Convert state to a hashable tuple (position, grid) """
    return (state['position'], state['grid'])

# A* algorithm that follows the optimal code's logic but retains current format
def astar(initial_state, heuristic):
    # Counter to ensure unique entries in heapq
    counter = itertools.count()
    
    frontier = []
    # Initialize Node0 (initial state) with g(n) = 0, h(n) calculated using heuristic, and f(n) = g(n) + h(n)
    g_value_initial = 0  # g(n) for Node0 is 0
    h_value_initial = heuristic(initial_state)
    f_value_initial = g_value_initial + h_value_initial
    heapq.heappush(frontier, (f_value_initial, next(counter), initial_state, [], g_value_initial, f_value_initial, h_value_initial))

    explored = set()
    num_expanded = 0
    node_index = 0  # Keep track of node index

    while frontier:
        f, _, state, path, g, f_value, h_value = heapq.heappop(frontier)

        # Print the node details
        print(f"Node {node_index}: State = {state}, g(n) = {g}, h(n) = {h_value}, f(n) = {f_value}, Actions = {path}")
        node_index += 1

        # Goal test
        if goal_test(state):
            print(f"Optimal Path: {path}")
            print(f"Total nodes expanded: {num_expanded}")
            return path

        state_tuple = state_to_tuple(state)  # Create a hashable version of the state
        if state_tuple not in explored:
            explored.add(state_tuple)
            num_expanded += 1

            for action in actions:
                next_state = get_successor(state, action)
                next_state_tuple = state_to_tuple(next_state)

                if next_state_tuple not in explored:
                    remaining_dirty = sum(sum(square for square in row) for row in next_state['grid'])

                    # Update g(n) based on the formula g(n) = prev g(n) + (1 + 2 * remaining dirty)
                    next_g_value = g + (1 + 2 * remaining_dirty)
                    
                    # Calculate h(n) using the heuristic function
                    h_value_next = heuristic(next_state)
                    
                    # Calculate f(n) as f(n) = g(n) + h(n)
                    next_f_value = next_g_value + h_value_next

                    # Push the tuple (f(n), counter, next_state, path, g, next_f_value, heuristic_value)
                    heapq.heappush(frontier, (next_f_value, next(counter), next_state, path + [action], next_g_value, next_f_value, h_value_next))

    return None

if __name__ == "__main__":
    print("Running A* with h1 (Admissible Heuristic):")
    solution_h1 = astar(initial_state, h1)
