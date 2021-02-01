'''
Problem formulation:
Initial State: 
    number of marbles = 44
    layout = [[9, 9, 1, 1, 1, 9, 9],
              [9, 9, 1, 1, 1, 9, 9],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 0, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [9, 9, 1, 1, 1, 9, 9],
              [9, 9, 1, 1, 1, 9, 9]])
Goal Test: number of marbles = 1
'''
import copy

class State:
    def __init__(self, layoutIn, parentIn=None):
        self.layout = layoutIn
        self.parent = parentIn
        self.evaluation_function = calculate_maximum_manhattan_distance(create_locations_list(layoutIn)) + corner_count(layoutIn)

def corner_count(layoutIn):
    locations = [[2, 0], [4, 0], [0, 2], [0, 4], [6, 2], [6, 4], [2, 6], [4, 6], [3, 0], [0, 3], [6, 3], [3, 6]]
    counter = 0
    for location in locations:
        x = location[0]
        y = location[1]
        if layoutIn[x][y] == 1:
            counter += 1
    return counter

def inner_count(layoutIn):
    locations = [[2, 1], [4, 1], [1, 2], [1, 4], [5, 2], [5, 4], [2, 5], [4, 5]]#, [3, 1], [1, 3], [5, 3], [5, 6]]
    counter = 0
    for location in locations:
        x = location[0]
        y = location[1]
        if layoutIn[x][y] == 1:
            counter += 0.1
    return counter

def calculate_chain_count(layoutIn):
    chain_count = 0
    for x in range(len(layoutIn) - 2):
        for y in range(len(layoutIn[0])):
            if ((layoutIn[x][y] == 1) and (layoutIn[x+1][y] == 0) and (layoutIn[x+2][y] == 1)):
                chain_count += 1
    return chain_count

def create_locations_list(layoutIn):
    locations = []
    for x in range(len(layoutIn)):
        for y in range((len(layoutIn[0]))):
            if layoutIn[x][y] == 1:
                locations.append([x, y])
    return locations

def calculate_average_manhattan_distance(listIn):
    distances = []
    for a in range(len(listIn)):
        for b in range(len(listIn) - a):
            distances.append(calculate_manhattan_distance(listIn[a], listIn[b]))
    return sum(distances) / len(distances)

def calculate_maximum_manhattan_distance(listIn):
    distances = []
    for a in range(len(listIn)):
        for b in range(len(listIn) - a):
            distances.append(calculate_manhattan_distance(listIn[a], listIn[b]))
    return max(distances)

def calculate_manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] + loc2[1])

def get_initial_state():
    return State([[9, 9, 1, 1, 1, 9, 9],
                  [9, 9, 1, 1, 1, 9, 9],
                  [1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 0, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1],
                  [9, 9, 1, 1, 1, 9, 9],
                  [9, 9, 1, 1, 1, 9, 9]])

def get_initial_state1():
    return State([[9, 9, 1, 1, 1, 9, 9],
                  [9, 1, 1, 1, 1, 1, 9],
                  [1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 0, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1],
                  [9, 1, 1, 1, 1, 1, 9],
                  [9, 9, 1, 1, 1, 9, 9]])

def goal_test(stateIn):
    total_sum = []
    for row in stateIn.layout:
        total_sum.append(row.count(1))
    num_marbles = sum(total_sum)
    if num_marbles == 1:
        return True
    return False

def expand(stateIn, frontierIn, counter, visited):
    for x in range(len(stateIn.layout) - 2):
        for y in range(len(stateIn.layout[0])):

            if ((stateIn.layout[x][y] == 1) and (stateIn.layout[x+1][y] == 1) and (stateIn.layout[x+2][y] == 0)):
                new_layout = copy.deepcopy(stateIn.layout)
                new_layout[x][y] = 0
                new_layout[x+1][y] = 0
                new_layout[x+2][y] = 1
                new_state = State(new_layout, stateIn)

                if goal_test(new_state):
                    return new_state

                total_sum = []
                for row in new_state.layout:
                    total_sum.append(row.count(1))
                num_marbles = sum(total_sum)
                
                if num_marbles not in counter:
                    counter.append(num_marbles)
                    print(num_marbles)

                if new_state.layout not in visited:
                    frontierIn.append(new_state)
                    visited.append(new_state.layout)

            if ((stateIn.layout[x][y] == 0) and (stateIn.layout[x+1][y] == 1) and (stateIn.layout[x+2][y] == 1)):
                new_layout = copy.deepcopy(stateIn.layout)
                new_layout[x][y] = 1
                new_layout[x+1][y] = 0
                new_layout[x+2][y] = 0
                new_state = State(new_layout, stateIn)

                if goal_test(new_state):
                    return new_state
                total_sum = []
                
                for row in new_state.layout:
                    total_sum.append(row.count(1))
                num_marbles = sum(total_sum)
                
                if num_marbles not in counter:
                    counter.append(num_marbles)
                    print(num_marbles)

                if new_state.layout not in visited:
                    frontierIn.append(new_state)
                    visited.append(new_state.layout)

    for x in range(len(stateIn.layout)):
        for y in range(len(stateIn.layout[0]) - 2):

            if ((stateIn.layout[x][y] == 1) and (stateIn.layout[x][y+1] == 1) and (stateIn.layout[x][y+2] == 0)):
                new_layout = copy.deepcopy(stateIn.layout)
                new_layout[x][y] = 0
                new_layout[x][y+1] = 0
                new_layout[x][y+2] = 1
                new_state = State(new_layout, stateIn)

                if goal_test(new_state):
                    return new_state

                total_sum = []
                for row in new_state.layout:
                    total_sum.append(row.count(1))
                num_marbles = sum(total_sum)
                
                if num_marbles not in counter:
                    counter.append(num_marbles)
                    print(num_marbles)

                if new_state.layout not in visited:
                    frontierIn.append(new_state)
                    visited.append(new_state.layout)

            if ((stateIn.layout[x][y] == 0) and (stateIn.layout[x][y+1] == 1) and (stateIn.layout[x][y+2] == 1)):
                new_layout = copy.deepcopy(stateIn.layout)
                new_layout[x][y] = 1
                new_layout[x][y+1] = 0
                new_layout[x][y+2] = 0
                new_state = State(new_layout, stateIn)

                if goal_test(new_state):
                    return new_state

                total_sum = []
                for row in new_state.layout:
                    total_sum.append(row.count(1))
                num_marbles = sum(total_sum)
                
                if num_marbles not in counter:
                    counter.append(num_marbles)
                    print(num_marbles)

                if new_state.layout not in visited:
                    frontierIn.append(new_state)
                    visited.append(new_state.layout)

def DFS():
    frontier = [get_initial_state()]
    counter = []
    visited = []
    while len(frontier) > 0:
        frontier.sort(reverse = True, key=lambda x: x.evaluation_function)
        state = frontier.pop()
        result = expand(state, frontier, counter, visited)
        if result:
            return result

    return "search failed"

def display_result():
    result = DFS()
    if result != "search failed":
        print()
        print("solution found")
        print()
        for row in result.layout:
            print(row)
        #print(result.layout)
        print()
        i = 0
        while result.parent != None:
            print(i)
            for row in result.parent.layout:
                print(row)
            #print(result.parent.layout)
            print()
            result = result.parent
            i += 1
    else:
        print(result)

display_result()
