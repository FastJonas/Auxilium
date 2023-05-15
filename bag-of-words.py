from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

df = pd.read_excel('kuggentest_without_stopwords.xlsx')

# Specify the column index to convert to lowercase
column_index = 8  # Assuming column indexing starts from 0

# Get the texts from the specified column
texts = df.iloc[:, column_index].tolist()

# Create an instance of CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the texts to create the bag-of-words representation
vectorized_texts = vectorizer.fit_transform(texts)

# Get the feature names (i.e., the vocabulary)
feature_names = vectorizer.get_feature_names()

# Create a new column to store the vectorized texts
df['VectorizedTexts'] = vectorized_texts.toarray().tolist()

df.to_excel('kuggentest_bag-of-words.xlsx', index=False)
