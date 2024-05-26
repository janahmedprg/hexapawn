import copy

# Part 1: The state is a list of 10 elements where
# the first element is the players turn and the
# rest is the board in row major order.

# Note: We don't need to_move function
#       since the first element of the state
#       stores players turn.

initial_state = [1, 
                -1, -1, -1, 
                0, 0, 0, 
                1, 1, 1]


class Hexapawn:
    def __init__(self, board=initial_state):
        self.board = board 
        self.actions = self.get_actions()

    # An action is defined as a 3 tuple
    # first element - direction -1, 0, 1 (left, forward, right)
    # second element - move from
    # third element - move to
    def get_actions(self):
        action_list = []
        if (self.board[0] == 1):
            pawns_loc = [i for i, x in enumerate(self.board) if (i>0 and x == 1)]
            for p in pawns_loc:
                if p-3>0 and self.board[p-3] == 0:
                    action_list.append((0, p, p-3))
                if p-4>0 and p%3 != 1 and self.board[p-4] == -1:
                    action_list.append((-1, p, p-4))
                if p-2>0 and p%3 != 0 and self.board[p-2] == -1:
                    action_list.append((1, p, p-2))

        else:
            pawns_loc = [i for i, x in enumerate(self.board) if (i>0 and x == -1)]
            for p in pawns_loc:
                if p+3<10 and self.board[p+3] == 0:
                    action_list.append((0, p, p+3))
                if p+4<10 and p%3 != 0 and self.board[p+4] == 1:
                    action_list.append((-1, p, p+4))
                if p+2<10 and p%3 != 1 and self.board[p+2] == 1:
                    action_list.append((1, p, p+2))
        return action_list

    def result(self, action):
        new_board = copy.deepcopy(self.board)
        new_board[action[2]] = new_board[0]
        new_board[action[1]] = 0
        new_board[0] = 1 if new_board[0] == -1 else -1
        return new_board

    def is_terminal(self):
        terminal = False
        if 1 in self.board[1:4]:
            terminal = True
        if -1 in self.board[7:10]:
            terminal = True
        if len(self.actions) == 0:
            terminal = True
        return terminal
    
    def utility(self):
        if 1 in self.board[1:4]:
            return 1
        if -1 in self.board[7:10]:
            return -1
        return 1 if self.board[0] == -1 else -1

# Part 2: Minimax search

policy_table = {}

def minimax_search(game: Hexapawn):
    return max_value(game)

def max_value(game: Hexapawn):
    if game.is_terminal():
        return (game.utility(), None)
    v = -1000000000
    policy = {}
    for a in game.actions:
        v2, a2 = min_value(Hexapawn(game.result(a)))
        if v2 > v:
            v, move = v2, a
        if v2 in policy:
            policy[v2].append(a)
        else:
            policy[v2] = [a]
    policy_table[str(game.board)] = policy
    return v, move

def min_value(game: Hexapawn):
    if game.is_terminal():
        return (game.utility(), None)
    v = 1000000000
    policy = {}
    for a in game.actions:
        v2, a2 = max_value(Hexapawn(game.result(a)))
        if v2 < v:
            v, move = v2, a
        if v2 in policy:
            policy[v2].append(a)
        else:
            policy[v2] = [a]
    policy_table[str(game.board)] = policy
    return (v, move)

minimax_search(Hexapawn())
print(policy_table)