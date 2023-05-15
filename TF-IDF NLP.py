import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Read the Excel file
df = pd.read_excel('kuggentest_without_stopwords.xlsx')

# Extract all rows from column 9
column_data = df.iloc[:, 8].tolist()

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Compute the TF-IDF features
tfidf_matrix = vectorizer.fit_transform(column_data)

# Convert the TF-IDF matrix to numerical values
tfidf_matrix_numerical = tfidf_matrix.toarray()

# Create a new column in the DataFrame with the numerical values
df['TF-IDF Numerical'] = tfidf_matrix_numerical.tolist()

df.to_excel('kuggentest_TF-IDF.xlsx', index=False)
