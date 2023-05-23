import tkinter as tk
import csv
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('scaled_resultat.csv')

ext = 0
agr = 0
con = 0
int = 0
ord = 0

# Initialize a variable to store the maximum value
trait = None


# Quiz function
class Quiz:
    def __init__(self, master):
        self.master = master
        self.questions = ['Jag är kung på fest.', 'Jag har medkänsla för andra.', 'Jag är alltid förberedd.', 'Jag brukar inte bli stressad.', 'Jag har ett stort ordförråd.', 'Jag pratar mycket.', 'Jag är intresserad av människor.', 'Jag bruka hålla ordning runt mig.', 'Jag är oftast avslappnad.', 'Jag har inga problem att förstå abstrakta koncept.']
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

# the trait with the highest score
ext = (quiz.answers[0] + quiz.answers[5]) / 2
agr = (quiz.answers[1] + quiz.answers[6]) / 2
con = (quiz.answers[2] + quiz.answers[7]) / 2
emo = (quiz.answers[3] + quiz.answers[8]) / 2
int = (quiz.answers[4] + quiz.answers[9]) / 2

# Features and target
X = df[['Extraversion', 'Medmänsklighet', 'Samvetsgrannhet', 'Emotionell stabilitet', 'Öppenhet för erfarenhet']]
y = df['Value']

# Create and fit KNN classifier
k = 3  # Number of nearest neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X, y)

# Predict the job title for the input values
input_data = [[ext, agr, con, emo, int]]
nearest_neighbors = knn.kneighbors(input_data, return_distance=False)

# Get the job titles of the nearest neighbors
nearest_job_titles = y.iloc[nearest_neighbors[0]]

# Count the occurrences of each job title and sort them in descending order
job_title_counts = nearest_job_titles.value_counts().sort_values(ascending=False)

# Get the top three job titles with the highest occurrence count
top_three_job_titles = job_title_counts.index[:3]

# Save the best fit as "trait", the second best fit as "trait2", and the third best fit as "trait3"
trait = top_three_job_titles[0]
trait2 = top_three_job_titles[1]
trait3 = top_three_job_titles[2]

print(trait)
print(trait2)
print(trait3)



# Create a function to handle the button click event
def submit():
    # Get the selected option from the dropdown menu
    selected_option = trait

    # Get the state of the checkboxes
    checkbox1_state = checkbox1_var.get()
    checkbox2_state = checkbox2_var.get()
    checkbox3_state = checkbox3_var.get()
    checkbox4_state = checkbox4_var.get()
    checkbox5_state = checkbox5_var.get()

    # Open the CSV file using the built-in 'open' function
    with open('jobs.csv', newline='') as csvfile:
        # Use the 'reader' function from the csv module to parse the CSV file
        reader = csv.reader(csvfile)

        # Create an empty list to store the matching rows
        matching_rows = []

        # Loop through each row of the CSV file and check for matches
        for row in reader:
            # Check if the value in the third column matches the selected option
            if row[2] == selected_option:
                # Check if any of the checkbox values are in the fifth column
                if (checkbox1_state and 'Python' in row[4]) or \
                   (checkbox2_state and 'Azure' in row[4]) or \
                   (checkbox3_state and 'Java' in row[4]) or \
                   (checkbox4_state and 'C#' in row[4]) or \
                   (checkbox5_state and '.NET' in row[4]):
                    # Add the first and fourth columns to the list of matching rows
                    matching_rows.append((row[0], row[3]))

        # Print the matching rows to the console
        if len(matching_rows) > 0:
            print("Matching rows:")
            for row in matching_rows:
                print(row[0], row[1])
        else:
            print("No matching rows found.")


root = tk.Tk()
root.title("Checkbox and Dropdown Example")

# sumbit button 2

# Create variables to hold the state of the checkboxes
checkbox1_var = tk.BooleanVar()
checkbox2_var = tk.BooleanVar()
checkbox3_var = tk.BooleanVar()
checkbox4_var = tk.BooleanVar()
checkbox5_var = tk.BooleanVar()

# Create a label for the checkboxes
checkbox_label = tk.Label(root, text="Vad kan du?")

# Create the checkboxes
checkbox1 = tk.Checkbutton(root, text="Python", variable=checkbox1_var)
checkbox2 = tk.Checkbutton(root, text="Azure", variable=checkbox2_var)
checkbox3 = tk.Checkbutton(root, text="Java", variable=checkbox3_var)
checkbox4 = tk.Checkbutton(root, text="C#", variable=checkbox4_var)
checkbox5 = tk.Checkbutton(root, text=".NET", variable=checkbox5_var)


# Create a button to submit the form
submit_button = tk.Button(root, text="Submit", command=submit)

# Pack all of the GUI elements onto the root window
checkbox_label.pack()
checkbox1.pack()
checkbox2.pack()
checkbox3.pack()
checkbox4.pack()
checkbox5.pack()
submit_button.pack()


root.mainloop()