# authors: Graydon Hall and Jared Kraus Group 2
from data_import import final_df
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# required so pycharm prints out pandas dataframes correctly
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 17)


def player_compare(pos):
    """
    function which takes a position as String, and returns a graph showing how different areas of their game
    contribured to their point totals
    :param pos: String position to investigate (ex QB, WR, TE)
    """
    if pos == "QB":
        optional_col = "Passing Pts"  # want passing if it's a QB
    else:
        optional_col = "Receiving Pts"  # otherwise want receiving

    idx = pd.IndexSlice
    req_cols = ['NAME', 'TTL PTS', 'Rushing Pts', optional_col]  # columns to study
    position_df = final_df[req_cols].loc[idx['PPR', pos], :].copy()  # copy of our main DF filterted to ppr and position
    position_df.dropna(inplace=True)  # drop null rows
    position_df['Other Pts'] = position_df['TTL PTS'] - position_df['Rushing Pts'] - position_df[optional_col]  # Calculated column for other points that aren't rushing or passing/receiving
    position_df[f'{pos} Rank'] = position_df['TTL PTS'].rank(ascending=False)  # ranking column based on ttl pts
    position_df.sort_values(by='TTL PTS', inplace=True, ascending=False)  # sort values by ranking
    position_df.head(20).plot.bar(x=f'{pos} Rank', y=['Rushing Pts', optional_col, 'Other Pts'], stacked=True)  # plot data
    plt.title(f"Fantasy {pos} point breakdown (PPR, 2020 Totals)")
    plt.ylabel("Fantasy Points")
    plt.show()



