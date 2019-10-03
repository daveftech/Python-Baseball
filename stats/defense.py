import pandas as pd
import matplotlib.pyplot as plt
from frames import games, info, events

# Use Query to select the plays that do not have an evnet of NP
plays = games.query("type == 'play' & event != 'NP'")

# Rename the column labels
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

# Use shift() to remove consecutive rows that apply to the same at bat to get player appearances (pa), and reorder the columns
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']]

# Group the player appearances by Year, Game, and Team, then call sizze to get the count, and reset the index
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name = 'PA')

# Set the new indices for the events dataframe
events = events.set_index(['year', 'game_id', 'team', 'event_type'])

# Unstack the events
events = events.unstack().fillna(0).reset_index()

# Use droplevel to remove a level of column headings/labels
events.columns = events.columns.droplevel()

# Rename the column labels
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']

# Remove the axis label by renaming the axis to nothing
events = events.rename_axis(None, axis='columns')

# Merge the events with the plate appearances
events_plus_pa = pd.merge(events, pa, how = 'outer', left_on = ['year', 'game_id', 'team'], right_on = ['year', 'game_id', 'team'])

# Merge the home/away information from the info dataframe
defense = pd.merge(events_plus_pa, info)

# Calculate the DER and add it to defense as a new column
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))

# Convert year to numeric
defense.loc[:, 'year'] = pd.to_numeric(defense['year'])

# Filter out all star games on or after 1978 and filter out the year, defense, and DER columns
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]

# Pivot the table to set it up for plotting.
der = der.pivot(index = 'year', columns = 'defense', values = 'DER')

# Set up a line plot for the DER data and display it
der.plot(x_compat = True, xticks = range(1978, 2018, 4), rot = 45)
plt.show()