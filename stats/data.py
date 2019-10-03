import os
import glob
import pandas as pd

# Load the game files
game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))

# curr_dir = os.getcwd()
# path = os.path.join(curr_dir, 'games', '*.EVE')
# game_files = glob.glob(path)

game_files.sort()

game_frames = []

# Create the data frames from the file data
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

games = pd.concat(game_frames)

# Clean up rows with '??' in the multi5 column by replacing '??' with ''
games.loc[games['multi5'] == '??',  'multi5'] = ""

# Extract the identifiers from the multi2 column
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')

# Fill in any of the unmatched identifiers using forward fill
identifiers = identifiers.fillna(method='ffill')

# Rename the columns
identifiers.columns = ['game_id', 'year']

# Concatenate the identifiers to the games dataframe
games = pd.concat([games, identifiers], axis=1, sort=False)

# Fill all null values in the dataframe with an empty space
games = games.fillna(' ')

# Change event type to a categorical type (as it can only be a finite set of values)
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

# Print the top of the dataframe to check the data
print(games.head())