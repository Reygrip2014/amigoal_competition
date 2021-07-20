events = {1: {"HOW MANY MATCHES HAVE BEEN PLAYED AT WEMBLEY DURING THIS EURO (INCLUDING THE FINAL)?":
              ["5", "6", "7", "8"]},
          2: {"WHICH TEAM WILL OPEN THE SCORE IN ITALY -"
              "ENGLAND (INCLUDING POSSIBLE PENALTY SHOOT-OUT)?": ["Italy", "England"]},
          3: {"WHEN WILL THE FIRST GOAL BE SCORED IN ITALY - ENGLAND?":
              ["First half", "Second half", "In the extra time", "Penalty shootout"]},
          4: {"HOW MANY GOALS WILL BE SCORED IN ITALY - ENGLAND (POSSIBLE PENALTY SHOOT-OUT NOT INCLUDED)?":
              ["0", "1", "2", "3", "4 or more"]},
          5: {"HOW MANY YELLOW CARDS WILL BE GIVEN DURING THE FIRST HALF OF ITALY - ENGLAND?":
              ["None", "1", "2", "3 or more"]},
          6: {"HOW MANY SUBSTITUTIONS WILL BE MADE DURING THE SECOND HALF OF ITALY - ENGLAND?":
              ["0, 1, 2 or 3", "4, 5 or 6", "7, 8 or 9", "10"]},
          7: {"WHICH TEAM WILL MAKE THE FIRST SUBSTITUTION IN ITALY - ENGLAND?":
                  ["Italy", "England", "No substitution"]},
          8: {"WHICH TEAM WILL HAVE THE MOST CORNER KICKS IN ITALY - ENGLAND?": ["Italy", "England", "Equal"]},
          9: {"WHICH TEAM WILL BE FLAGGED OFFSIDE MOST OFTEN IN ITALY - ENGLAND?": ["Italy", "England", "Equal"]},
          10: {"WHICH TEAM WILL WIN THIS EURO AND HOW?": ["Italy, without a penalty shoot-out",
                                                          "Italy, after a penalty shoot-out", "England, without "
                                                          "a penalty shoot-out", "England, after a penalty shoot-out"]}
          }


baseline_proba = {"Qualification": {"Italy Regular Time": 0.3, "Italy Extra Time": 0.075, "Italy Penalties": 0.09,
                  "England Regular Time": 0.363, "England Extra Time": 0.082, "England Penalties": 0.09},
                  "Most_offsides": {'Italy': 0.481, 'England': 0.304, 'Draw': 0.215},
                  "Yellow_cards_1st_half": {'0': 0.272,'1': 0.347,'2': 0.227, '3+': 0.154},  # bingoal
                  "Most_corners": {'Italy': 0.392, 'England': 0.473, 'Draw': 0.135},
                  "First_substitution": {'Italy': 0.579, 'England': 0.421},
                  "First_goal": {'Italy': 0.475, 'England': 0.525},
                  "First_goal_time": {'First half': 0.606, 'Second half': 0.27, 'In the extra time': 0.074,
                                      'In the penalty shoot-out': 0.05},
                  "Number_goals": {'0': 0.138, '1': 0.239, '2': 0.275, '3': 0.18, '4+': 0.168},  # proba
                  "Sub_2nd_half": {'0-3': 0.02, '3-6': 0.13, '7-9': 0.75, '10': 0.1},
                  "Wembley": {'8': 1}
                  }
