import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_import import final_df
entire_df = final_df.copy()


def PlayerPointsPlot(df, idx, leauge, year, col):
    """
    Plots the top players in each position by the given col

    Args:
        df (pandas.core.frame.DataFrame): A pandas dataframe of fantasy players
        idx (pandas.core.indexing._IndexSlice): for indexslicing of a pandas df
        leauge (String): The type of league for the title
        year (String): The year the of data for the title
        col (float): the column that will be used for the y points
    """

    # dict of player positions and the max amount that will be drafted
    # in a league
    offense_dict = {'WR': 50, 'RB': 50, 'QB': 25, 'TE': 25}

    y_size = []  # to get the max for the y axis ticks

    # loop through key/value in offense_dict
    for k, v in offense_dict.items():

        # sub df of the top v number of values for the k position sorted by the col given
        # this will be the y values of the plot
        y_val = df.sort_values(
            col, axis=0, ascending=False).loc[idx[:, k, :], idx[col]].iloc[:v]
        # plot of y_values against index values (0 to number of rows)
        plt.plot(range(len(y_val.index)), y_val, linewidth=2,
                 label=k, marker='o', markersize=6)

        # adds max col value in the sub df to y_size
        y_size.append(y_val.max())

    plt.legend()  # add legend to plot
    plt.grid()  # add grid to plot
    plt.xticks(np.arange(0, 50, 5))  # x axis goes to 50 and steps by 5
    # gp to largest value and step by 20
    plt.yticks(np.arange(0, max(y_size), 20))
    plt.title(year + " " + col + " in " + leauge + " League")  # add title
    plt.xlabel("Player Rank")  # add x axis label
    plt.ylabel("Fantasy Points")  # add y axis label
    print("Printing " + year + " " + col + " in " + leauge + " League graph.")
    plt.show()  # show plot


def GeneralStats(df):
    """
    Prints out 2020 averages, 2021 projection averages,
    earlist draft by postion, and team fantasy points
    for the given df

    Args:
        df (pandas.core.frame.DataFrame): A pandas dataframe of fantasy players
    """
    # 110 is the max number of relevant players drafted in most leagues
    drafted_df = df[df["ADP"] < 111]

    # 2020 ADP, Rank and total point mean averages rounded to 1 decimal place
    print("\n2020 Mean Averages\n")
    print(drafted_df.groupby(["League Type", "POS"])
          [["ADP", "RK", "TTL PTS"]].mean().round(1))

    # 2021 projected ADP and total point mean averages rounded to 1 decimal place
    print("\n2021 Projections Mean Average\n")
    print(drafted_df.groupby(["League Type", "POS"])
          [["RK_ADP", "PROJ PTS"]].mean().round(1))

    # earliest (min) ADP of a position
    print("\nEarliest draft pick of each position in 2020\n")
    print(drafted_df.pivot_table(
        "ADP", index='POS', columns='League Type', aggfunc=np.min).round(1))

    # sum of 2020 fantasy points for each team
    print("\nTeams with the most Fantasy Points in 2020\n")
    print(drafted_df.pivot_table(
        "PROJ PTS", index='TEAM', columns='League Type', aggfunc=np.sum).round(1).sort_values("PPR", ascending=False))


def RunGeneralStats(df):
    """
    Run PlayerPointsPlot() function for each year and league (4 times)
    Run GeneralStats()

    Args:
        df (pandas.core.frame.DataFrame): Full df of fantasy player data
    """

    idx = pd.IndexSlice  # for indexslicing
    ppr_df = df.loc[idx["PPR", :, :], idx[:]]
    std_df = df.loc[idx["STD", :, :], idx[:]]
    PlayerPointsPlot(ppr_df, idx, "PPR", "2021",
                     "PROJ PTS")  # 2021 proj PPR plot
    PlayerPointsPlot(std_df, idx, "STD", "2021",
                     "PROJ PTS")  # 2021 proj STD plot
    PlayerPointsPlot(ppr_df, idx, "PPR", "2020",
                     "TTL PTS")  # 2020 points PPR plot
    PlayerPointsPlot(std_df, idx, "STD", "2020",
                     "TTL PTS")  # 2020 points STD plot
    GeneralStats(df)


RunGeneralStats(entire_df)
