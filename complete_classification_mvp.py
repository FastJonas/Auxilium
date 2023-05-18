import tkinter as tk
import pandas as pd
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


class Quiz:
    def __init__(self, master):
        self.master = master
        self.questions = ['Jag är kung på fest.', 'Jag har medkänsla för andra.', 'Jag är alltid förberedd.', 'Jag brukar inte bli stressad.', 'Jag har ett stort ordförråd.', 'Jag pratar mycket.', 'Jag är intresserad av människor.', 'Jag brukar hålla ordning runt mig.', 'Jag är oftast avslappnad.', 'Jag har inga problem att förstå abstrakta koncept.']
        self.answers = []
        self.current_question = 0
        self.setup_ui()

    def setup_ui(self):
        # Create a label to display the current question
        self.question_label = tk.Label(self.master, text=self.questions[self.current_question])
        self.question_label.pack()

        # Create a scale to allow the user to select their answer
        self.answer_scale = tk.Scale(self.master, from_=1, to=5, orient=tk.HORIZONTAL)
        self.answer_scale.pack()

        # Create a button to submit the answer and move to the next question
        self.next_button = tk.Button(self.master, text='Next', command=self.next_question)
        self.next_button.pack()

    def next_question(self):
        # Record the answer to the current question
        self.answers.append(self.answer_scale.get())

        # Move on to the next question
        self.current_question += 1

        # If there are no more questions, quit the application
        if self.current_question >= len(self.questions):
            self.master.destroy()
        else:
            # Update the question label and reset the answer scale
            self.question_label.config(text=self.questions[self.current_question])
            self.answer_scale.set(1)


root = tk.Tk()
quiz = Quiz(root)
root.mainloop()

# Calculate trait scores and percentages
ext = quiz.answers[0] + quiz.answers[5]
agr = quiz.answers[1] + quiz.answers[6]
con = quiz.answers[2] + quiz.answers[7]
emo = quiz.answers[3] + quiz.answers[8]
inte = quiz.answers[4] + quiz.answers[9]

# Percentages of each trait
ext_percentage = ext / 5
agr_percentage = agr / 5
con_percentage = con / 5
emo_percentage = emo / 5
inte_percentage = inte / 5

# Step 1: Define the percentages for each variable
variable_percentages = [ext_percentage, agr_percentage, con_percentage, emo_percentage, inte_percentage]

# Step 2: Load the Excel file into a DataFrame
df = pd.read_excel('personalitytraits_keywords.xlsx')

# Step 3: Extract the specified percentage of words for each variable from the columns
extracted_words = []
for i, percentage in enumerate(variable_percentages):
    column_name = f'column {i + 1}'  # Replace 'ext{i + 1}' with the actual column name in the Excel file
    num_words = int(len(df) * percentage)
    extracted_words.extend(df[column_name].head(num_words).tolist())

combined_words = ', '.join(extracted_words)

# Create a DataFrame with the combined words in a single cell
output_df = pd.DataFrame({'Combined Words': [combined_words]})

# Step 5: Save the extracted words to a new Excel file
output_df.to_excel('kopplade_traits_keywords.xlsx', index=False)

#_____________________________________________________________________________


# Step 1: Load the Excel file into a DataFrame
df = pd.read_excel('kopplade_traits_keywords.xlsx')

# Step 2: Preprocess the data and tokenize the sentences
sentences = df['Combined Words'].tolist()
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
df.to_excel('kopplade_traits_keywords_word2vec.xlsx', index=False)

#___________________________________________________________________



# Step 1: Load the Excel file into a DataFrame
df = pd.read_excel('testareArkitekt_processed.xlsx')

# Step 2: Prepare the data for classification
X = df.iloc[:, 35:135] 
y = df['occupation'] 

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train a classification model
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions on the test set
y_pred = model.predict(X_test)

# Step 7: Compute the confusion matrix
confusion_mat = confusion_matrix(y_test, y_pred)

# Step 5: Make predictions on the training set
y_train_pred = model.predict(X_train)

# Step 6: Compute the training accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Training Accuracy: {train_accuracy}")

# Step 7: Make predictions on the test set
y_test_pred = model.predict(X_test)

# Step 8: Compute the test accuracy
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f"Test Accuracy: {test_accuracy}")

# Step 8: Visualize the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mat, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.show()

# Step 1: Load the Excel file into a DataFrame
input_data = pd.read_excel('kopplade_traits_keywords_word2vec.xlsx', usecols="B:CW", skiprows=0)

# Step 3: Use the trained model to predict the class label for the input data
input_pred = model.predict(input_data)

# Step 4: Add the predicted labels to the input data DataFrame
input_data['Predicted Label'] = input_pred

# Step 5: Save the results to an Excel file
input_data.to_excel('kopplade_traits_keywords_word2vec_classified.xlsx', index=False)




