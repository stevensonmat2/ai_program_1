import copy
from math import sqrt


class Node:
    def __init__(
        self, state, blank, goal_state, level=0, parent=None, direction=None
    ) -> None:
        self.state = state
        self.state_value = self.write_state_value()
        self.blank = blank
        self.goal_state = goal_state
        self.children = []
        self.level = level
        self.mismatched_tiles = self.calculate_mismatched_tiles()
        self.manhattan_distance = self.calculate_manhattan_distance()
        self.combo = self.mismatched_tiles + self.manhattan_distance
        self.parent = parent
        self.direction = direction
        self.a_star = self.level
        self.bf = 0

    def calculate_mismatched_tiles(self):
        mismatches = 0
        for i, number in enumerate(self.state_value):
            if number != self.goal_state[i]:
                mismatches += 1

        return mismatches

    def write_state_value(self):
        state = ""
        for row in self.state:
            for number in row:
                state += str(number)
        return state

    def calculate_child_states(self):
        neighbors = {"up": [1, 0], "left": [0, 1], "down": [-1, 0], "right": [0, -1]}
        xb = self.blank[0]
        yb = self.blank[1]
        state_len = len(self.state_value)
        root = int(sqrt(state_len))

        for key, neighbor in neighbors.items():
            child = copy.deepcopy(self.state)
            x = xb + neighbor[0]
            y = yb + neighbor[1]

            if ((root-1) < x or x < 0) or ((root-1) < y or y < 0):
                pass
            else:
                child[xb][yb] = child[x][y]
                child[x][y] = 0
                self.children.append(
                    Node(child, [x, y], self.goal_state, self.level + 1, self, key)
                )

    def calculate_manhattan_distance(self):
        goal_state_coordinates = [
            (0, 0),
            (1, 0),
            (2, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (0, 2),
            (1, 2),
            (2, 2),
        ]
        sum = 0
        for number in self.state_value:
            num = int(number)
            for y, row in enumerate(self.state):
                try:
                    x = row.index(num)
                    sum += abs(
                        (x - goal_state_coordinates[num - 1][0])
                        + abs(y - goal_state_coordinates[num - 1][1])
                    )
                except:
                    pass
        return sum


    def display_board(self):

        print(f"{self.state_value}, {self.direction}, ", end="")

    def display_path(self):
        path = []
        parent = self
        while parent:
            path.insert(0, parent)
            parent = parent.parent

        for node in path:
            node.display_board()
        print("\n")


class Board:
    def __init__(self) -> None:
        self.blank_index = []
        self.board = None
        self.goal_state_value = None
        self.root = None
        self.priority_queue = []
        self.visited = {}

    def parity_is_matched(self):
        state = ""
        inversions = 0
        goal_inversions = 0
        for row in self.board:
            state = state + "".join(map(str, row))

        for number in state:
            for other_num in number:
                if number > other_num:
                    inversions += 1

        if (inversions * goal_inversions) % 2 == 0:
            return True
        return False

    def build_board(self, input, goal_state, size):
        state_copy = copy.deepcopy(input)
        output = []
        root = int(sqrt(size))
        row = 0
        while row < root:
            output.append(state_copy[0:root])
            state_copy = state_copy[root::]

            try:
                self.blank_index = [row, output[-1].index(0)]
            except:
                pass
            row += 1

        self.priority_queue = []
        self.visited = {}
        self.goal_state_value = "".join(map(str, goal_state))
        self.board = output
        self.root = Node(self.board, self.blank_index, self.goal_state_value)

    def display_board(self):
        for row in self.board:
            print(row)

        print(self.blank_index)

    def reach_goal(self, search_type, heuristic):
        limit = 300000
        iterations = 0
        node = self.root

        if self.parity_is_matched():

            while iterations < limit:
                iterations += 1
                if node.state_value == self.goal_state_value:
                    print(
                        f"search: {search_type}, heuristic: {heuristic}, steps: {node.level}, expansions: {iterations}"
                    )
                    node.display_path()
                    self.iterations = iterations
                    return node.level

                key = node.state_value + str(getattr(node, search_type))
                if not key in self.visited:
                    self.visited[key] = node
                    node.calculate_child_states()
                    self.priority_queue.extend(node.children)
                    self.priority_queue.sort(
                        key=lambda x: getattr(x, heuristic) + getattr(x, search_type)
                    )

                node = self.priority_queue.pop(0)

        return 0

    def solve(self, states, goal_state):
        search_types = ["bf", "a_star"]
        heuristics = ["mismatched_tiles", "manhattan_distance", "combo"]

        for search_type in search_types:
            for heuristic in heuristics:
                step_sum = 0
                iteration_sum = 0
                for state in states:
                    self.build_board(state, goal_state, len(state))
                    step_sum += self.reach_goal(search_type, heuristic)
                    iteration_sum += self.iterations
                step_average = step_sum / len(states)
                iteration_average = iteration_sum / len(states)
                print(
                    f"average number of steps: {step_average}, average number of expansions: {iteration_average}"
                )
                print("------------------")
                print("\n")


states = [
    [1, 2, 3, 7, 5, 0, 6, 8, 4],
    [2, 0, 3, 1, 8, 5, 4, 7, 6],
    [7, 2, 5, 0, 1, 4, 6, 3, 8],
    [5, 7, 0, 2, 1, 3, 8, 4, 6],
    [8, 7, 4, 5, 1, 3, 2, 6, 0],
]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

states_15 = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15]]
goal_state_15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


board = Board()
# board.solve(states_15, goal_state_15)
board.solve(states, goal_state)
