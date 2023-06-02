import pandas as pd

# Read the CSV file
data = pd.read_csv('ResultAndScore.csv', encoding='latin-1')

# Get the first column (string column)
first_column = data.iloc[:, 0]

# Create a new DataFrame to store the scaled values
scaled_data = pd.DataFrame()

# Iterate over each numerical column (excluding the first column)
for column in data.columns[1:]:
    # Find the lowest and highest values in the column
    min_value = data[column].min()
    max_value = data[column].max()

    # Scale the values to a range of 1 to 5
    scaled_values = ((data[column] - min_value) / (max_value - min_value)) * 4 + 1

    # Add the scaled values to the new DataFrame
    scaled_data[column] = scaled_values

# Include the first column in the new DataFrame
scaled_data.insert(0, data.columns[0], first_column)

# Save the scaled data to a new CSV file
scaled_data.to_csv('ResultAndScore_scaled.csv', index=False)

print("Scaled data saved to ResultAndScore_scaled.csv")
