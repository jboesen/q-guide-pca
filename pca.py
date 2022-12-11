# this is an earlier version
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sys

# read in the data
df = pd.read_excel('q-guide-fall.xlsx')

import importlib
importlib.reload(pd)

# drop column web-scraper-order
df = df.drop(['web-scraper-order', 'web-scraper-start-url'], axis=1)

formatted_df = pd.DataFrame(columns=[
  'name',
  'class_size',
  'rsp_ratio',
  'course_overall',
  'materials',
  'assignments',
  'feedback',
  'section',
  'instructor',
  'lectures',
  'accessible',
  'enthusiasm',
  'discussion',
  'feedback',
  'timely', 
  'time_mean',
  'time_std',
  'time_median',
  'recommend',
])
def formatting_fnc(group):
  # a select number of courses have no instructor ratings; we exclude them
  if group['Instructor Mean'].dropna().shape[0] == 0:
    return pd.DataFrame()
  return_df = pd.DataFrame(columns=['reason'], index=[0])
  # select from group row where raters = 'Response Ratio'
  class_size = float(group[group['Raters'] == 'Invited']['Students'].iloc[0])
  return_df['class_size'] = class_size ** -1 if class_size > 0 else 0
  return_df['rsp_ratio'] = float(group[group['Raters'] == 'Response Ratio']['Students'].iloc[0][0:-1])/100
  # General feedback
  return_df['course_overall'] = float(group['Course Mean'].dropna().iloc[0]) / 5
  return_df['materials'] = float(group['Course Mean'].dropna().iloc[1]) / 5
  return_df['assignments'] = float(group['Course Mean'].dropna().iloc[2]) / 5
  return_df['feedback'] = float(group['Course Mean'].dropna().iloc[3]) / 5
  return_df['section'] = float(group['Course Mean'].dropna().iloc[4]) / 5
  # Instructor
  return_df['instructor'] = float(group['Instructor Mean'].dropna().iloc[0]) / 5
  return_df['lectures'] = float(group['Instructor Mean'].dropna().iloc[1]) / 5
  return_df['accessible'] = float(group['Instructor Mean'].dropna().iloc[2]) / 5
  return_df['enthusiasm'] = float(group['Instructor Mean'].dropna().iloc[3]) / 5
  return_df['discussion'] = float(group['Instructor Mean'].dropna().iloc[4]) / 5
  return_df['feedback'] = float(group['Instructor Mean'].dropna().iloc[5]) / 5
  return_df['timely'] = float(group['Instructor Mean'].dropna().iloc[6]) / 5
  # time
  # parse a string into float
  time_mean = float(group[group['Statistics'] == 'Mean']['Value'].iloc[0]) * 7.5
  return_df['time_mean'] = time_mean ** -1 if time_mean > 0 else 1
  time_std = float(group[group['Statistics'] == 'Standard Deviation']['Value'].iloc[0]) * 7.5
  return_df['time_std'] = time_std ** -1 if time_std > 0 else 1
  time_med = float(group[group['Statistics'] == 'Median']['Value'].iloc[0]) * 7.5
  return_df['time_median'] = time_med ** -1 if time_med > 0 else 1
  recommend_rows = group[df['Options'].str.contains('Recommend', na=False)]
  # change recommend column datatype to object
  return_df.at[0, 'recommend'] = recommend_rows['Percentage'].str.strip('%').astype('float').div(100).mean() / 5
  return_df['elective'] = group[group['Options'] == 'Elective']['Count'].iloc[0]/class_size
  return_df['concentration'] = group[group['Options'] == 'Concentration or Department Requirement']['Count'].iloc[0]/class_size
  return_df['secondary'] = group[group['Options'] == 'Secondary Field or Language Citation Requirement']['Count'].iloc[0]/class_size
  # return_df.at[0, 'reason'] = tuple([x/7.5 for x in return_df.at[0, 'reason']])
  return return_df

# group by course name column
grouped = df.groupby('coursename')
print('ballin')
formatted_df = grouped.apply(formatting_fnc)

# drop name columns
# formatted_df = formatted_df.drop(['name'], axis=1)
# convert index to numbers
formatted_df = formatted_df.reset_index(drop=True)
# drop all zero rows
formatted_df = formatted_df[(formatted_df.T != 0).any()]

# export formatted_df to excel
formatted_df.to_excel('formatted.xlsx')

# drop columns reason
formatted_df = formatted_df.drop(['reason'], axis=1)

# compress with pca
pca = PCA(n_components=2)
data = pca.fit_transform(formatted_df)

# plot the data
plt.scatter(data[:,0], data[:,1])
plt.show()
