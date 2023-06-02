#load pandas, tool for data analysis in Python
import pandas as pd
# read the file called 2022.json that is in the same directory and call it jobtech_dataset
df = pd.read_csv('Hela.csv')

# select the columns to search through by their index numbers
columns_to_search = [24]

# loop through the selected columns
for column in columns_to_search:
    # search for the word "lärare" in the column
    mask = df.iloc[:, column].str.contains('Data/IT', na=False)
    # if any row in the column contains the word "lärare", save the entire row to a new DataFrame
    if mask.any():
        new_df = df.loc[mask]
        # you can then save the new DataFrame to a new CSV file if you want
        new_df.to_csv('HelaDataIT.csv', index=False)
