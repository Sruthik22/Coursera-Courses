"""
Stress testing for SolitaireMancala
"""

#import poc_simpletest
import random
#import codeskulptor

#codeskulptor.set_timeout(100)  # prevent browser from freezing and killing the program

# create test_cases
TEST_LENGTH = 10
# [[]]*TEST_LENGTH though genius, does not work due to issues with list reference
TEST_CASES = [[] for dummy_idx in range(TEST_LENGTH)]
for a_config in TEST_CASES:
    # create a random length for each test case
    length = random.choice(range(1, 11))
    # create elements for each test case
    a_config.append(0)  # first element in each configuration must be 0
    for dummy_idx in range(length - 1):
        a_config.append(2** random.randint(0, 10))
print(TEST_CASES)
"""
# function to detect bug
def run_suite(myclass, yourclass):
    # create a test suite
    suite = poc_simpletest.TestSuite()

    # stress testing for each test case using suite.run_test(...)
    for a_config in TEST_CASES:
        # correct implementation
        my_game = myclass()
        my_game.set_board(a_config)
        # incorrect implementation
        your_game = yourclass()
        your_game.set_board(a_config)
        # compare between correct and incorrect
        suite.run_test(my_game.plan_moves(), your_game.plan_moves(), \
                       'Failed at configuration ' + str(a_config))

    # report the number of tests and failures
    suite.report_results()


# these are the classes that we want to debug

# this is the correct implementation
class SolitaireMancala:

    def __init__(self):
        self._board = [0]

    def set_board(self, configuration):
        self._board = list(configuration)

    def __str__(self):
        temp = list(self._board)
        temp.reverse()
        return str(temp)

    def get_num_seeds(self, house_num):
        return self._board[house_num]

    def is_game_won(self):
        for idx in range(1, len(self._board)):
            if self._board[idx] != 0:
                return False
        return True

    def is_legal_move(self, house_num):
        move_in_range = 0 < house_num < len(self._board)
        index_matches = self._board[house_num] == house_num
        return move_in_range and index_matches

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for idx in range(house_num):
                self._board[idx] += 1
            self._board[house_num] = 0

    def choose_move(self):
        for house_num in range(1, len(self._board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0

    def plan_moves(self):
        new_board = SolitaireMancala()
        new_board.set_board(self._board)
        move_list = []
        next_move = new_board.choose_move()
        while next_move != 0:
            new_board.apply_move(next_move)
            move_list.append(next_move)
            next_move = new_board.choose_move()
        return move_list


# these are incorrect implementations
class SolitaireMancala1:

    def __init__(self):
        self.board = [0]

    def set_board(self, configuration):
        self.board = list(configuration)

    def __str__(self):
        return str(self.board[::(-1)])

    def get_num_seeds(self, house_num):
        return self.board[house_num]

    def is_game_won(self):
        if (sum(self.board[1:]) == 0):
            return True
        else:
            return False

    def is_legal_move(self, house_num):
        if ((house_num != 0) and (self.get_num_seeds(house_num) == house_num)):
            return True
        else:
            return False

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for house in range(house_num):
                self.board[house] += 1
            self.board[house_num] = 0

    def choose_move(self):
        shortest_legal_move = 0
        for house in range(len(self.board)):
            if self.is_legal_move(house):
                shortest_legal_move = house
                break
        return shortest_legal_move

    def plan_moves(self):
        plan_board = list(self.board)
        plan = []
        while (self.choose_move() != 0):
            for house_num in range(len(self.board)):
                plan.append(self.choose_move())
                self.apply_move(self.choose_move())
        self.board = plan_board
        return plan


class SolitaireMancala2:

    def __init__(self):
        self.board = [0]

    def set_board(self, configuration):
        self.board = [configuration[house] for house in range(len(configuration))]

    def __str__(self):
        board = ']'
        ndx = 0
        while (ndx < len(self.board)):
            board = ((', ' + str(self.board[ndx])) + board)
            ndx += 1
        return ('[' + board[2:])

    def get_num_seeds(self, house_num):
        return self.board[house_num]

    def is_game_won(self):
        for house_num in range(1, len(self.board)):
            if (self.board[house_num] != 0):
                return False
        return True

    def is_legal_move(self, house_num):
        if (house_num == 0):
            return False
        return (self.board[house_num] == house_num)

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for houses in range(house_num):
                self.board[houses] += 1
            self.board[house_num] = 0

    def choose_move(self):
        for house_num in range(1, len(self.board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0

    def plan_moves(self):
        moves = []
        for house_num in range(1, len(self.board)):
            if self.is_legal_move(house_num):
                self.apply_move(house_num)
                moves.append(house_num)
        return moves


class SolitaireMancala3:

    def __init__(self):
        self._board = [0]

    def set_board(self, configuration):
        self._board = configuration[:]

    def __str__(self):
        return str([self._board[i] for i in range((len(self._board) - 1), (-1), (-1))])

    def get_num_seeds(self, house_num):
        return self._board[house_num]

    def is_legal_move(self, house_num):
        if ((house_num == 0) or (house_num >= len(self._board))):
            return False
        else:
            return (house_num == self._board[house_num])

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for i in range(house_num):
                self._board[i] += 1
            self._board[house_num] = 0

    def choose_move(self):
        for i in self._board[1:]:
            if self.is_legal_move(i):
                return i
        return 0

    def is_game_won(self):
        won = True
        for i in self._board[1:]:
            if (i != 0):
                won = False
        return won

    def plan_moves(self):
        moves = []
        while True:
            move = self.choose_move()
            if ((move == 0) or self.is_game_won()):
                break
            else:
                self.apply_move(move)
                moves.append(move)
        return moves


class SolitaireMancala4:

    def __init__(self):
        self.game_board = [0]

    def set_board(self, configuration):
        self.game_board = configuration[::]

    def __str__(self):
        game_board = self.game_board[::]
        game_board.reverse()
        return str(game_board)

    def get_num_seeds(self, house_num):
        return self.game_board[house_num]

    def is_game_won(self):
        if (self.game_board[1:].count(0) == len(self.game_board[1:])):
            return True
        return False

    def is_legal_move(self, house_num):
        if (house_num == 0):
            return False
        elif (self.game_board[house_num] == house_num):
            return True
        return False

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            self.game_board[house_num] = 0
            for num in range(house_num):
                self.game_board[num] += 1

    def choose_move(self):
        for num in self.game_board[1:]:
            if (self.game_board.index(num, 1) == num):
                return num
        return 0

    def plan_moves(self):
        ret = []
        while (not self.is_game_won()):
            check_num = self.choose_move()
            if (check_num != 0):
                ret.append(check_num)
            if (check_num == 0):
                break
            self.apply_move(check_num)
        return ret


# run stress testing
# run_suite(SolitaireMancala, SolitaireMancala1)
# run_suite(SolitaireMancala, SolitaireMancala2)
# run_suite(SolitaireMancala, SolitaireMancala3)
# run_suite(SolitaireMancala, SolitaireMancala4)
"""