#!/usr/bin/env python
from ants import *
from random import shuffle
import math
# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us

def debug(msg, end='\n'):
    bot_name = 'Bot1'
    print('bot={}: {}'.format(bot_name, msg), end=end, file=sys.stderr)

class Ant:
    def __init__(self, location):
        self.pos = location
        self.last_pos = location
        self.path = []
        self.target = False


class Food:
    def __init__(self, _location):
        pos = _location


class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        ANTS = 0
        DEAD = -1
        LAND = -2
        FOOD = -3
        WATER = -4
        self.my_ants = []
        self.food = []
        self.width = 1
        self.height = 1

        debug('Start3')

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.width = ants.cols
        self.height = ants.rows
        pass

    def destination(self, loc, direction):
        'calculate a new location given the direction and wrap correctly'
        row, col = loc
        AIM = {'n': (-1, 0),
            'e': (0, 1),
            's': (1, 0),
            'w': (0, -1)}
        d_row, d_col = AIM[direction]
        return ((row + d_row) % self.height, (col + d_col) % self.width)

    def do_move(self, loc, direction):
        new_loc = self.destination(loc, direction)

        if (ants.passable(new_loc)
            and new_loc not in ants.my_ants()
            and new_loc not in move_orders):

            ants.issue_order((loc, direction))
            move_orders[new_loc] = loc
            return True
        else:
            return False

    def do_target_move(self, loc, target):
        # move to target
        directions = ants.direction(loc, target)
        for direction in directions:
            if (self.do_move(loc, direction)):
                move_targets[target] = loc
                return True
        return False

    def move_away_from_target(self, loc, target):
        directions = ['n', 'e', 's', 'w']
        shuffle(directions)
        bad_directions = self.direction(loc, target)
        for direction in directions:
            if (direction not in bad_directions
                and self.do_move(loc, direction)):

                move_targets[target] = loc
                return True
        return False

    def random_move(self, loc):
        directions = ['n', 'e', 's', 'w']
        shuffle(directions)
        for direction in directions:
            if (self.do_move(loc, direction)):
                break

    def distance(self, width, height, loc1, loc2):
        'calculate the closest distance between to locations'
        row1, col1 = loc1
        row2, col2 = loc2
        d_col = min(abs(col1 - col2), width - abs(col1 - col2))
        d_row = min(abs(row1 - row2), height - abs(row1 - row2))
        return math.hypot(d_col, d_row)

    def direction(self, loc1, loc2):
        'determine the 1 or 2 fastest (closest) directions to reach a location'
        row1, col1 = loc1
        row2, col2 = loc2
        height2 = self.height//2
        width2 = self.width//2
        d = []
        if row1 < row2:
            if row2 - row1 >= height2:
                d.append('n')
            if row2 - row1 <= height2:
                d.append('s')
        if row2 < row1:
            if row1 - row2 >= height2:
                d.append('s')
            if row1 - row2 <= height2:
                d.append('n')
        if col1 < col2:
            if col2 - col1 >= width2:
                d.append('w')
            if col2 - col1 <= width2:
                d.append('e')
        if col2 < col1:
            if col1 - col2 >= width2:
                d.append('e')
            if col1 - col2 <= width2:
                d.append('w')
        return d

    def passable(loc):
        if (loc not in ants
            and loc not in waters
            and loc not in hills):

            return True
        else:
            return False

    def find_path(loc):
        pass

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):

        # Update lists
        current_ant_list = []
        for ant in self.my_ants:
            if (ant.pos in ants.my_ants()):
                current_ant_list.append(ant)
        self.my_ants = current_ant_list
        del(current_ant_list)
        for ant in ants.my_ants():
            for other in self.my_ants:
                debug(other)
                #if ant = (x for x in ants.my_ants if x not in lambda pos: pos.pos):
            self.my_ants.append(Ant(location=ant))

        current_food_list = []
        for food in self.food:
            if (food.pos in ants.food()):
                current_food_list.append(food)
        self.food = current_food_list
        del(current_food_list)


        move_orders = {}
        food_targets = {}
        move_targets = {}

        # -------------------------

        debug('Starting turn')
        # ant logic
        for ant in ants.my_ants():
            hill_distances = []
            for hill in ants.my_hills():
                debug('TEST\n')
                debug('ants.cols:{}, ants.rows:{}, ant:{}, hill:{}, distance:{}'.format(ants.cols, ants.rows, ant, hill, self.distance(10, 10, (1,1), (2,2))))
                hill_distances.append([hill, self.distance(ants.cols, ants.rows, ant, hill)])
            hill_distances = sorted(hill_distances, key=lambda hill_d: hill_d[1])

            food_distances = []
            for food in ants.food():
                food_distances.append([food, self.distance(ants.cols, ants.rows, ant, food)])
            food_distances = sorted(food_distances, key=lambda food_d: food_d[1])

            ant_distances = []
            for other_ant in ants.my_ants():
                if ant != other_ant:
                    ant_distances.append([other_ant, self.distance(ants.cols, ants.rows, ant, other_ant)])
            ant_distances = sorted(ant_distances, key=lambda ant_d: ant_d[1])

            debug('ant: {}'.format(ant))
            if (len(hill_distances) and hill_distances[0][1] < 4):    # Move away from hills or stay put if you cant
                debug(', choice: away from hill.')
                if not self.move_away_from_target(ant, hill_distances[0][0]):
                    debug(', choice: could not move away from hill, random move.')
                    random_move(ant)


            elif (len(ant_distances)
                and ant_distances[0][1] < 5):    # Move away from other ants or stay put if you cant

                debug(', choice: away from other ants, or stay.')
                if not self.move_away_from_target(ant, ant_distances[0][0]):
                    debug(', choice: stay.')

            elif (len(ants.food())):
                debug(', choice: get food.')
                for food in food_distances:
                    if(food[0] not in move_targets
                        and food[0] not in food_targets):

                        food_targets[food[0]] = ant
                        do_target_move(ant, food[0])
                        break

            else:
                debug(', choice: find food, random move.')
                directions = ('n', 'e', 's', 'w')
                for direction in directions:
                    if (self.do_move(ant, direction)):
                        break


            debug('(end ant: {})\n'.format(ant))

            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break



if __name__ == '__main__':
    debug("Bot Start")
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
