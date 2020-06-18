class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # Distance b/w starting node and current node 
        self.h = 0 # Estimated distance b/w current + end node
        self.f = 0 # Total cost: f = g + h

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start(snakehead) and end node (food)
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = [] # squares being considered for finding shortest path
    closed_list = [] # squares that won't be considered for the path

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0: # open_list is emptied when reaching end node

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f: # lower f means that it's part of shortest path
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Tracks path from end node to start node
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None: # Start node initialized with parent=None
                path.append(current.position) # xy coordinates
                current = current.parent # the node that preceded current
            return path[::-1] # Return reversed path

        # Generate children aka potential moves from current node
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Loop through adjacent squares

            #new_position[0] is x, new_position[0] is y
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (height - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

# (len(maze[len(maze)-1]) -1) breakdown
# innermost_value = len(maze) - 1, get position of maze edge
# maze_position = maze[innermostvalue]

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)