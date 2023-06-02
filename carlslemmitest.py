#se till att ha pandas spacy och den svenska språkmodellen

import pandas as pd
import spacy

# Smäll in sv_core_news_sm
nlp = spacy.load('sv_core_news_sm')

def lemmatize_text(text):
    doc = nlp(text)
    lemmatized_words = [token.lemma_ for token in doc]
    lemmatized_text = ' '.join(lemmatized_words)
    return lemmatized_text

input_file = 'bajs3.xlsx'
output_file = 'output.xlsx'

df = pd.read_excel(input_file)

# description ligger i column 8
text_column_index = 8

# Lemmatizing
df.iloc[:, text_column_index] = df.iloc[:, text_column_index].apply(lemmatize_text)

df.to_excel(output_file, index=False)

print("Färdigt :D")
