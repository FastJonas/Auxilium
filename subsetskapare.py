import pandas as pd

ext = ['Tillgiven', 'pratsam', 'söker sällskap', 'fysiskt aktiv', 'levnadsglad', 'passionerad']
agr = ['Deltagande', 'tillitsfull', 'generös', 'medgörlig', 'överseenden', 'tålig']
con = ['Plikttrogen', 'välorganiserad', 'hårt arbetande', 'ambitiös', 'uthållig', 'punktlig']
emo = ['Lugn', 'stabilt humör', 'tillfreds', 'bekväm', 'okänslig', 'hårdhudad']
int = ['Föreställningsförmåga', 'kreativ', 'originell', 'föredrar variation', 'nyfiken', 'liberal']

databas = ['databasutvecklare']
testare = ['testare']
arkitekt = ['IT-arkitekt']

# read the CSV file into a pandas DataFrame
df = pd.read_csv('JobbdataGBGIT.csv')

# select the columns to search through by their index numbers
columns_to_search = [22]

# loop through the selected columns
for column in columns_to_search:
    # search for the words in the column using a regular expression
    regex = '|'.join(arkitekt)
    mask = df.iloc[:, column].str.contains(regex, na=False, case=False, regex=True)
    
    # if any row in the column contains the words, save the entire row to a new DataFrame
    if mask.any():
        new_df = df.loc[mask]
        # you can then save the new DataFrame to a new Excel file if you want
        new_df.to_excel('kuggentest1.xlsx', index=False)