#python 3.11 on windows, have to install pandas and matplotlib before execution
import pandas as pd
import matplotlib.pyplot as plt

#read excel file and import data in a global data frame that contains a distinct data frame for each sheet
df_stats = pd.read_excel('stats.xlsx', sheet_name=None)

#build index Season-Position to get the scored points for a race
df_stats['results']['Season-Position'] = df_stats['results']['Season'].map(str) + '-' + df_stats['results']['Position'].map(str)
df_stats['points']['Season-Position'] = df_stats['points']['Season'].map(str) + '-' + df_stats['points']['Position'].map(str)
df_stats['points'] = df_stats['points'].set_index('Season-Position')
df_stats['results'] = df_stats['results'].merge(df_stats['points'],how='left',on='Season-Position' ,suffixes=("", "_y"),)

#add x2 points multiplicatoir for the final race of each season
df_stats['results'].loc[df_stats['results']['Final Race'] == 1, 'Points'] = df_stats['results']['Points'] * 2

#add 2 points for the driver who did the fastest lap of the race
df_stats['results'].loc[df_stats['results']['Fastest Lap'] == 1, 'Points'] = df_stats['results']['Points'] + 2

#print the data frame results
print(df_stats['results'])

#build a pivot table for drivers
pt_stats_results = pd.pivot_table(df_stats['results'],index=['Driver'],values='Points', aggfunc = 'sum', columns=['Season'], margins=True)
print(pt_stats_results)

#build a pivot table for teams
pt_stats_results = pd.pivot_table(df_stats['results'],index=['Team'],values='Points', aggfunc = 'sum', columns=['Season'], margins=True)
print(pt_stats_results)