import pandas as pd

input_file = 'ResultAndScore_scaled.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Extract the 'label' string from the column and overwrite the column with it
df['Job Title'] = df['Job Title'].apply(lambda x: eval(x)['label'])

# Save the modified DataFrame back to the original CSV file
df.to_csv(input_file, index=False)
