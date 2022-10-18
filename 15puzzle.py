import copy
from math import sqrt
import random
from re import A


class Node:
    def __init__(
        self, state, blank, goal_state, level=0, parent=None, direction=None
    ) -> None:
        self.state = state
        self.state_value = self.state_15()
        self.blank = blank
        self.goal_state = goal_state
        self.children = []
        self.level = level
        self.mismatched_tiles = self.calculate_mismatched_tiles()
        self.manhattan_distance = self.calculate_manhattan_distance()
        self.combo = max(self.mismatched_tiles, self.manhattan_distance)
        self.parent = parent
        self.direction = direction
        self.a_star = self.level
        self.bf = 0

    def state_15(self):
        state = []
        for i in self.state:
            for j in i:
                state.append(str(j))
        
        return state


    def calculate_mismatched_tiles(self):
        mismatches = 0
        for i, number in enumerate(self.state_value):
            if number != str(self.goal_state[i]):
                mismatches += 1

        return mismatches

    def write_state_value(self):
        if len(self.state) > 3:
            return self.state_15()
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
        goal_state_coordinates = {
            0: (0, 0),
            1: (1, 0),
            2: (2, 0),
            3: (3, 0),
            4: (0, 1),
            5: (1, 1),
            6: (2, 1),
            7: (3, 1),
            8: (0, 2),
            9: (1, 2),
            10: (2, 2),
            11: (3, 2),
            12: (0, 3),
            13: (1, 3),
            14: (2, 3),
            15: (3, 3),
        }
        sum = 0
        for index, number in enumerate(self.goal_state):
            current_number = int(self.state_value[index])
            if current_number != int(number):
                current_square = goal_state_coordinates[index]
                desired_square = goal_state_coordinates[max(current_number-1, 0)]
                sum += abs(current_square[0] - desired_square[0]) + abs(current_square[1] - desired_square[1])
        
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
        self.root = Node(self.board, self.blank_index, goal_state)


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
                if "".join(node.state_value) == self.goal_state_value:
                    print(
                        f"search: {search_type}, heuristic: {heuristic}, steps: {node.level}, expansions: {iterations}"
                    )
                    # node.display_path()
                    self.iterations = iterations
                    return node.level

                key = "".join(node.state_value) + str(getattr(node, search_type))
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


states_15 = [
# [0, 1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
# [2, 0, 3, 4, 1, 6, 7, 8, 5, 10, 11, 12, 9, 13, 14, 15],
# [1, 2, 0, 4, 5, 6, 3, 8, 9, 10, 7, 12, 13, 14, 11, 15],
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 10, 14, 15],
# [1, 2, 3, 4, 5, 6, 0, 8, 9, 11, 7, 12, 13, 10, 14, 15]
[5, 2, 11, 3, 7, 1, 15, 4, 9, 13, 8, 0, 14, 6, 10, 12],
[5, 2, 11, 3, 7, 1, 15, 4, 9, 13, 0, 8, 14, 6, 10, 12],
[5, 2, 11, 3, 7, 1, 0, 4, 9, 13, 15, 8, 14, 6, 10, 12],
[5, 2, 0, 3, 7, 1, 11, 4, 9, 13, 15, 8, 14, 6, 10, 12],
[5, 1, 2, 3, 7, 0, 11, 4, 9, 13, 15, 8, 14, 6, 10, 12]
]

goal_state_15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


board = Board()
board.solve(states_15, goal_state_15)
