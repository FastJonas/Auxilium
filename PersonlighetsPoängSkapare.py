#ext = ['Tillgiven', 'pratsam', 'söker sällskap', 'fysiskt aktiv', 'levnadsglad', 'passionerad']
#agr = ['Deltagande', 'tillitsfull', 'generös', 'medgörlig', 'överseenden', 'tålig']
#con = ['Plikttrogen', 'välorganiserad', 'hårt arbetande', 'ambitiös', 'uthållig', 'punktlig']
#emo = ['Lugn', 'stabilt humör', 'tillfreds', 'bekväm', 'okänslig', 'hårdhudad']
#int = ['Föreställningsförmåga', 'kreativ', 'originell', 'föredrar variation', 'nyfiken', 'liberal']

import pandas as pd
import re

def score_word_list(text, word_list):
    pattern = '|'.join(word_list)
    match = re.findall(pattern, text, re.IGNORECASE)
    return len(match)

def add_word_list_scores(df, word_lists):
    for i, word_list in enumerate(word_lists):
        col_name = f"score_wordlist{i+1}"
        df[col_name] = df['description'].apply(lambda x: score_word_list(x, word_list['words']))

    df['total_score'] = df.filter(regex='^score_wordlist').sum(axis=1)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('JobbdataGBGIT.csv')

# Define the lists of words to search for and their corresponding weights
word_lists = [
    {'words': ['tillgiven', 'pratsam', 'sällskap', 'levnadsglad', 'passionerad', 'utåtriktad', 'social', 'energisk', 'självsäker', 'entusiastisk',], 'weight': 0.5},
    {'words': ['deltagande', 'tillitsfull', 'generös', 'medgörlig', 'överseenden', 'tålig', 'vänlig', 'empatisk', 'hjälpsam', 'omtänksam'], 'weight': 0.5},
    {'words': ['plikttrogen', 'organiserad', 'hårt arbetande', 'ambitiös', 'uthållig', 'punktlig', 'pålitlig', 'effektiv', 'målmedveten', 'disciplinerad'], 'weight': 0.5},
    {'words': ['lugn', 'stabil', 'tillfreds', 'bekväm', 'okänslig', 'hårdhudad', 'stress', 'positiv', 'flexibel', 'optimistisk'], 'weight': 0.5},
    {'words': ['föreställningsförmåga', 'kreativ', 'originell', 'föredrar variation', 'nyfiken', 'liberal', 'uppfinningsik', 'visionär'], 'weight': 0.5},
]

# Compute the scores and add them as new columns to the DataFrame
add_word_list_scores(df, word_lists)

# Save the modified DataFrame to a new CSV file
df.to_csv('Personlighetnytttest.csv', index=False)

