# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import bisect
import os
import numpy as np
import math
import copy
from operator import attrgetter
import itertools as it
from data import *


class App:
    def __init__(self, users, df, competition, last_round_simulation):
        self.users = users
        self.df = df
        self.competition = competition
        self.last_round_simulation = last_round_simulation


class Combination:
    """Combination object are the possible scenarios, possible combinations by the
     contenders > possible combinations of events"""
    objects = []

    def __init__(self, market_outcome, combination_list):
        self.market_outcome = market_outcome
        self.combination_list = combination_list
        self.base_market_probabilities = base_market_outcomes  # from data file
        self.total_odds = None
        self.match_combi_to_odds()
        Combination.objects.append(self)

    def match_combi_to_odds(self):
        """

        :return:
        """
        conditional_proba_object = ConditionalProbabilities.objects[self.market_outcome]
        base_market_outcome_probability = self.base_market_probabilities[self.market_outcome]
        probabilities = conditional_proba_object.conditional_probabilities_wo_label
        combi_odds = 1
        combi_odds *= base_market_outcome_probability
        combi_to_odds = dict()
        for combi in self.combination_list:
            q_index = alphabet.index(combi[0])+1
            index = q_index, combi[1]
            single_odd = probabilities[index]
            combi_odds *= single_odd
        combi_odds = round(combi_odds, 10)
        combi_to_odds[self.combination_list] = combi_odds
        self.total_odds = combi_to_odds


class ConditionalProbabilities:
    objects = {}

    def __init__(self, market_outcome, conditional_probabilities):
        self.conditional_probabilities = conditional_probabilities
        self.market_outcome = market_outcome
        self.combinations = []
        ConditionalProbabilities.objects[market_outcome] = self
        self.conditional_probabilities_wo_label = self.probas_wo_labels()
        self.create_combinations()

    def probas_wo_labels(self):
        """remove strings on markets (to only get """
        wo_labels = {}
        for q, outcome_dic in self.conditional_probabilities.items():
            for outcome, odds in outcome_dic.items():
                tuple_odds = (q[0], outcome[0])
                wo_labels[tuple_odds] = odds
        return wo_labels

    def create_combinations(self):
        """

        :return:
        """
        # print(conditional_probas_filtered)
        a_ = [[(alphabet[a_[0] - 1], c_[0]) for c_ in b_.keys()] for a_, b_ in self.conditional_probabilities.items()]
        #  a = ([('a', 0), ('a', 1)], [('b',0), ('b',1)])
        combinations = list(it.product(*a_))
        for combination in combinations:
            self.combinations.append(Combination(self.market_outcome, combination))


class LastRound:
    def __init__(self, independent_probabilities, dependence_ratios):
        self.base_probas = self.create_copy_dictionary(independent_probabilities)
        self.independent_probabilities = independent_probabilities  # nested dictionary matching each questions to the
        # outcomes and the odds associated with them
        self.dependence_ratios = dependence_ratios  # nested dictionary matching outcome 1st question to dependence
        # ratio related to every other outcome
        self.default_market = 'Qualification'
        self.base_market = None
        self.base_outcome = None

    def calculate_conditional_probabilities(self):
        for outcome in self.dependence_ratios.keys():
            # print('\n\nFOR OUTCOME ' + str(outcome))
            event_nb, outcome_nb = outcome
            probabilities = self.calculate_proba_after_outcome(event_nb, outcome_nb)
            self.create_conditional_probabilities_objects(probabilities)
        return

    @staticmethod
    def create_copy_dictionary(dictionary):
        return copy.deepcopy(dictionary)

    def calculate_proba_after_outcome(self, question_nb, outcome_nb):  # calculate conditional proba
        """
        :param question_nb: question number
        :param outcome_nb: outcome number (in relation to question)
        match base_market and outcome_market to ConditionalProbabilities objects
        """
        self.base_market = (question_nb, self.default_market)  # base market- setting the probability to 1 or 0 for each
        # outcome possible from the base market in order to calculate the conditional probabilities of all the
        # other outcomes
        for outcome in self.independent_probabilities[self.base_market].keys():
            if outcome_nb in outcome:
                self.base_outcome = outcome
        dependence_probabilities = self.dependence_ratios[(question_nb, outcome_nb)]  # getting the conditional
        # probabilities for given outcome in base market
        return self.adjust_probabilities(dependence_probabilities)

    def adjust_probabilities(self, dependence_probabilities):
        """
        :param dependence_probabilities: dependence ratios for given base market and outcome
        :return:
        """
        # needs to use a dic copy as we don't
        # want to modify the original nested dic
        if self.base_market in self.base_probas:
            del self.base_probas[self.base_market]
        for index, increase_factor in dependence_probabilities.items():
            question_, outcome = index
            question_outcome = {q: outcome_matching_proba for q, outcome_matching_proba in self.base_probas.items() if
                                question_ in q}  # getting the dependent questions
            outcome_odds = list(question_outcome.values())[0]  # unnecessary nested dic
            new_outcome_odds = {key: odds*(1+increase_factor) for key, odds in outcome_odds.items() if outcome in key}
            self.calibrate_odds(outcome_odds, new_outcome_odds)   # probas dic now holds correct odds
        return self.filter_nul_probabilities()

    @staticmethod
    def calibrate_odds(outcome_dic, outcome_modify):
        """
        Calibrate odds so total probability is equal to 1 (as we previously adjusted the probability
        on a selected outcome)
        :param outcome_dic: outcomes matching a probability (all the outcomes in the dictionary being complementary)
        :param outcome_modify: single outcome whose odds ought to be modified to the corresponding value
        """
        for key in outcome_modify.keys():
            new_odd = round(outcome_modify[key], 3)
            outcome_dic[key] = new_odd
        complementary_odds = {key: odds for key, odds in outcome_dic.items() if key not in outcome_modify}
        factor = (1-new_odd)/sum(list(complementary_odds.values()))
        adjusted_odds = {key: round(odds*factor, 3) for key, odds in complementary_odds.items()}
        outcome_dic.update(adjusted_odds)
        assert round(sum(outcome_dic.values()), 4) == 1
        # return outcome_dic

    def filter_nul_probabilities(self):
        conditional_probas_filtered = copy.deepcopy(self.base_probas)
        for a_, b_ in self.base_probas.items():
            for outcome, odds in b_.items():
                if odds == 0:
                    del conditional_probas_filtered[a_][outcome]
        return conditional_probas_filtered

    def create_conditional_probabilities_objects(self, conditional_probas_filtered):
        ConditionalProbabilities(self.base_outcome, conditional_probas_filtered)
        # self.conditional_probabilities_objects[self.base_outcome] = ci_object
        # chunk 3



