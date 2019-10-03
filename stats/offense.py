import pandas as pd
import matplotlib.pyplot as plt
from data import games

# Select the plays from the games data
plays = games[games['type'] == 'play']

# Re-name the column labels
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

# Select the singles, doubles, triples, and home runs
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]

# Convert inning to a numeric
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# Generate the regular expressions for replacing each of the events with the name of the hit type
replacements = {r'^S(.*)': 'single', r'^D(.*)': 'double', r'^T(.*)': 'triple', r'^HR(.*)': 'hr'}

# Replace the event type with the hit type (using the regexes defined above)
hit_type = hits['event'].replace(replacements, regex=True)

# Add the hit_type column to the dataframe
hits = hits.assign(hit_type = hit_type)

# Group the dataframe by inning and hit type, then reset the index to convert it back to a dataframe
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name = 'count')

# Convert hit_type to a categorical variable
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])

# Sort the vaules
hits = hits.sort_values(['inning', 'hit_type'])

# Pivot the table to configure it for plotting
hits = hits.pivot(index = 'inning', columns = 'hit_type', values = 'count')

# Configure the stacked bar plot and show
hits.plot.bar(stacked=True)
plt.show()