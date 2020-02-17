#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems


def sokoban_goal_state(state):
    '''
  @return: Whether all boxes are stored.
  '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    sum = 0
    for box in state.boxes:
        min_distance = float("inf")
        for position in state.storage:
            distance = calculate_manhattan_distance(box, position)
            if distance < min_distance:
                min_distance = distance
        sum += min_distance
    return sum


def calculate_manhattan_distance(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def last_move_box(new_box_positions, parent_box_positions):
    """
    return the new position of moved box by parent state
    if no box is moved, return None
    """
    for box in new_box_positions:
        if box not in parent_box_positions:
            return box
    return None


_X = 0
_Y = 1


def check_box_status(box_position, width, height, obstacles_position_list, storage_list, box_list, direction, possible_box):
    """
    return 0, 0 if the box is at the first row (boundary)
           0, height-1 if the box is at the last row (boundary)
           1, 0 if the box is at the first column (boundary)
           1, width-1 if the box is at the last column (boundary)
           -1 if the box is stuck at corner/obstacle
    return None if box is not at any boundary or stuck
    """
    box_x = box_position[0]
    box_y = box_position[1]
    up = (box_x, box_y - 1)
    down = (box_x, box_y + 1)
    left = (box_x - 1, box_y)
    right = (box_x + 1, box_y)

    if box_position not in storage_list:
        # Check if the box is stuck by boundary and obstacles
        if box_x == 0:
            if box_y != 0 and box_y != height - 1 \
                and (0, box_y - 1) not in obstacles_position_list\
                and (0, box_y - 1) not in box_list \
                    and (0, box_y + 1) not in obstacles_position_list \
                    and (0, box_y + 1) not in box_list:
                return _X, 0
            else:
                # print("stuck by b and o or b and b" + " box is " + str(box_position) + "obstacles" + str(obstacles_position_list) + "000000")
                return -1, -1
        elif box_x == (width - 1):
            if box_y != 0 and box_y != height - 1 \
                and (width - 1, box_y - 1) not in obstacles_position_list \
                and (width - 1, box_y - 1) not in box_list \
                    and (width - 1, box_y + 1) not in obstacles_position_list \
                    and (width - 1, box_y + 1) not in box_list:
                return _X, width - 1
            else:
                # print("stuck by b and o or b and b" + " box is " + str(box_position) + "obstacles" + str(obstacles_position_list) + "111111")
                return -1, -1
        elif box_y == 0:
            if (box_x - 1, 0) not in obstacles_position_list \
                and (box_x - 1, 0) not in box_list \
                    and (box_x + 1, 0) not in obstacles_position_list\
                    and (box_x + 1, 0) not in box_list:
                return _Y, 0
            else:
                # print("stuck by b and b"+ " box is " + str(box_position) + "obstacles" + str(obstacles_position_list) + "222222")
                return -1, -1
        elif box_y == (height - 1):
            if (box_x - 1, height - 1) not in obstacles_position_list \
                and (box_x - 1, height - 1) not in box_list \
                    and (box_x + 1, height - 1) not in obstacles_position_list\
                    and (box_x + 1, height - 1) not in box_list:
                return _Y, height - 1
            else:
                # print("stuck by b and o or b and b"+ " box is " + str(box_position) + "obstacles" + str(obstacles_position_list) + "333333")
                return -1, -1
        # Check if the box is stuck by obstacles only
        elif (up in obstacles_position_list and left in obstacles_position_list) \
                or (up in obstacles_position_list and right in obstacles_position_list)\
                or (down in obstacles_position_list and left in obstacles_position_list)\
                or (down in obstacles_position_list and right in obstacles_position_list):
            # print("stuck by obstacles" + " box is " + str(box_position) + "obstacles" + str(obstacles_position_list) + "444444")
            return -1, -1
    else:
        if box_x == 0:
            if (0, box_y - 1) not in possible_box and (0, box_y + 1) not in possible_box:
                if box_y != 0 and box_y != height - 1:
                    return _X, 0
                else:
                    if direction == "up":
                        return _Y, 0
                    elif direction == "down":
                        return _Y, height - 1
                    elif direction == "left":
                        return _X, 0
            else:
                return -1, -1
        elif box_x == (width - 1):
            if (width - 1, box_y - 1) not in possible_box and (width - 1, box_y + 1) not in possible_box:
                if box_y != 0 and box_y != height - 1:
                    return _X, width - 1
                else:
                    if direction == "up":
                        return _Y, 0
                    elif direction == "down":
                        return _Y, height - 1
                    elif direction == "right":
                        return _X, width - 1
            else:
                return -1, -1
        elif box_y == 0:
            if (box_x - 1, 0) not in possible_box and (box_x + 1, 0) not in possible_box:
                return _Y, 0
            else:
                return -1, -1
        elif box_y == (height - 1):
            if (box_x - 1, height - 1) not in possible_box and (box_x + 1, height - 1) not in possible_box:
                return _Y, height - 1
            else:
                return -1, -1
    return None, None


def storage_obstacle_on_same_boundary(boundary_direction, boundary, storage_position_list, obstacles_position_list, possible_box):
    possible_storage = set()
    possible_obstacles = set()
    possible_boxes = set()
    if boundary_direction == _X:
        for storage in storage_position_list:
            if storage[0] == boundary:
                possible_storage.add(storage)
        for obstacle in obstacles_position_list:
            if obstacle[0] == boundary:
                possible_obstacles.add(obstacle)
        for box in possible_box:
            if box[0] == boundary:
                possible_boxes.add(box)
    else:
        for storage in storage_position_list:
            if storage[1] == boundary:
                possible_storage.add(storage)
        for obstacle in obstacles_position_list:
            if obstacle[1] == boundary:
                possible_obstacles.add(obstacle)
        for box in possible_box:
            if box[1] == boundary:
                possible_boxes.add(box)
    return possible_storage, possible_obstacles, possible_boxes


def boundary_deadlock(width, height, box_position, storage_position_list, obstacles_position_list, possible_storage, box_list, possible_box, direction):
    boundary_direction, boundary = check_box_status(box_position, width, height, obstacles_position_list, storage_position_list, box_list, direction, possible_box)
    free_box = box_position in possible_box
    # Check if the box is at corner
    if boundary_direction == -1:
        return True
    elif boundary_direction is not None:
        storages, obstacles, boxes = \
            storage_obstacle_on_same_boundary(boundary_direction, boundary, possible_storage,
                                              obstacles_position_list, possible_box)
        if free_box and len(storages) == 0:
            return True
        elif len(boxes) > len(storages):
            return True
        elif len(boxes) == 0:
            return False
        else:
            for obstacle in obstacles:
                possible = []
                if obstacle > box_position:
                    for storage in storages:
                        possible.append(box_position < storage < obstacle)
                        if not any(possible):
                            # print("can't achieve and boundary")
                            return True
                else:
                    for storage in storages:
                        possible.append(obstacle < storage < box_position)
                        if not any(possible):
                            # print("can't achieve and boundary")
                            return True
            return False
    return False


def robot_distance(robots, possible_box, num_possible_boxes):
    result = []
    for bot in robots:
        for box in possible_box:
            distance = calculate_manhattan_distance(box, bot) - 1
            result.append(distance)
    result.sort()
    # print("bot distance", result)
    return sum(result[:num_possible_boxes])


def cal_distance(possible_box, possible_storage):
    # possible_box, possible_storage = get_free_box_and_storage(state)
    sum = 0
    for box in possible_box:
        min_distance = float("inf")
        for position in possible_storage:
            d = calculate_manhattan_distance(box, position)
            if d < min_distance:
                min_distance = d
        sum += min_distance
    return sum


def get_free_box_and_storage(storage_list, box_list):
    possible_box = []
    possible_storage = list(storage_list.copy())
    for box in box_list:
        if box in storage_list:
            possible_storage.remove(box)
        else:
            possible_box.append(box)
    return possible_box, possible_storage


def get_up(box: tuple): return tuple([box[0], box[1] - 1])


def get_down(box: tuple): return tuple([box[0], box[1] + 1])


def get_left(box: tuple): return tuple([box[0] - 1, box[1]])


def get_right(box: tuple): return tuple([box[0] + 1, box[1]])


def is_at_boundary(box, width, height):
    return box[0] == 0 or box[1] == 0 or box[0] == height - 1 or box[1] == width - 1


def no_bot_left_right(box, bots): return get_left(box) in bots and get_right(box) in bots


def no_bot_up_down(box, bots): return get_up(box) in bots and get_right(box) in bots


def get_robot_on_storage_punish(bots, storage, box, boxes):
    if box not in storage:
        if len(storage) <= len(boxes) or len(storage) <= len(bots):
            if any([i in storage for i in bots]):
                return 1
    return 0


def complicate_distance(possible_box, possible_storage):
    num_storage = len(possible_storage)
    num_box = len(possible_box)
    result = []
    for box in possible_box:
        possible_distance = []
        for position in possible_storage:
            d = calculate_manhattan_distance(box, position)
            possible_distance.append(d)
        result.append(possible_distance)
    if num_storage == 2 and num_box == 2:
        return min(result[0][0] + result [1][1], result [0][1] + result[1][0])
    elif num_storage == 2 and num_box == 1:
        return min(result[0])
    elif num_storage == 1 and num_box == 2:
        return min(result)[0]
    else:
        return min(result[0])


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.


    possible_box, possible_storage = get_free_box_and_storage(state.storage, state.boxes)
    len_possible_box = len(possible_box)
    len_possible_storage = len(possible_storage)
    direction = state.action.split()[-1]

    simple_distance = cal_distance(possible_box, possible_storage) + robot_distance(state.robots, possible_box, len_possible_box)
    # distance = cal_distance(possible_box, possible_storage) \
    #     if len_possible_storage <= 2 and len_possible_box <= 2 else complicate_distance(possible_box, possible_storage)
    if state.parent is not None:
        box = last_move_box(state.boxes, state.parent.boxes)
        if box is not None:
            cost = 0
            if boundary_deadlock(state.width, state.height, box, state.storage, state.obstacles, possible_storage, state.boxes, possible_box, direction):
                return float("inf")
            robot_on_storage_punish = get_robot_on_storage_punish(state.robots, state.storage, box, state.boxes)
            cost += robot_on_storage_punish
            # if direction == "up":
            #     if (get_up(box) in state.obstacles or get_up(box) in state.boxes or box[0] == 0 or get_up(box) in state.robots) \
            #             and no_bot_left_right(box, state.robots):
            #         cost += 2
            # elif direction == "down":
            #     if (get_down(box) in state.obstacles or get_down(box) in state.boxes or box[0] == state.height - 1 or get_down(box) in state.robots)\
            #             and no_bot_left_right(box, state.robots):
            #         cost += 2
            # elif direction == 'left':
            #     if (get_left(box) in state.obstacles or get_left(box) in state.boxes or box[1] == 0 or get_left(box) in state.robots) \
            #             and no_bot_up_down(box, state.robots):
            #         cost += 2
            # elif direction == 'right':
            #     if (get_right(box) in state.obstacles or get_right(box) in state.boxes or box[1] == state.width - 1 or get_right(box) in state.robots) \
            #             and no_bot_up_down(box, state.robots):
            #         cost += 2
            # print("cal_distance is ", cal_distance(possible_box, possible_storage), "cost", cost, "robot_distance", robot_distance(state.robots, possible_box, len_possible_box), "robots", state.robots, "boxes", state.boxes)

            return cal_distance(possible_box, possible_storage) + cost + robot_distance(state.robots, possible_box, len_possible_box)
        return simple_distance
    return simple_distance


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=2., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    # Set up
    start_time = os.times()[0]
    se = SearchEngine(strategy='custom', cc_level='full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn, fval_function=lambda sN: fval_function(sN, weight))

    # First try
    result = se.search(timebound=timebound, costbound=None)
    if not result:
        return False
    else:
        cost = result.gval + heur_fn(result)

    weight = 1.
    # Find better solution
    while timebound - (os.times()[0] - start_time) > 0 and not se.open.empty():
        weight *= 0.5
        se.fval_function = lambda sN: fval_function(sN, weight)
        better_result = se.search(timebound=timebound - (os.times()[0] - start_time), costbound=(float("inf"), float("inf"), cost))
        if better_result:
            cost = better_result.gval + heur_fn(better_result)
            result = better_result
        else:
            return result

    return result


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    """
    Provides an implementation of anytime greedy best-first search, as described in the HW1 handout
    INPUT: a sokoban state that represents the start state and a timebound (number of seconds)
    OUTPUT: A goal state (if a goal is found), else False
    implementation of weighted astar algorithm
    """
    # Set up
    start_time = os.times()[0]
    se = SearchEngine(strategy='best_first', cc_level='full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)

    # First try
    result = se.search(timebound=timebound, costbound=None)
    if not result:
        return False
    else:
        cost = result.gval

    # Find better solution
    while timebound - (os.times()[0] - start_time) > 0 and not se.open.empty():
        better_result = se.search(timebound=timebound - (os.times()[0] - start_time), costbound=(cost, float("inf"), float("inf")))
        if better_result:
            cost = better_result.gval
            result = better_result
        else:
            return result

    return result

# print(boundary_deadlock(6, 6, tuple([5, 0]), frozenset({(0, 1), (5, 4), (0, 5), (5, 0), (0, 3), (5, 2)}), frozenset({}), frozenset({(0, 1), (5, 2)}), frozenset({(2, 0), (5, 4), (0, 5), (5, 0), (4, 2), (0, 3)}), frozenset({(2, 0), (4, 2)}), "up"))
# storage = frozenset({(0, 0), (4, 0), (4, 4), (0, 4)})
# boxes = frozenset({(0, 3), (0, 0), (3, 1), (4, 3)})
# robots = ((0, 1), (1, 3))
# possible_box, possible_storage = get_free_box_and_storage(storage, boxes)
# len_possible_box = len(possible_box)
# print("cal_distance is ", cal_distance(possible_box, possible_storage),  "robot_distance", robot_distance(robots, possible_box, len_possible_box), "robots", robots, "boxes", boxes)