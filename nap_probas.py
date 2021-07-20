import numpy as np


over_under = {'0.5': {'over': 1.12, 'under': 7},
              '1.5': {'over': 1.54, 'under': 2.55},
              '2.5': {'over': 2.75, 'under': 1.47},
              '3.5': {'over': 5.75, 'under': 1.16},
              }
#"Number_goals": {'0': 0.138, '1': 0.239, '2': 0.275, '3': 0.18, '4+': 0.168}

goal_1st_half = {'yes': 1.53, 'no': 2.35}
goal_2nd_half = {'yes': 1.36, 'no': 2.95}


odds = {"Qualification": {"Italy Regular Time": 2.9, "Italy Extra Time": 12, "Italy Penalties": 10,
        "England Regular Time": 2.55, "England Extra Time": 11, "England Penalties": 10},
        "Most_offsides": {'Italy': 1.9, 'England': 3, 'Draw': 4.25},
        "Yellow_cards_1st_half": {'0': 3,'1': 2.35,'2':3.6,'3+': 5.3},  # bingoal
        "Most_corners": {'Italy': 2.32, 'England': 1.92, 'Draw': 6.75},
        "First_substitution": {'Italy': 1.6, 'England': 2.2},
        "First_goal_team": {'Italy': 1.96, 'England': 1.77},
        }

def evaluate_probas(events):
    odds = list(events.values())
    odds = np.array(odds)
    odds = 1/odds
    total = sum(odds)
    margin = total-1  # 1-1/total
    factor = 1+margin
    new_dic = dict()
    for a, b in events.items():
        b = 1/(b*factor)
        new_dic[a] = b
    return new_dic


for line,odds in odds.items():
    a = evaluate_probas(odds)
    print(a)

