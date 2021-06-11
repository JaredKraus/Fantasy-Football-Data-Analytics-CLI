from data_import import final_df
import pandas as pd
import numpy as np

# required so pycharm prints out pandas dataframes correctly
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',17)

def obtain_user_input():
    """
    A function which uses the terminal to obtain league type (PPR or STD), football position to analyze
    (WR, RB, QB, or TE), count of players to consider in analysis, and the ranking system which will be used in
    comparing players (ADP or 2020 points). All input is validated, and user is prompted to re-enter value if
    invalid entry is given.
    :param: none
    :return: Tuple with (league_type, pos, rank_sys, n_rows)
    """


    league_types = ['PPR', 'STD']  # possible acceptable league types

    while True:  # continue till valid entry given
        try:
            league_type = input("Enter a League Type (PPR or STD): ").upper()  # obtain value from user
            if league_type in league_types:  # check if it's valid
                break  # entry is valid therefore break
            else:  # invalid entry
                raise ValueError
        except:
            # presesnt error message and redo loop
            print("Invalid Entry: please enter either PPR or STD")


    positions = ['WR', 'RB', 'QB', 'TE']  # possible acceptable positions
    while True:  # continue till valid entry given
        try:
            pos = input("Please enter a position (WR, RB, QB, or TE): ").upper()  # obtain value from user
            if pos in positions:  # make sure position is valid
                break  # entry is valid so break.
            else:  # invalid entry
                raise ValueError
        except:
            # presesnt error message and redo loop
            print("Invalid Entry: please enter either WR, RB, QB, or TE")



    idx = pd.IndexSlice  # index slice object used to slice df
    num_pos = final_df.loc[idx[league_type, pos], :].shape[0]  # total count of the position.
    while True:  # continue till valid entry given
        try:
            n_rows = input(f"Enter a count of players to study as an integer (max: {num_pos} for {pos}): ")
            n_rows = int(n_rows)  # will raise ValueError if not an integer.
            if n_rows <= num_pos:  # ensure < than count of position
                break  # brak since valid entry
            else:  # invalid entry
                raise ValueError
        except ValueError:
            # presesnt error message and redo loop
            print(f"Invalid entry: please enter an integer less than {num_pos}")


    # possible user entry values. 
    rank_dict = {
        "1": "ADP",
        "2": "TTL PTS"
    }

    while True:  # continue till valid entry given
        # obtain value from user
        rank_sys = input("Enter how you would like to rank players (1 for ADP, 2 for 2020 Total Points): ")
        try:
            if rank_sys in rank_dict:  # valid entry
                rank_sys = rank_dict[rank_sys]
                break
            else:  # invalid entry
                raise ValueError
        except ValueError:
            # presesnt error message and redo loop
            print("Invalid Entry: please enter either 1 for ADP, or 2 for 2020 Total Points")

    return league_type, pos, rank_sys, n_rows