import itertools
import random


class History():
    """
    A class for keeping track of a AI's history. It has the name, the list of opponents, the total number of rounds
    and a dictionary where opponents are keys, and either a list of their moves, your moves, or the scores are the items
    """
    def __init__(self, name):
        self.name = name
        self.oppmoves = {}
        self.mymoves = {}
        self.scores = {}
        self.round = 0
        self.listOfOpps = []

    def add_encounter(self, player, myplay, theirplay, result):
        """
        Updates a dictionary after a move.
        """
        if player not in self.listOfOpps:
            self.oppmoves[player] = []
            self.mymoves[player] = []
            self.scores[player] = []
            self.listOfOpps.append(player)

        self.mymoves[player].append(myplay)
        self.oppmoves[player].append(theirplay)
        self.scores[player].append(result)

class Player():
    list_of_players = []
    def __init__(self, movedet):
        """
        :param movedet The function for making a move. It should return True for cooperate and False for Defect
        """
        self.score = 0
        self.history = History(repr(movedet.__name__))
        self.move = movedet
        self.name = repr(movedet.__name__)
        Player.list_of_players.append(self)
    def move(self, history, opp, round ):
        """
        :param history - the algorthim's history
        :param The name of the opponent
        :param the round number
        :return True for cooperate or False for defect
        Passes the necceary information to the movedet function, which returns the move
        """
        move = self.movedet(history, opp, round)
        return move
    def update(self, opp, mymove, theirmove, result):
        self.history.add_encounter(opp, mymove, theirmove, result)
        self.score += result


class Game():
    def __init__(self, cop, copd, defc, defect, rounds):
        """
        :param cop: The reward if both cooperate
        :param copd: The reward for the player that copperates when the other defects
        :param defc: The reward for the player that defects when the other cooperates
        :param defect: The reward if they both defect
        :param rounds: The number of rounds to be played
        :return:
        """
        self.cop = cop
        self.copd = copd
        self.defc = defc
        self.defect = defect
        self.rounds = rounds
    def pay_off(self, moveA, moveB):
        """
        :param moveA Player A's move
        :param moveB Player B's Move
        :return a tuple of (player A's reward, Player B's reward
        """
        if moveA is True and moveB is True:
            return (self.cop, self.cop)
        if moveA is False and moveB is False:
            return (self.defect, self.defect)
        if moveA is True and moveB is False:
            return (self.copd,self.defc)
        if moveA is False and moveB is True:
            return (self.defc,self.copd)

    def play(self, pa, pb):
        """
        :param pa Player A
        :param pb Player B
        Plays the game for the specified number of rounds and updates all relevant information
        """
        x = 0
        while x < self.rounds:
            a = pa.move(pa.history, pb.name, x)
            b = pb.move(pb.history, pa.name, x)
            results = self.pay_off(a, b)
            pa.update(pb.name, a, b, results[0])
            pb.update(pa.name, b, a, results[1])
            x += 1

# Example functions:
def cooperate(a, b, c):
    return True

def defect(a, b, c):
    return False

def tit_for_tat(a, b, c):
    if c is 0:
        return True
    else:
        return a.oppmoves[b][-1]

def tat_for_tit(a, b, c):
    if c is 0:
        return False
    else:
        return a.oppmoves[b][-1]

def ran_bot(a,b,c):
    test = random.randint(0,1)
    if test is 1:
        return True
    if test is 0:
        return False


#Example functions turned into bots:
Player(cooperate)
Player(defect)
Player(tit_for_tat)
Player(tat_for_tit)
#Player(ran_bot)

# Plays the game with the defined pay offs and prints some information to demonstrate the history
def simulate():
    game = Game(20, -10, 10, 0, 10)
    combinations = list(itertools.combinations(Player.list_of_players,r=2))
    for x in combinations:
        game.play(x[0], x[1])
    for x in Player.list_of_players:
        print('Player: {0} Score: {1}'.format(x.name, x.score))
    for x in Player.list_of_players:
        for y in Player.list_of_players:
            if y is not x:
                score = sum(x.history.scores[y.name])
                print('{0} scored {1} with {2}'.format(x.name, score, y.name))

simulate()
