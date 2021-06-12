import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_import import final_df
entire_df = final_df.copy()


def PlayerPointsPlot(df, idx, title, col):

    # dict of player positions and the max amount that will be drafted
    # in a league
    offense_dict = {'WR': 50, 'RB': 50, 'QB': 25, 'TE': 25}

    y_size = []

    for k, v in offense_dict.items():

        # sub set of the top v number of values for the k position
        y_val = df.sort_values(
            col, axis=0, ascending=False).loc[idx[:, k, :], idx[col]].iloc[:v]

        plt.plot(range(len(y_val.index)), y_val, linewidth=2,
                 label=k, marker='o', markersize=6)

        y_size.append(y_val.max())

    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, 40, 5))
    plt.yticks(np.arange(0, max(y_size), 20))
    plt.title(col + " in " + title + " League")
    plt.xlabel("Player Rank")
    plt.ylabel("Fantasy Points")
    plt.show()


def GeneralStats(df):
    # 110 is the max number of relevant players drafted in most leagues
    drafted_df = df[df["ADP"] < 111]

    print("\nAverage draft pick of each position\n")
    print(drafted_df.pivot_table(
        "ADP", index='POS', columns='League Type').round(1))

    print("\nEarliest draft pick of each position\n")
    print(drafted_df.pivot_table(
        "ADP", index='POS', columns='League Type', aggfunc=np.min).round(1))

    print("\nTeams with the best Fantasy Players")
    print("Calculated by the sum of (1/ADP)\n")

    print(drafted_df.pivot_table(
        "ADP", index='TEAM', columns='League Type', aggfunc=np.sum).round(1).sort_values("PPR"))

    print(drafted_df.groupby(["League Type", "POS"])
          [["ADP", "2020 RK", "2020 TTL PTS"]].mean().round(1))


def RunGeneralStats(df):

    idx = pd.IndexSlice
    ppr_df = df.loc[idx["PPR", :, :], idx[:]]
    std_df = df.loc[idx["STD", :, :], idx[:]]
    PlayerPointsPlot(ppr_df, idx, "PPR", "2021 PROJ PTS")
    PlayerPointsPlot(std_df, idx, "STD", "2021 PROJ PTS")
    PlayerPointsPlot(ppr_df, idx, "PPR", "2020 TTL PTS")
    PlayerPointsPlot(std_df, idx, "STD", "2020 TTL PTS")
    print("yeet", "yah")
    print("TOMMY B")
    # GeneralStats(df)


RunGeneralStats(entire_df)
