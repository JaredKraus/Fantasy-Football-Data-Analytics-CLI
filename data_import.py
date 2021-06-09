import pandas as pd

offense_list = ['WR', 'RB', 'QB', 'TE'] # List containing desired posiitons

# read in data
ppr_2020 = pd.read_csv("./Fantasy Football Datasets/2020 PPR.csv")
std_2020 = pd.read_csv("./Fantasy Football Datasets/2020 Standard.csv")
adp_std_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP Standard.csv")
adp_ppr_2021 = pd.read_csv("./Fantasy Football Datasets/2021 ADP PPR.csv")

# ******* formatting our 4 tables *******
# 2020 PPR
ppr_2020.drop(ppr_2020.columns[[14,15,16,17]], axis=1, inplace=True)  # get rid of defense columns
ppr_2020 = ppr_2020[ppr_2020['POS'].isin(offense_list)]  # filter to only have desired positions
ppr_2020 = ppr_2020.rename({'RK': '2020 RK'}, axis=1)  # rename column
ppr_2020['Passing Pts'] = ppr_2020['PASSING YDS']/25 + ppr_2020['PASSING TD']*4 - ppr_2020['PASSING TD']*2
ppr_2020['Rushing Pts'] = ppr_2020['RUSHING YDS']/10 + ppr_2020['RUSHING TD']*6
ppr_2020['Receiving Pts'] = ppr_2020['RECEIVING YARDS']/10 + ppr_2020['RECEIVING TDS']*6 + ppr_2020['RECEIVING RECEPTIONS']

# 2020 STD
std_2020.drop(std_2020.columns[[14,15,16,17]], axis=1, inplace=True)
std_2020 = std_2020[std_2020['POS'].isin(offense_list)]
std_2020 = std_2020.rename({'RK': '2020 RK'}, axis=1)
std_2020['Passing Pts'] = std_2020['PASSING YDS']/25 + std_2020['PASSING TD']*4 - std_2020['PASSING TD']*2
std_2020['Rushing Pts'] = std_2020['RUSHING YDS']/10 + std_2020['RUSHING TD']*6
std_2020['Receiving Pts'] = std_2020['RECEIVING YARDS']/10 + std_2020['RECEIVING TDS']*6

# ADP STD
adp_std_2021 = adp_std_2021[adp_std_2021['POS'].isin(offense_list)]
adp_std_2021 = adp_std_2021.rename({'RK': 'RK_ADP', 'PTS':'2021 PROJ PTS','POS RK':'2021 PROJ POS RK' }, axis=1)
adp_std_2021.drop(adp_std_2021.columns[[4,5]], axis=1, inplace=True)

# ADP PPR
adp_ppr_2021 = adp_ppr_2021[adp_ppr_2021['POS'].isin(offense_list)]
adp_ppr_2021 = adp_ppr_2021.rename({'RK': 'RK_ADP', 'PTS':'2021 PROJ PTS','POS RK':'2021 PROJ POS RK' }, axis=1)
adp_ppr_2021.drop(adp_ppr_2021.columns[[4,5]], axis=1, inplace=True)


# ******* joining our tables *******
std_merged = pd.merge(adp_std_2021,std_2020, on='ID',how="outer" )
std_merged['League Type'] = 'STD'  # add league type column
ppr_merged = pd.merge(adp_ppr_2021,std_2020, on='ID',how="outer" )
ppr_merged['League Type'] = 'PPR'  # add league type column
final_df = pd.concat([ppr_merged, std_merged])

# combine columns
# fill NA in one column with values from other
final_df.NAME_x.fillna(final_df.NAME_y, inplace=True)
final_df.drop(['NAME_y'], axis=1, inplace=True)
final_df.TEAM_x.fillna(final_df.TEAM_y, inplace=True)
final_df.drop(['TEAM_y'], axis=1, inplace=True)
final_df.POS_x.fillna(final_df.POS_y, inplace=True)
final_df.drop(['POS_y'], axis=1, inplace=True)
final_df = final_df.rename({'NAME_x': 'NAME', 'POS_x': 'POS', 'TEAM_x': 'TEAM', 'GAMES':'2020 GP', 'TOTAL POINTS':'2020 TTL PTS'}, axis=1)

# add indexing
final_df.set_index(['League Type', 'POS' ], inplace=True)
final_df.sort_index(inplace=True)

final_df.to_excel(r".\testExport.xlsx", index=True, header=True)  # export