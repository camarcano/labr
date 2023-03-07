import pandas as pd

"""
# read in LABR.csv as a dataframe
df_labr = pd.read_csv('LABR.csv', usecols=['OVERALL', 'PICK', 'PLAYER', 'MLB', 'POS', 'BID', 'TEAM', 'OWNER'])

# read in IDMAP.csv as a dataframe
df_idmap = pd.read_csv('IDMAP.csv', usecols=['FANTPROSNAME', 'IDFANGRAPHS'])

# merge the two dataframes on the 'PLAYER' and 'FANTPROSNAME' columns
df_merged = pd.merge(df_labr, df_idmap, left_on='PLAYER', right_on='FANTPROSNAME', how='left')

# create the 'PlayerId' column by filling missing values with an empty string
df_merged['PlayerId'] = df_merged['IDFANGRAPHS'].fillna('')

# drop the 'FANTPROSNAME' and 'IDFANGRAPHS' columns
df_general = df_merged.drop(['FANTPROSNAME', 'IDFANGRAPHS'], axis=1)

# ensure the 'PlayerId' column is of type string
df_general['PlayerId'] = df_general['PlayerId'].astype(str)

df_general.to_csv('list2.csv')

"""

# read in list.csv as a dataframe
df_general = pd.read_csv('list.csv')

# read in hitters.csv as a dataframe
df_hitters = pd.read_csv('hitters.csv', usecols=['PlayerId', 'H', 'AB', 'R', 'HR', 'RBI', 'SB'])

# read in pitchers.csv as a dataframe
df_pitchers = pd.read_csv('pitchers.csv', usecols=['PlayerId', 'ER', 'IP', 'H', 'BB', 'W', 'SV', 'SO'])

# merge 'df_general' with 'df_hitters' on 'PlayerId' column
df_merged = pd.merge(df_general, df_hitters, on='PlayerId', how='left')

# replace missing values in 'H', 'AB', 'R', 'HR', 'RBI', and 'SB' columns with 0
df_merged[['H', 'AB', 'R', 'HR', 'RBI', 'SB']] = df_merged[['H', 'AB', 'R', 'HR', 'RBI', 'SB']].fillna(0)

# merge the resulting dataframe with 'df_pitchers' on 'PlayerId' column
df_final = pd.merge(df_merged, df_pitchers, on='PlayerId', how='left')

# replace missing values in 'ER', 'IP', 'H_y', 'BB', 'W', 'SV', and 'SO' columns with 0
df_final[['ER', 'IP', 'H_y', 'BB', 'W', 'SV', 'SO']] = df_final[['ER', 'IP', 'H_y', 'BB', 'W', 'SV', 'SO']].fillna(0)

# ensure all numeric columns are of type float
df_final[['H_x', 'AB', 'R', 'HR', 'RBI', 'SB', 'ER', 'IP', 'H_y', 'BB', 'W', 'SV', 'SO']] = df_final[['H_x', 'AB', 'R', 'HR', 'RBI', 'SB', 'ER', 'IP', 'H_y', 'BB', 'W', 'SV', 'SO']].astype(float)

# ensure 'PlayerId' column is of type string
df_final['PlayerId'] = df_final['PlayerId'].astype(str)

# rename columns to remove '_x' and '_y' suffixes
df_final = df_final.rename(columns={'H_x': 'H', 'H_y': 'H_pitched'})

# assign the new dataframe to 'df_general'
df_general = df_final
df_general[['ER', 'IP', 'H_pitched', 'BB', 'W', 'SV', 'SO']] = df_general[['ER', 'IP', 'H_pitched', 'BB', 'W', 'SV', 'SO']].fillna(0)

# create a new dataframe that groups by the 'TEAM' column and sums all columns
grouped_df = df_general.groupby(['TEAM']).sum()

# save the grouped dataframe to a csv file called 'ranked.csv'
grouped_df.to_csv('ranked.csv', index=True)

grouped_df['AVG'] = grouped_df['H']/grouped_df['AB']
grouped_df['WHIP'] = (grouped_df['BB'] + grouped_df['H_pitched'])/grouped_df['IP']
grouped_df['ERA'] = (grouped_df['ER']*9)/grouped_df['IP']

# add ranking columns for R, HR, RBI, SB, AVG, W, SV, and SO
cols_to_rank = ['R', 'HR', 'RBI', 'SB', 'AVG', 'W', 'SV', 'SO']
for col in cols_to_rank:
    grouped_df[f'{col}_ranked'] = grouped_df[col].rank(method='max', ascending=True)

# add ranking columns for ERA and WHIP
cols_to_rank = ['ERA', 'WHIP']
for col in cols_to_rank:
    grouped_df[f'{col}_ranked'] = grouped_df[col].rank(method='min', ascending=False)

grouped_df = grouped_df.loc[:, [ 'R', 'HR', 'RBI', 'SB', 'AVG', 'W', 'SO', 'SV', 'WHIP', 'ERA','R_ranked', 'HR_ranked', 'RBI_ranked', 'SB_ranked', 'AVG_ranked', 'W_ranked', 'SO_ranked', 'SV_ranked', 'WHIP_ranked', 'ERA_ranked' ]]
cols = ['R_ranked', 'HR_ranked', 'RBI_ranked', 'SB_ranked', 'AVG_ranked', 'W_ranked', 'SO_ranked', 'SV_ranked', 'WHIP_ranked', 'ERA_ranked']

grouped_df['TOTAL'] = grouped_df[cols].sum(axis=1)

temp_cols=grouped_df.columns.tolist()
new_cols=temp_cols[-1:] + temp_cols[1:] 
new_cols=new_cols[0:1] + new_cols[10:20] + new_cols[0:1] + temp_cols[0:1] + new_cols[1:10]
grouped_df=grouped_df[new_cols]

# save the updated dataframe to a new file called 'ranked_ranked.csv'
grouped_df.to_csv('ranked_ranked.csv')