import math
import os

from data_import import final_df
from user_input import obtain_user_input

import pandas as pd
import numpy as np

# required so pycharm prints out pandas dataframes correctly
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 17)

def ind_player_stats():
    """
    Uses obtain_user_input() to obtain fantasy football league type, football position, Ranking system for players,
    and count of players to study. The program prints out a table with individual stats for the number of players
    specified. It then prints out a summary statistics table for the specified number of players. Finally, it gives a
    table of number of players taken in the first 16 rounds of a fantasy football draft, for both STD leagues and PPR
    leagues.
    :param: none
    :return: nothing
    """
    league_type, pos, rank_sys, n_rows = obtain_user_input()
    # testing values
    # league_type = 'PPR'
    # pos = 'TE'
    # rank_sys = 'ADP'
    # n_rows = 10


    # positions: 'WR', 'RB', 'QB', 'TE'
    # key = position name
    # value = list with [rows to display relevant to that position, corresponding indexes for dataframe. ]
    pos_df_cols_dict = {
        "RB": [['NAME', 'TEAM', 'ADP', 'GP', 'RK', 'TTL PTS', 'PTS/GAME', 'RUSHING YDS','Rushing Pts', 'RECEIVING YARDS', 'Receiving Pts'],
                   ['Player Info','Player Info','Projections','2020','2020','2020', '2020', '2020', '2020', '2020', '2020']],
        "WR": [['NAME', 'TEAM', 'ADP', 'GP', 'RK', 'TTL PTS', 'PTS/GAME', 'RUSHING YDS','Rushing Pts', 'RECEIVING YARDS', 'Receiving Pts'],
                       ['Player Info','Player Info','Projections','2020','2020','2020', '2020', '2020', '2020', '2020', '2020']],
        "QB": [['NAME', 'TEAM', 'ADP', 'GP', 'RK', 'TTL PTS', 'PTS/GAME', 'RUSHING YDS','Rushing Pts', 'PASSING YDS', 'Passing Pts'],
                           ['Player Info','Player Info','Projections','2020','2020','2020', '2020', '2020', '2020', '2020', '2020']],
        "TE": [['NAME', 'TEAM', 'ADP', 'GP', 'RK', 'TTL PTS', 'PTS/GAME', 'RUSHING YDS','Rushing Pts', 'RECEIVING YARDS', 'Receiving Pts'],
                           ['Player Info','Player Info','Projections','2020','2020','2020', '2020', '2020', '2020', '2020', '2020']],

    }


    # filter table to league_type
    # filter to pos
    # rank based on rank_sys
    idx = pd.IndexSlice  # index slice object used to slice df
    # display columns based on position (from pos_df_cols_dict)
    position_df = final_df[pos_df_cols_dict[pos][0]].loc[idx[league_type,pos],:].copy()


    if rank_sys == 'ADP':
        ascending = True  # sorting: want ascending if ADP is selected
    else:
        ascending = False  # sorting: want descending if 2020 pts is selected

    position_df.sort_values(by=[rank_sys], ascending=ascending, inplace=True)  # sort DF
    # add multi-indexing based on index labels provided in pos_df_cols_dict
    position_df.columns = pd.MultiIndex.from_arrays([pos_df_cols_dict[pos][1], position_df.columns])

    # header note on NaN values
    print("\n\n\n"
          "** Note: Players with NaN values for 2020 stats were outside of top 300 players based on 2020 pts. ")
    print("         Players with NaN values for ADP stats were outside of top 300 players based on 2021 ADP projections.\n ")


    print(f"------------------------------------ Individual Statistics for top {n_rows} {pos}s ({league_type})------------------------------------")
    print(position_df.head(n_rows).to_string(index=False))  # display individual player statistics data for top X players.

    print(f"\n------------------------------------- Overall Statistics for top {n_rows} {pos}s ({league_type})-------------------------------------")
    print(position_df.head(n_rows).describe().iloc[1:, :])  # display descriptive statistics for top X players



    final_df_mod = final_df.copy()  # get new copy of our DF
    final_df_mod.reset_index(inplace=True)  # reset index
    final_df_mod.set_index('ID', inplace=True)  # just make ID the index now.

    # define function to map ADP to a a round
    def round_mapper(x):
        return np.ceil(x['RK_ADP']/10)

    # create column giving the round each player is drafted based on ADP
    final_df_mod['Round Drafted'] = final_df_mod.apply(round_mapper, axis=1)

    # filter to position and only do first 16 rounds
    position_df_rds = final_df_mod.loc[(final_df_mod['POS'] == pos) & (final_df_mod['Round Drafted'] <= 16)]

    # use pivot to see how many of that position is taken in each round
    rounds_pivot = position_df_rds.pivot_table(values='ADP', index='League Type', columns='Round Drafted',
                                               aggfunc=np.count_nonzero, fill_value=0)

    # dipslay table and heading
    print(f"\n-----------------------------------Count of {pos}s taken in first 16 rounds (based on ADP)-----------------------------------")
    print(rounds_pivot)