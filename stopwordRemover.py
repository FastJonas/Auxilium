import nltk
import pandas as pd
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

def remove_swedish_stopwords(text):
    # Tokenize the text into individual words
    words = nltk.word_tokenize(text, language='swedish')

    # Get the set of Swedish stopwords
    swedish_stopwords = set(stopwords.words('swedish'))

    # Remove stopwords from the text
    filtered_words = [word for word in words if word.lower() not in swedish_stopwords]

    # Join the filtered words back into a single text
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

def remove_english_stopwords(text):
    # Tokenize the text into individual words
    words = nltk.word_tokenize(text, language='english')

    # Get the set of Swedish stopwords
    english_stopwords = set(stopwords.words('english'))

    # Remove stopwords from the text
    filtered_words = [word for word in words if word.lower() not in english_stopwords]

    # Join the filtered words back into a single text
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

# Example usage
# Read the Excel file
df = pd.read_excel('kuggentest_lowercase.xlsx')

# Specify the column index to convert to lowercase
column_index = 8  # Assuming column indexing starts from 0

# Convert the text in the specified column to lowercase using the reg_test function
df.iloc[:, column_index] = df.iloc[:, column_index].apply(remove_swedish_stopwords)
df.iloc[:, column_index] = df.iloc[:, column_index].apply(remove_english_stopwords)


df.to_excel('kuggentest_without_stopwords.xlsx', index=False)