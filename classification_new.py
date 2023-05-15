from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix


df = pd.read_excel('kuggentest_TF-IDF.xlsx')

bag_to_words_col_num = 35

X = df.iloc[:, bag_to_words_col_num].apply(lambda x: ' '.join(x.strip('[]').split(',')))
y = df.iloc[:, 22]  # Assuming the label column is the last one

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

# Create an instance of CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the training data to create the bag-of-words representation
X_train_vectorized = vectorizer.fit_transform(X_train)

# Transform the test data using the fitted vectorizer
X_test_vectorized = vectorizer.transform(X_test)

# Initialize and train the decision tree classifier
DT = RandomForestClassifier(random_state=0).fit(X_train_vectorized, y_train)

# Accuracy on the train set
acc_train = DT.score(X_train_vectorized, y_train)
# Accuracy on the test set
acc_test = DT.score(X_test_vectorized, y_test)

# Predict labels for the test set
y_pred = DT.predict(X_test_vectorized)

# Compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, y_pred)

# Create a DataFrame for the confusion matrix with labels
confusion_df = pd.DataFrame(confusion_mtx, index=DT.classes_, columns=DT.classes_)

# Plot the confusion matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_df, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

print('The accuracy on the train set is {}'.format(acc_train))
print('The accuracy on the test set is {}'.format(acc_test))


