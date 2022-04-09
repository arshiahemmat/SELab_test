from base import Action
from genetic_motor import define_requirment

INF = 1000000
Gems = {1: (10, 0, 15), 2: (25, 15, 8), 3: (35, 50, 5), 4: (75, 140, 4)}


class Gem:
    class_type = 'Gem'
    gem_gain_score = None
    gem_limited = None
    gem_score = None

    def __init__(self, x, y, gem_type):
        self.x = x
        self.y = y
        self.gem_type = gem_type
        self.set_gem_information()

    def set_gem_information(self):
        if self.gem_type == 1:
            self.gem_limited = 15
            self.gem_score = 10
            self.gem_gain_score = 0
        elif self.gem_type == 2:
            self.gem_limited = 8
            self.gem_score = 25
            self.gem_gain_score = 15
        elif self.gem_type == 3:
            self.gem_limited = 5
            self.gem_score = 35
            self.gem_gain_score = 50
        elif self.gem_type == 4:
            self.gem_limited = 4
            self.gem_score = 75
            self.gem_gain_score = 140

    def __str__(self):
        return self.class_type + '\tCoordinates: ' + str(self.x) + '\t' + str(self.y)


# class Trap:
#     class_type = 'Trap'
#     trap_type = False  # if False is our trap otherwise, enemy trap
#     trap_gain_score = 0

#     def __init__(self, x, y, trap_type):
#         self.x = x
#         self.y = y
#         self.trap_type = trap_type
#         self.trap_score = 40

#     def __str__(self):
#         return self.class_type + '\tCoordinates: ' + str(self.x) + '\t' + str(self.y)


class Agent:
    def __init__(self, x, y, score, character, agent_id):
        self.x = x
        self.y = y
        self.score = score
        self.character = character
        self.agent_id = agent_id
        self.path = list()
        self.gem_reach_list = list()


class Empty:
    class_type = 'Empty'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.class_type + '\tCoordinates: ' + str(self.x) + '\t' + str(self.y)


class Wall:
    class_type = 'Wall'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.class_type + '\tCoordinates: ' + str(self.x) + '\t' + str(self.y)


class Teleport:
    class_type = 'Teleport'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.class_type + '\tCoordinates: ' + str(self.x) + '\t' + str(self.y)


