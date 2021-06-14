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
    if pos == "QB":
        optional_col = "Passing Pts"
    else:
        optional_col = "Receiving Pts"

    idx = pd.IndexSlice
    req_cols = ['NAME', 'TTL PTS', 'Rushing Pts', optional_col]
    position_df = final_df[req_cols].loc[idx['PPR', pos], :].copy()
    position_df.dropna(inplace=True)
    position_df['Other Pts'] = position_df['TTL PTS'] - position_df['Rushing Pts'] - position_df[optional_col]
    position_df[f'{pos} Rank'] = position_df['TTL PTS'].rank(ascending=False)
    position_df.sort_values(by='TTL PTS', inplace=True, ascending=False)
    position_df.head(20).plot.bar(x=f'{pos} Rank', y=['Rushing Pts', optional_col, 'Other Pts'], stacked=True)
    plt.title(f"Fantasy {pos} point breakdown")
    plt.ylabel("Fantasy Points")
    plt.show()



