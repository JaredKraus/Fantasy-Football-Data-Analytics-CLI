from data_import import final_df
import pandas as pd
import numpy as np
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',17)

def obtain_user_input():
    league_types = ['PPR', 'STD']

    while True:
        try:
            league_type = input("Enter a League Type (PPR or STD): ").upper()
            if league_type in league_types:
                break
            else:
                raise ValueError
        except:
            print("Invalid Entry: please enter either PPR or STD")


    positions = ['WR', 'RB', 'QB', 'TE']
    while True:
        try:
            pos = input("Please enter a position (WR, RB, QB, or TE): ").upper()
            if pos in positions:
                break
            else:
                raise ValueError
        except:
            print("Invalid Entry: please enter either WR, RB, QB, or TE")



    idx = pd.IndexSlice  # index slice object used to slice df
    num_pos = final_df.loc[idx[league_type, pos], :].shape[0]  # total count of the position.
    while True:
        try:
            n_rows = input(f"Enter a count of players to study as an integer (max: {num_pos} for {pos}): ")
            n_rows = int(n_rows)
            if n_rows <= num_pos:
                break
            else:
                raise ValueError
        except:
            print(f"Invalid entry: please enter an integer less than {num_pos}")


    rank_dict = {
        "1": "ADP",
        "2": "TTL PTS"
    }
    rank_sys = input("Enter how you would like to rank players (1 for ADP, 2 for 2020 Total Points): ")
    try:
        while True:
            if rank_sys in rank_dict:
                rank_sys = rank_dict[rank_sys]
            else:
                raise ValueError
    except:
        print("Invalid Entry: please enter either 1 for ADP, or 2 for 2020 Total Points")

    return league_type, pos, rank_sys, n_rows