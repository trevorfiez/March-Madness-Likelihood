__author__ = 'Trevor'

import csv
import sys
import re
import math
import random
from lxml import etree
import time


class Bracket:
    def __init__(self):
        self.teams = []

    def create_rounds(self):
        self.teams_by_region = {}
        self.teams_by_name = {}
        for team in self.teams:
            self.teams_by_name[team.name] = team
            if team.region not in self.teams_by_region:
                self.teams_by_region[team.region] = {}
                print(team.region)

            self.teams_by_region[team.region][team.seed] = team

        self.first_round = []

        regions = ['East', 'West', 'Midwest', 'South']
        num_order = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]


        for reg in regions:
            for s in num_order:
                self.first_round.append(self.teams_by_region[reg][s])

        for round in range(6):
            cur_index = 0
            increment_step = math.pow(2, round)
            for i in range(len(self.first_round)):
                if (i % increment_step == 0 and i != 0):
                    cur_index += 1

                self.first_round[i].indices.append(cur_index)



    def calc_prob_from_file(self, filename, log=True):
        round_winners = []
        for round in range(6):
            round_winners.append([])
            for i in range(int(math.pow(2, 6 - round))):
                round_winners[round].append(0)

        with open(filename) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if (row[0] == ""):
                    continue

                for g in range(len(row[1:])):
                    if (row[1 + g] == "1"):
                        round_winners[g][self.teams_by_name[row[0]].indices[g]] = 1

        print(round_winners[4])


        round_teams = []
        round_teams.append(self.first_round)
        for round in range(len(round_winners) - 1):
            cur_round = []
            for i in range(int(math.pow(2, 5 - round))):
                cur_round.append(round_teams[-1][(i * 2) + round_winners[round][(i * 2) + 1]])

            round_teams.append(cur_round)

        for round in range(4, len(round_teams)):
            print("Round %d" % (round))
            for team in round_teams[round]:
                team.team_print()

        log_score = 0.0
        for round in range(len(round_teams)):
            for i in range(len(round_teams[round])):
                if (round_winners[round][i] == 1):
                    offset = i % 2
                    log_score += round_teams[round][i].logwin[round_teams[round][i - offset].seed]

        return log_score, math.exp(log_score)

    def rand_logscore(self):
        log_score = 0.0
        round_teams = self.first_round
        for round in range(6):
            new_list = []
            for i in range(len(round_teams) / 2):
                winner = random.randint(0, 1)
                loser = 0 if winner == 1 else 1
                log_score += round_teams[i * 2 + winner].logwin[round_teams[i * 2 + loser].seed]
                new_list.append(round_teams[i * 2 + winner])

            round_teams = new_list

        return log_score



class Team:
    def __init__(self, name, seed, probs, region):
        self.name = name
        self.seed = seed
        self.round_probs = probs
        self.region = region
        self.indices = []

    def add_indices(self):
        pass

    def team_print(self):
        print(self.name + " seed: %d, region: " % (self.seed) + self.region)

    def default_winprob(self):
        self.winprob = {}
        self.logwin = {}

        for i in range(1,17):
            winprob = 1.0 - float(i) / (i + self.seed)
            self.winprob[i] = winprob
            self.logwin[i] = math.log(winprob)
            
    def list_winprob(self, seed_wins):
        self.winprob = {}
        self.logwin = {}
        
        for i in range(1, 17):
            self.winprob[i] = seed_wins[self.seed - 1][i - 1]
            self.logwin[i] = math.log(seed_wins[self.seed - 1][i - 1])
            


class Bournoulli:
    def __init__(self, bracket):
        self.p = 0.5
        self.pos_samples = 0.0
        self.total_samples = 0.0
        self.bracket = bracket

    def set_threshold_from_file(self, filename):
        self.threshold, self.prob_threshold = self.bracket.calc_prob_from_file(filename)


    def run_bournoulli_batch(self, iters):
        for i in xrange(iters):
            rand_score = self.bracket.rand_logscore()
            if (rand_score < self.threshold):
                self.pos_samples += 1
            self.total_samples += 1

    def estimate_bournoulli(self, max_iters, batch_size):
        sys.stdout.write('\n')
        sys.stdout.flush()
        for i in xrange(0, max_iters, batch_size):
            self.run_bournoulli_batch(batch_size)
            self.cur_error = math.pow(self.total_samples, -0.5)
            sys.stdout.write("P = %06f, Max error: %0.6f\r" % (self.pos_samples / self.total_samples, self.cur_error))
            sys.stdout.flush()

        sys.stdout.write('\n')
        sys.stdout.flush()



def load_seed_win_probs(seed_file):
    seed_win_probs = []
    with open(seed_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
           
            float_row = [float(x) for x in row]
            seed_win_probs.append(float_row)
            
    return seed_win_probs
        


def dep_load_teams(filename):
    my_bracket = Bracket()
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if (int(row[3]) == 0):
                continue
            new_team = Team(row[12], int( re.sub("[^0-9]", "", row[15])), [float(row[x]) for x in range(4, 10)], row[14])
            my_bracket.teams.append(new_team)

    return my_bracket



def main(argv):

    my_bracket = dep_load_teams('2017_projections.csv')
    other_bracket = dep_load_teams('2016_projections.csv')

    seed_wins = load_seed_win_probs('seed_win_probs.csv')
    
    for team in my_bracket.teams:
        team.team_print()
        team.list_winprob(seed_wins)

    for team in other_bracket.teams:
        team.list_winprob(seed_wins)

    my_bracket.create_rounds()
    other_bracket.create_rounds()

    log_score, prob = my_bracket.calc_prob_from_file('2017_results.csv')
    other_log, other_prob = other_bracket.calc_prob_from_file('2016_results.csv')
    print(log_score)
    print(prob)

    print(other_log)
    print(other_prob)

    print(other_prob / prob)
    '''
    bourn = Bournoulli(my_bracket)
    bourn.set_threshold_from_file('2017_results.csv')
    bourn.estimate_bournoulli(100000, 10000)
    '''
    other_b = Bournoulli(other_bracket)
    other_b.set_threshold_from_file('2016_results.csv')
    other_b.estimate_bournoulli(100000, 10000)
    
    print("this finished")


if __name__ == "__main__":
    main(sys.argv[:1])
