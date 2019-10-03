import pandas as pd
import matplotlib.pyplot as plt
from data import games

# Select plays from the games data
plays = games[games['type'] == 'play']

# Select strike outs from the plays
strike_outs = plays[plays['event'].str.contains('K')]

# Create a group by object, grouping the plays by year and game
strike_outs = strike_outs.groupby(['year', 'game_id']).size()

# Convert the group by object back to a dataframe by resetting the index
strike_outs = strike_outs.reset_index(name='strike_outs')

# Apply the pd.to_numeric() function to multiple columns by selecting those columns and using apply()
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)

# Create a scatterplot of the strikeout data and update the label on the legend
strike_outs.plot(x = 'year', y = 'strike_outs', kind = 'scatter').legend(['Strike Outs'])

# Render the plot
plt.show()