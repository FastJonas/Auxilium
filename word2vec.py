import pandas as pd
from gensim.models import Word2Vec
import numpy as np

# Step 1: Load the Excel file into a DataFrame
df = pd.read_excel('bajs2.xlsx')

# Step 2: Preprocess the data and tokenize the sentences
sentences = df['description'].tolist()
tokenized_sentences = [sentence.split() for sentence in sentences]

# Step 3: Train the Word2Vec model
model = Word2Vec(tokenized_sentences, min_count=1)

# Step 4: Get the Word2Vec embeddings for each sentence
sentence_embeddings = []
for sentence in tokenized_sentences:
    embeddings = [model.wv[word] for word in sentence if word in model.wv]
    if embeddings:
        sentence_embeddings.append(np.mean(embeddings, axis=0))
    else:
        sentence_embeddings.append([])

# Step 5: Add the sentence embeddings as new columns in the DataFrame
for i in range(len(sentence_embeddings[0])):
    df[f'embedding_{i+1}'] = [emb[i] if len(emb) > 0 else np.nan for emb in sentence_embeddings]

# Step 6: Save the modified DataFrame to a new Excel file
df.to_excel('word2vec_file2.xlsx', index=False)
