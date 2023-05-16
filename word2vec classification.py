import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load the Excel file into a DataFrame
df = pd.read_excel('word2vec_file.xlsx')

# Step 2: Prepare the data for classification
X = df.iloc[:, 35:135]  # Assuming embeddings are in columns 1 to 100
y = df['occupation']  # Assuming the label column is named 'label'

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