class Grid:
    Node_grid = list()
    Our_agent = None
    Aim_gem = tuple()
    # Enemy_agent = None
    previous_grid = None
    # Max_trap = None
    forbidden_nodes = [(-1, -1)]
    last_move = tuple()
    score_list = list()
    Gems_list = list()
    # Trap_list = list()
    Wall_list = list()
    Teleport_list = list()
    our_gem_catch_list = [0, 0, 0, 0]
    enemy_gem_catch_list = list()
    color_grid = list()
    possible_teleports = list()

    def __init__(self, grid_information):
        self.grid = grid_information.grid
        self.height = grid_information.grid_height
        self.width = grid_information.grid_width
        self.Max_trap = grid_information.trap_count
        self.score_list.append(grid_information.score)
        self.set_agents(grid_information)
        self.reconstruct_grid(grid_information)
        self.divide_grid()
        self.last_move = (self.Our_agent.x, self.Our_agent.y)
        self.Aim_gem = (self.Our_agent.x, self.Our_agent.y)

    def add_score(self, value):
        self.score_list.append(value)

    def set_agents(self, grid_information):
        our_id = grid_information.id
        our_char = 'A'
        our_agent_location = None
        for i in range(grid_information.grid_height):
            for j in range(grid_information.grid_width):
                if our_char in self.grid[i][j]:
                    our_agent_location = (i, j)
        self.Our_agent = Agent(our_agent_location[0], our_agent_location[1], grid_information.score, our_char, our_id)

    def reconstruct_grid(self, grid_information):
        self.Gems_list.clear()
        self.Wall_list.clear()
        self.Teleport_list.clear()
        self.divide_grid()
        self.Our_agent.score = grid_information.agent_scores[self.Our_agent.agent_id - 1]
        # self.Enemy_agent.score = grid_information.agent_scores[self.Enemy_agent.agent_id - 1]
        # self.our_gem_catch_list = grid_information.agent_gems[self.Our_agent.agent_id - 1]
        # self.enemy_gem_catch_list = grid_information.agent_gems[self.Enemy_agent.agent_id - 1]
        self.grid = grid_information.grid
        raw_columns = list()

        for i in range(grid_information.grid_height):
            raw_columns.clear()
            for j in range(grid_information.grid_width):
                # if self.Our_agent.character in self.grid[i][j]:
                #     self.Our_agent.x, self.Our_agent.y = i, j
                # elif self.Enemy_agent.character in self.grid[i][j]:
                #     self.Enemy_agent.x, self.Enemy_agent.y = i, j
                if 'A' in self.grid[i][j]:
                    self.Our_agent.x, self.Our_agent.y = i, j
                if 'E' in self.grid[i][j]:
                    raw_columns.append(Empty(i, j))
                elif 'W' in self.grid[i][j]:
                    raw_columns.append(Wall(i, j))
                    self.Wall_list.append(Wall(i, j))
                elif 'T' in self.grid[i][j]:
                    raw_columns.append(Teleport(i, j))
                    self.Teleport_list.append(Teleport(i, j))
                elif '1' in self.grid[i][j]:
                    raw_columns.append(Gem(i, j, 1))
                    self.Gems_list.append(Gem(i, j, 1))
                elif '2' in self.grid[i][j]:
                    raw_columns.append(Gem(i, j, 2))
                    self.Gems_list.append(Gem(i, j, 2))
                elif '3' in self.grid[i][j]:
                    raw_columns.append(Gem(i, j, 3))
                    self.Gems_list.append(Gem(i, j, 3))
                elif '4' in self.grid[i][j]:
                    raw_columns.append(Gem(i, j, 4))
                    self.Gems_list.append(Gem(i, j, 4))
            self.Node_grid.append(raw_columns)

    def collect_gem(self, x, y):
        self.Our_agent.score += self.Node_grid[x][y].gem_score
        if self.Node_grid[x][y].class_type == 'Gem':
            self.our_gem_catch_list[self.Node_grid[x][y].gem_type - 1] += 1
            self.Node_grid[x][y] = Empty(x, y)

    def divide_grid(self):
        self.color_grid = [[0 for i in range(self.width)] for j in range(self.height)]
        frontier = [(self.Our_agent.x, self.Our_agent.y)]
        self.color_grid[self.Our_agent.x][self.Our_agent.y] = 1
        while len(frontier) != 0:
            first_node = frontier[0]
            frontier.pop(0)
            if self.grid[first_node[0]][first_node[1]] == 'W':
                continue
            x, y = first_node[0], first_node[1]
            color = self.color_grid[x][y]
            if 0 <= x - 1 < self.height and self.color_grid[x - 1][y] != 1:
                if self.grid[x - 1][y] != 'W':
                    self.color_grid[x - 1][y] = color
                    frontier.append((x - 1, y))
            if 0 <= x + 1 < self.height and self.color_grid[x + 1][y] != 1:
                if self.grid[x + 1][y] != 'W':
                    self.color_grid[x + 1][y] = color
                    frontier.append((x + 1, y))
            if 0 <= y - 1 < self.width and self.color_grid[x][y - 1] != 1:
                if self.grid[x][y - 1] != 'W':
                    self.color_grid[x][y - 1] = color
                    frontier.append((x, y - 1))
            if 0 <= y + 1 < self.width and self.color_grid[x][y + 1] != 1:
                if self.grid[x][y + 1] != 'W':
                    self.color_grid[x][y + 1] = color
                    frontier.append((x, y + 1))

    def check_possible_teleport(self):
        for each in self.Teleport_list:
            if self.color_grid[each.x][each.y] == 1:
                self.possible_teleports.append((each.x, each.y))


game_grid: Grid


def construct_gem_dictionary(grid_info: Grid) -> dict:
    gem_dictionary = dict()
    type_one = list()
    type_two = list()
    type_three = list()
    type_four = list()
    for each_gem in grid_info.Gems_list:
        if each_gem.gem_type == 1 and grid_info.our_gem_catch_list[0] < 15:
            type_one.append((each_gem.x, each_gem.y))
        elif each_gem.gem_type == 2 and grid_info.our_gem_catch_list[1] < 8 and grid_info.Our_agent.score >= 15:
            type_two.append((each_gem.x, each_gem.y))
        elif each_gem.gem_type == 3 and grid_info.our_gem_catch_list[2] < 5 and grid_info.Our_agent.score >= 50:
            type_three.append((each_gem.x, each_gem.y))
        elif each_gem.gem_type == 4 and grid_info.our_gem_catch_list[3] < 4 and grid_info.Our_agent.score >= 140:
            type_four.append((each_gem.x, each_gem.y))
    gem_dictionary[1] = (10, type_one)
    gem_dictionary[2] = (25, type_two)
    gem_dictionary[3] = (35, type_three)
    gem_dictionary[4] = (75, type_four)
    return gem_dictionary


