import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import csv

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('scaled_resultat.csv')

# Input values
red_input = 1
green_input = 1
blue_input = 1
yellow_input = 1
purple_input = 1

# Features and target
X = df[['Extraversion', 'Medmänsklighet', 'Samvetsgrannhet', 'Emotionell stabilitet', 'Öppenhet för erfarenhet']]
y = df['Value']

# Create and fit KNN classifier
k = 1  # Number of nearest neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X, y)


output_counts = {}

for A in range(1, 6):
    red_input = A
    for B in range(1, 6):
        green_input = B
        for C in range(1, 6):
            blue_input = C
            for D in range(1, 6):
                yellow_input = D
                for E in range(1, 6):
                    purple_input = E
                    # Predict the job title for the input values
                    input_data = [[red_input, green_input, blue_input, yellow_input, purple_input]]
                    nearest_neighbors = knn.kneighbors(input_data, return_distance=False)

                    # Get the job titles of the nearest neighbors
                    nearest_job_titles = y.iloc[nearest_neighbors[0]]

                    # Find the most common job title among the nearest neighbors
                    output = nearest_job_titles.mode()[0]

                    if output in output_counts:
                        output_counts[output] += 1
                    else:
                        output_counts[output] = 1

with open('provaelvin.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Occupation', 'Count'])
    for output, count in output_counts.items():
        writer.writerow([output, count])