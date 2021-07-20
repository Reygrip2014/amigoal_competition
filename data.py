import string
independent_probabilities_ = {
                  1: {"Qualification": {"Italy Regular Time": 0.3, "Italy Extra Time": 0.075, "Italy Penalties": 0.09,
                      "England Regular Time": 0.363, "England Extra Time": 0.082, "England Penalties": 0.09}},
                  2: {"Most_offsides": {'Italy': 0.481, 'England': 0.304, 'Draw': 0.215}},
                  3: {"Yellow_cards_1st_half": {'0': 0.272, '1': 0.347, '2':0.227, '3+': 0.154}},  # bingoal odds
                  4: {"Most_corners": {'Italy': 0.392, 'England': 0.473, 'Draw': 0.135}},
                  5: {"First_substitution": {'Italy': 0.579, 'England': 0.421}},
                  6: {"First_goal": {'Italy': 0.475, 'England': 0.525}},
                  7: {"First_goal_time": {'First half': 0.606, 'Second half': 0.27, 'In the extra time': 0.074,
                                          'In the penalty shoot-out': 0.05}},
                  8: {"Number_goals": {'0': 0.138, '1': 0.239, '2': 0.275, '3': 0.18, '4+': 0.168}},
                  9: {"Sub_2nd_half": {'0-3': 0.01, '3-6': 0.15, '7-9': 0.75, '10': 0.09}},
                  10: {"Wembley": {'8': 1}}
                     }


standardized_probabilities = {}
i = 0
for dic in independent_probabilities_.values():
    for event, outcomes_ in dic.items():
        i += 1
        standardized_probabilities[(i, event)] = {}
        j = 0
        for outcome_, probability_ in outcomes_.items():
            j += 1
            standardized_probabilities[(i, event)][(j, outcome_)] = probability_


# estimation of dependence ratio between outcomes (1st question serves as basis)
# shortcut we do not estimate every dependency (most often than not it's marginal)
dependence_probabilities = {
    (1, 1): {(4, 2): 0.2, (6, 1): 0.85, (7, 3): -1, (7, 4): -1, (8, 1): -1},
    (1, 2): {(6, 1): 0.33, (8, 1): -1}, (1, 3): {(7, 4): 8, (8, 2): -1, (8, 4): -1},
    (1, 4): {(4, 1): 0.2, (6, 2): 0.85, (7, 3): -1, (7, 4): -1, (8, 1): -1},
    (1, 5): {(6, 2): 0.33, (8, 1): -1}, (1, 6): {(7, 4): 8, (8, 2): -1, (8, 4): -1}
    }


# prizes for each rank
prizes = {1: 35000, 2: 1355, 3: 849}

alphabet = list(string.ascii_lowercase)