def construct_environment(grid_info):
    global game_grid
    game_grid = Grid(grid_info)
    game_grid.Our_agent.path.append((-1, -1))
    game_grid.Our_agent.path.append((-1, -1))
    game_grid.Our_agent.path.append((game_grid.Our_agent.x, game_grid.Our_agent.y))


def can_eat_gem_for_us(grid_info, gem_type):
    if grid_info.Our_agent.score > Gems[gem_type][1] and grid_info.our_gem_catch_list[gem_type - 1] < Gems[gem_type][2]:
        return True
    return False


def manhattan(i0, j0, i1, j1):
    return abs(i0 - i1) + abs(j0 - j1)


def calculate_score_of_place():
    if game_grid.color_grid[game_grid.Our_agent.x][game_grid.Our_agent.y] != 1:
        game_grid.divide_grid()
    place_score = 0
    # print('------------------START FUNCTION-----------------------')
    # print('grid of color:')
    # for each in game_grid.color_grid:
    #     print(each)
    # for each in game_grid.Gems_list:
    #     print((each.x, each.y))
    for gem in game_grid.Gems_list:
        # print('colour grid:', game_grid.color_grid[gem.x][gem.y], gem.x, gem.y)
        if game_grid.color_grid[gem.x][gem.y] == 1:
            # print('coordinate:', gem.x, gem.y)
            if can_eat_gem_for_us(game_grid, gem.gem_type):
                place_score += gem.gem_score
    #             print('Score of gems', gem.gem_score)
    # print('place_score: ', place_score)
    # print('------------------END FUNCTION-----------------------')
    return place_score


def brain_of_code() -> str:
    place_score = calculate_score_of_place()
    flag = True

    if place_score <= 0 and len(game_grid.Teleport_list) > 0:
        return 'teleport'

    return 'gem'


def teleportize(node, enemy_location: list, teleport_location_in_list_of_tupels: list):
    dictionary = dict()
    dictionary['e'] = (-80, [enemy_location])
    dictionary['t'] = (800, teleport_location_in_list_of_tupels)
    hs = 0
    i = node[0]
    j = node[1]
    for type in dictionary.keys():
        for b in dictionary[type][1]:
            if list(b) != [i, j]:
                hs += 40 * (dictionary[type][0] / manhattan(b[0], b[1], i, j))
            else:
                hs += dictionary[type][0] * 80
    return hs


