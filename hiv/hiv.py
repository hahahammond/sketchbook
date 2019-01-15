#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:04:01 2019

@author: larkink
"""
# Import libraries
import pandas as pd
import numpy as np
import matplotlib as plt

# Load data
# Data source: http://apps.who.int/gho/data/node.main.HIVINCIDENCE?lang=en
hiv_df = pd.read_csv('hiv.csv')

# Subsetting data with groupby method
country_col = hiv_df['Country']
regions = hiv_df.groupby('WHO region')
regions_dict = regions.groups
print(regions.groups.keys())
africa_group = regions.get_group('Africa')
hiv_df['WHO region'] == 'Europe'
europe_group = hiv_df[hiv_df['WHO region'] == 'Europe']

# Write df to json
hiv_json = hiv_df.to_json('hiv.json', orient='records')

# Creating a panel (i.e. a dictionary of dataframes)
# NOTE: Panel is deprecated
#pn = pd.Panel({'item1':africa_group, 'item2':europe_group})
#pn['item1']

# Inspecting the data
hiv_df.info()
hiv_df.describe()
hiv_df.columns
hiv_df['Year'].value_counts()
hiv_df['Display Value'].value_counts()
hiv_df['WHO region'].unique()

# Setting the df's index
hiv_df = hiv_df.set_index('Country')
hiv_df.head(2)
hiv_df.reset_index(inplace = True)
hiv_df.head(2)

# Creating boolean masks based on multiple conditions
mask = (hiv_df['Indicator'] == 'Number of new HIV infections') & (hiv_df['Numeric'] > 10000)
high_infections = hiv_df[mask]
high_infections.count()
high_infections.describe()
high_infections['WHO region'].describe()
high_infections.info()

# String methods
high_infections[high_infections.Country.str.contains('Island')]['Country']

# Find nulls
nulls = hiv_df[hiv_df.isnull()]
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
high_infections.sort_values('Numeric', ascending=False).iloc[:10][['Country', 'WHO region', 'Numeric']]