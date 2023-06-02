import nltk
import pandas as pd
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

def remove_swedish_stopwords(text):
    words = nltk.word_tokenize(text, language='swedish')
    swedish_stopwords = set(stopwords.words('swedish'))
    filtered_words = [word for word in words if word.lower() not in swedish_stopwords]
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

df = pd.read_excel('Final250PerTitle.xlsx')

column_index = 1  

df.iloc[:, column_index] = df.iloc[:, column_index].apply(remove_swedish_stopwords)

df.to_excel('Final250PerTitleWithoutStopwords.xlsx', index=False)