def execution_test(grid_info):
    global game_grid
    if grid_info.turn_count == 1:
        construct_environment(grid_info)
        sequence_grid = list()
    game_grid.reconstruct_grid(grid_information=grid_info)
    # check_enemy_trap()
    game_grid.add_score(game_grid.Our_agent.score)
    # for each in game_grid.Gems_list:
    #     print((each.x, each.y))
    print('Turn count:', grid_info.turn_count)
    decisions = brain_of_code()
    game_grid.last_move = (game_grid.Our_agent.x, game_grid.Our_agent.y)
    # print(decisions)
    if decisions == 'gem':
        if game_grid.Aim_gem == (game_grid.Our_agent.x, game_grid.Our_agent.y):
            if '1' in game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y] or '2' in game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y] or '3' in game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y] or '4' in game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y]:
                if can_eat_gem_for_us(game_grid, game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y][0]):
                    game_grid.our_gem_catch_list[game_grid.grid[game_grid.Our_agent.x][game_grid.Our_agent.y][0] - 1] += 1
            sequence_grid = define_requirment(game_grid.grid, game_grid.height, game_grid.width, game_grid.Our_agent.score,
                                  grid_info.turn_count)
            print('sequence_grid: ',sequence_grid)
            print('game_grid: ',game_grid.Aim_gem)
            game_grid.Aim_gem = tuple(sequence_grid[0])
        action = list()
        current_x, current_y = game_grid.Our_agent.x, game_grid.Our_agent.y
        if 0 <= current_x - 1 < game_grid.height and game_grid.grid[current_x - 1][current_y] != 'W' and (
                current_x - 1, current_y) not in game_grid.forbidden_nodes:
            each_score = heuristics((current_x - 1, current_y), game_grid.Aim_gem)
            action.append((each_score, 'UP'))
        if 0 <= current_x + 1 < game_grid.height and game_grid.grid[current_x + 1][current_y] != 'W' and (
                current_x + 1, current_y) not in game_grid.forbidden_nodes:
            each_score = heuristics((current_x + 1, current_y), game_grid.Aim_gem)
            action.append((each_score, 'DOWN'))
        if 0 <= current_y - 1 < game_grid.width and game_grid.grid[current_x][current_y - 1] != 'W' and (
                current_x, current_y - 1) not in game_grid.forbidden_nodes:
            each_score = heuristics((current_x, current_y - 1), game_grid.Aim_gem)
            action.append((each_score, 'LEFT'))
        if 0 <= current_y + 1 < game_grid.width and game_grid.grid[current_x][current_y + 1] != 'W' and (
                current_x, current_y + 1) not in game_grid.forbidden_nodes:
            each_score = heuristics((current_x, current_y + 1), game_grid.Aim_gem)
            action.append((each_score, 'RIGHT'))
        if len(action) == 0:
            return Action.NOOP
        action.sort()
        final = action[-1][1]
        # print('final action:', final)
        if final == 'UP':
            return Action.UP
        elif final == 'DOWN':
            return Action.DOWN
        elif final == 'LEFT':
            return Action.LEFT
        elif final == 'RIGHT':
            return Action.RIGHT

    elif decisions == 'teleport':

        action = list()
        current_x, current_y = game_grid.Our_agent.x, game_grid.Our_agent.y
        game_grid.check_possible_teleport()

        if 'T' in game_grid.grid[current_x][current_y]:
            return Action.TELEPORT
        if 0 <= current_x - 1 < game_grid.height and game_grid.grid[current_x - 1][current_y] != 'W' and (
                current_x - 1, current_y) not in game_grid.forbidden_nodes:
            each_score = teleportize((current_x - 1, current_y), [game_grid.Enemy_agent.x, game_grid.Enemy_agent.y],
                                     game_grid.possible_teleports)
            action.append((each_score, 'UP'))
        if 0 <= current_x + 1 < game_grid.height and game_grid.grid[current_x + 1][current_y] != 'W' and (
                current_x + 1, current_y) not in game_grid.forbidden_nodes:
            each_score = teleportize((current_x + 1, current_y), [game_grid.Enemy_agent.x, game_grid.Enemy_agent.y],
                                     game_grid.possible_teleports)
            action.append((each_score, 'DOWN'))
        if 0 <= current_y - 1 < game_grid.width and game_grid.grid[current_x][current_y - 1] != 'W' and (
                current_x, current_y - 1) not in game_grid.forbidden_nodes:
            each_score = teleportize((current_x, current_y - 1), [game_grid.Enemy_agent.x, game_grid.Enemy_agent.y],
                                     game_grid.possible_teleports)
            action.append((each_score, 'LEFT'))
        if 0 <= current_y + 1 < game_grid.width and game_grid.grid[current_x][current_y + 1] != 'W' and (
                current_x, current_y + 1) not in game_grid.forbidden_nodes:
            each_score = teleportize((current_x, current_y + 1), [game_grid.Enemy_agent.x, game_grid.Enemy_agent.y],
                                     game_grid.possible_teleports)
            action.append((each_score, 'RIGHT'))
        if len(action) == 0:
            return Action.NOOP
        action.sort()
        final = action[-1][1]
        # print('final action:', final)
        if final == 'UP':
            return Action.UP
        elif final == 'DOWN':
            return Action.DOWN
        elif final == 'LEFT':
            return Action.LEFT
        elif final == 'RIGHT':
            return Action.RIGHT


def heuristics(node: tuple, aim_location: tuple):
    hs = 0

    if aim_location != node:
        hs += 40 * (2 + (8000 / manhattan(aim_location[0], aim_location[1], node[0], node[1])))
    else:
        hs += 90000000

    return hs


def manhattan(i0, j0, i1, j1):
    return abs(i0 - i1) + abs(j0 - j1)


def can_eat_gem_for_us(grid_info, gem_type):
    if grid_info.Our_agent.score > Gems[gem_type][1] and grid_info.our_gem_catch_list[gem_type - 1] < Gems[gem_type][2]:
        return True
    return False


def can_eat_gem_for_enemy(grid_info, gem_type):
    if grid_info.Enemy_agent.score > Gems[gem_type][1] and grid_info.enemy_gem_catch_list[gem_type - 1] < \
            Gems[gem_type][2]:
        return True
    return False
