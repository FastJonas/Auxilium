import pandas as pd

input_file = 'scaled_resultat.csv'
df = pd.read_csv(input_file)

# Extract the 'label' string from the column and overwrite the column with it
df['Value'] = df['Value'].apply(lambda x: eval(x)['label'])

df.to_csv(input_file, index=False)
