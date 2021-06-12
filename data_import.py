import pandas as pd

offense_list = ['WR', 'RB', 'QB', 'TE'] # List containing desired posiitons

# read in the CSVs.
ppr_2020 = pd.read_csv("./Fantasy Football Datasets/2020 PPR.csv")
std_2020 = pd.read_csv("./Fantasy Football Datasets/2020 Standard.csv")
adp_std_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP Standard.csv")
adp_ppr_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP PPR.csv")

# ******* formatting our 4 tables *******

# 2020 PPR Dataframe
ppr_2020.drop(ppr_2020.columns[[14,15,16,17]], axis=1, inplace=True)  # get rid of defense columns
ppr_2020 = ppr_2020[ppr_2020['POS'].isin(offense_list)]  # filter to only have desired positions
# calculated columns for fantasy points from passing, rushin,g and receiving
ppr_2020['Passing Pts'] = ppr_2020['PASSING YDS']/25 + ppr_2020['PASSING TD']*4 - ppr_2020['PASSING TD']*2
ppr_2020['Rushing Pts'] = ppr_2020['RUSHING YDS']/10 + ppr_2020['RUSHING TD']*6
ppr_2020['Receiving Pts'] = ppr_2020['RECEIVING YARDS']/10 + ppr_2020['RECEIVING TDS']*6 + ppr_2020['RECEIVING RECEPTIONS']

# 2020 STD Dataframe
std_2020.drop(std_2020.columns[[14,15,16,17]], axis=1, inplace=True)  # get rid of defense columns
std_2020 = std_2020[std_2020['POS'].isin(offense_list)]  # filter to desired positions
# calculated columns for fantasy points from passing, rushin,g and receiving
std_2020['Passing Pts'] = std_2020['PASSING YDS']/25 + std_2020['PASSING TD']*4 - std_2020['PASSING TD']*2
std_2020['Rushing Pts'] = std_2020['RUSHING YDS']/10 + std_2020['RUSHING TD']*6
std_2020['Receiving Pts'] = std_2020['RECEIVING YARDS']/10 + std_2020['RECEIVING TDS']*6

# ADP STD  Dataframe
adp_std_2021 = adp_std_2021[adp_std_2021['POS'].isin(offense_list)]  # filter to desired positions
adp_std_2021 = adp_std_2021.rename({'RK': 'RK_ADP', 'PTS':'PROJ PTS','POS RK':'PROJ POS RK' }, axis=1)  # rename columns
adp_std_2021.drop(adp_std_2021.columns[[4,5]], axis=1, inplace=True)  # drop irrelivant columns

# ADP PPR  Dataframe
adp_ppr_2021 = adp_ppr_2021[adp_ppr_2021['POS'].isin(offense_list)]  # filter to desired positions
adp_ppr_2021 = adp_ppr_2021.rename({'RK': 'RK_ADP', 'PTS':'PROJ PTS','POS RK':'PROJ POS RK'}, axis=1)  # rename columns
adp_ppr_2021.drop(adp_ppr_2021.columns[[4,5]], axis=1, inplace=True)  # drop irrelivant columns


# ******* joining our tables *******
# merge standard league 2020 with standard league adp projections
std_merged = pd.merge(adp_std_2021,std_2020, on='ID',how="outer" )  # Outer join based on player ID
std_merged['League Type'] = 'STD'  # add league type column

# merge ppr league 2020 with ppr league adp projections
ppr_merged = pd.merge(adp_ppr_2021,ppr_2020, on='ID',how="outer" )  # Outer join based on player ID
ppr_merged['League Type'] = 'PPR'  # add league type column
final_df = pd.concat([ppr_merged, std_merged])  # add tables on top of one another.

# combine columns
# fill NA values in one table with corresponding column in other table
# then delete un-needed column, and rename other one.
#Note: Players with NaN values for 2020 stats were outside of top 300 players based on 2020 pts.
#      Players with NaN values for ADP stats were outside of top 300 players based on 2021 ADP projections.
final_df.NAME_x.fillna(final_df.NAME_y, inplace=True)  # fill NaN values
final_df.drop(['NAME_y'], axis=1, inplace=True)  # drop redundant column
final_df.TEAM_x.fillna(final_df.TEAM_y, inplace=True)  # fill NaN values
final_df.drop(['TEAM_y'], axis=1, inplace=True)  # drop redundant column
final_df.POS_x.fillna(final_df.POS_y, inplace=True)  # fill NaN values
final_df.drop(['POS_y'], axis=1, inplace=True)  # drop redundant column
final_df = final_df.rename({'NAME_x': 'NAME', 'POS_x': 'POS', 'TEAM_x': 'TEAM', 'GAMES':'GP', 'TOTAL POINTS':'TTL PTS'}, axis=1)  # rename


final_df.set_index(['League Type', 'POS', 'ID'], inplace=True)  # add multi-level indexing
final_df.sort_index(inplace=True)  # sort values

final_df.to_excel(r".\testExport.xlsx", index=True, header=True)  # export final dataframe.