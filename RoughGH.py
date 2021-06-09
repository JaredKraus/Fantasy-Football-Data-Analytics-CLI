import pandas as pd


def format_2020_df(df):
    # filter out defensive positions
    # get rid of uncecessary columns
    # calculate extra columns
    pass

def format_adp_df():
    # get rid of extra columns
    pass


# import the data as dataframes
ppr_2020 = pd.read_csv("./Fantasy Football Datasets/2020 PPR.csv")
std_2020 = pd.read_csv("./Fantasy Football Datasets/2020 Standard.csv")
adp_std_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP Standard.csv")
adp_ppr_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP PPR.csv")


# print(ppr_2020)
# print(std_2020)
# print(adp_std_2021)
# print(adp_ppr_2021)