#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:04:01 2019

@author: larkink
"""
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load data
# Data source: http://apps.who.int/gho/data/node.main.HIVINCIDENCE?lang=en
new_infections_df = pd.read_csv('data/new_infections.csv')

# Data source: http://apps.who.int/gho/data/view.main.23300
therapy_coverage_df = pd.read_csv('data/therapy_coverage.csv')

# Data source: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?view=map
gdp_df= pd.read_csv('data/gdp.csv')

# Subset data based on column values
country_col = new_infections_df['Country']
regions = new_infections_df.groupby('WHO region')
regions_dict = regions.groups
print(regions.groups.keys())
africa_group = regions.get_group('Africa')
new_infections_df['WHO region'] == 'Europe'
europe_group = new_infections_df[new_infections_df['WHO region'] == 'Europe']

all_hiv_df = therapy_coverage_df[therapy_coverage_df['Indicator'] == 'Estimated number of people (all ages) living with HIV'][['Country', 'Numeric']]
num_therapy_df = therapy_coverage_df[therapy_coverage_df['Indicator'] == 'Reported number of people receiving antiretroviral therapy'][['Country', 'Numeric']]

gdp_df = gdp_df[['Country', '2017']]

# Write df to json
#new_infections_json = new_infections_df.to_json('output/new_infections.json', orient='records')

# Create panel (i.e. a dictionary of dataframes)
# NOTE: Panel is deprecated
#pn = pd.Panel({'item1':africa_group, 'item2':europe_group})
#pn['item1']

# Inspect data
new_infections_df.info()
new_infections_df.describe()
new_infections_df.columns
new_infections_df['Year'].value_counts()
new_infections_df['Display Value'].value_counts()
new_infections_df['WHO region'].unique()

# Set df's index
new_infections_df = new_infections_df.set_index('Country')
new_infections_df.head(2)
new_infections_df.reset_index(inplace = True)
new_infections_df.head(2)

# Create boolean masks based on multiple conditions
mask = (new_infections_df['Indicator'] == 'Number of new HIV infections') & (new_infections_df['Numeric'] > 10000)
high_infections = new_infections_df[mask]
high_infections.count()
high_infections.describe()
high_infections['WHO region'].describe()
high_infections.info()

# Use string methods
high_infections[high_infections.Country.str.contains('Island')]['Country']

# Find nulls
nulls = new_infections_df[new_infections_df.isnull()]
nulls.count()

# Find duplicates
dupe_regions = high_infections[high_infections.duplicated('WHO region') | high_infections.duplicated('WHO region', keep='last')]
dupe_regions.count()

for name, rows in high_infections.groupby('WHO region'):
    print('WHO region: %s, number of rows: %d' % (name, len(rows)))

# Sort df
high_infections.sort_values('WHO region')

# Display subset of df columns
high_infections[['Country', 'WHO region', 'Numeric']]

# Find row by loc
high_infections.loc[high_infections.Country=='Ethiopia']

# Change column value for row
high_infections.loc[high_infections.Country=='Brazil', 'Comments'] = 'Brazil is awesome'

# Subset top ten countries with most new infections
top_infections = high_infections.sort_values('Numeric', ascending=False).iloc[:10][['Country', 'WHO region', 'Numeric']]

# Rename columns
top_infections.rename(columns={'Numeric':'Number of new HIV infections'}, inplace=True)
all_hiv_df.rename(columns={'Numeric':'Estimated number of people (all ages) living with HIV'}, inplace=True)
num_therapy_df.rename(columns={'Numeric':'Reported number of people receiving antiretroviral therapy'}, inplace=True)
gdp_df.rename(columns={'2017':'GDP'}, inplace=True)

# Merge dfs
merged_df = top_infections.merge(all_hiv_df, on='Country').merge(num_therapy_df, on='Country').merge(gdp_df, how='left', on='Country')
merged_df.count()

# Fix missing 2017 GDP value for United Republic of Tanzania
# Data source: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
merged_df.loc[merged_df.Country=='United Republic of Tanzania', 'GDP'] = 52090320325.4736
merged_df.count()

# Visualize data
plt.bar(merged_df.Country, merged_df.GDP)