class Competition:
    """we are not evaluating the possibility that it could be good
     to mix some impossible results as an hedge"""
    def __init__(self, competition_table, users_objects, probabilities):
        self.df = competition_table
        self.users = users_objects
        self.sorted_by_rank = self.users.copy()
        self.sorted_by_rank.sort(key=attrgetter('ranking'))
        self.probabilities = probabilities

    def expected_points_max(self):
        for question, outcomes in self.independent_probabilities.items():
            for outcome, probability in outcomes.items():
                pass


class User:
    def __init__(self, points, username, ranking):
        self.points = points
        self.username = username
        self.ranking = ranking
        self.true_randomness_funcs = {101: '0.05+(0.1*ranking-1)/100', 201: '0.15+(0.1*ranking-101)/100', 501: 0.25}
        self.bias_towards_expected_points = {101: '0.05+(0.15*ranking-1)/100', 501: 0.2}
        """iterate for each player the best strategy with some randomness associated with it 
        and with bias towards more probable outcomes + a ratio of awareness.
        2 models: maximise expected points or maximise dollars"""

    def estimate_randomness(self):
        index = bisect.bisect_right(list(self.true_randomness_funcs.keys()), self.ranking)
        randomness_func = list(self.true_randomness_funcs.values())[index]
        # noinspection PyUnusedLocal
        ranking = self.ranking
        true_randomness = exec(randomness_func)
        return true_randomness

    @staticmethod
    def close_odds_randomness(cote_a, cote_b):
        odds_difference = abs(cote_a - cote_b)
        randomness_close_odds = {0.2: 0.98, 0.5: 0.7, 0.85: 0.2, 1.2: 0.1, 2: 0}  # key: odds_difference
        # value: randomness resulting on a wrong probability estimate (1 being the maximum)
        index = bisect(randomness_close_odds.keys(), odds_difference)
        close_odds_randomness = list(randomness_close_odds.values())[index]
        return close_odds_randomness

    def bias_expected_points(self):
        index = bisect.bisect_right(self.bias_towards_expected_points.keys(), self.ranking)
        bias_expected_points = list(self.bias_towards_expected_points.values())[index]
        ranking = self.ranking
        bias_expected_points = exec(bias_expected_points)
        return bias_expected_points

    def bias_dependent_probabilities(self):
        pass


def get_data():
    df = pd.read_excel('/Users/mini/Desktop/amigoal copy/ranking_nap copy.xlsx', header=None)
    df = df.iloc[::2]
    df = df.reset_index()
    df = df[[1, 2]]
    df = df.rename(columns={1: 'username', 2: 'points'})
    df['ranking'] = range(1, 301)
    df['prize'] = df.apply(lambda x: prizes[x['ranking']] if x['ranking'] in prizes.keys() else None, axis=1)
    return df


if __name__ == '__main__':
    df_ = get_data()
    users = []
    for row_n, row in df_.iterrows():
        user = User(row['username'], row['points'], row['ranking'])
        users.append(user)
    competition = Competition(df_, users, standardized_probabilities)
    last_round = LastRound(standardized_probabilities, dependence_ratios)
    last_round.calculate_conditional_probabilities()
    #  conditional_probabilities = last_round.conditional_probabilities_objects
    #  print(conditional_probabilities)
    # print(combi_odds[index][combi])

     #app = App(users, df_, competition, last_round)


# users_sorted_by_rank = competition.sorted_by_rank


# for user in users_sorted_by_rank:
# print(user.estimate_randomness(), user.ranking)


