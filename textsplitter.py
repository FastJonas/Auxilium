import pandas as pd
import re

def reg_test(text):
    words = str(text).split()  # Split text into individual words
    reg_result = []
    for word in words:
        cleaned_word = re.sub('[^A-Za-z0-9åäöÅÄÖ]+', '', word)  # Remove special characters except for å, ä, and ö
        cleaned_word = cleaned_word.lower()  # Convert the word to lowercase
        reg_result.append(cleaned_word)
    return ' '.join(reg_result)  # Join the cleaned words back into a single text

# Read the Excel file
df = pd.read_excel('kuggentest1.xlsx')

# Specify the column index to convert to lowercase
column_index = 8  # Assuming column indexing starts from 0

# Convert the text in the specified column to lowercase using the reg_test function
df.iloc[:, column_index] = df.iloc[:, column_index].apply(reg_test)

# Save the modified DataFrame back to an Excel file
df.to_excel('kuggentest_lowercase.xlsx', index=False)
