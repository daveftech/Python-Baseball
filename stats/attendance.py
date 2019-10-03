import pandas as pd
import matplotlib.pyplot as plt
from data import games

# Select the attendance data from the games dataframe
attendance = games.loc[(games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year', 'multi3']]

# Rename the columns
attendance.columns = ['year', 'attendance']

# Convert the attendance data to numeric values
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance'])

# Plot the attendance on a bar plot
attendance.plot(x = 'year', y = 'attendance', figsize = (15, 7), kind = 'bar')

# Overwrite the axis labels
plt.xlabel('Year')
plt.ylabel('Attendance')

# Add mean data to the plot
plt.axhline(y = attendance['attendance'].mean(), label = 'Mean', linestyle = '--', color = 'green')

# Render the plot
plt.show()