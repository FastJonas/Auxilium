import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import csv

df = pd.read_csv('resultAndScore_scaled.csv')

ext = 0
agr = 0
con = 0
int = 0
ord = 0
trait = None


class Quiz:
    def __init__(self, master):
        self.master = master
        self.questions = ['Jag är kung på fest.', 'Jag har medkänsla för andra.', 'Jag är alltid förberedd.',
                          'Jag brukar inte bli stressad.', 'Jag har ett stort ordförråd.', 'Jag pratar mycket.',
                          'Jag är intresserad av människor.', 'Jag bruka hålla ordning runt mig.',
                          'Jag är oftast avslappnad.', 'Jag har inga problem att förstå abstrakta koncept.']
        self.answers = []
        self.current_question = 0
        self.checkbox1_var = tk.BooleanVar()
        self.checkbox2_var = tk.BooleanVar()
        self.checkbox3_var = tk.BooleanVar()
        self.checkbox4_var = tk.BooleanVar()
        self.checkbox5_var = tk.BooleanVar()
        self.setup_ui()

    def setup_ui(self):
        # Configure the window settings
        self.master.configure(bg='#f9f9f9')
        self.master.title('Auxillium')

        # Create a frame to hold the entry page content
        entry_frame = tk.Frame(self.master, bg='#f9f9f9')
        entry_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)

        instructions_label = tk.Label(entry_frame, text='Lär känna din personlighetstyp och hitta \npassande jobbroller genom att besvara 50 frågor.\nTestet tar ungefär fem till tio minuter att genomföra.\n\nVänligen betygsätt följande påståenden på en skala från \n1 till 5, där 1 är "Håller inte med alls" och 5 är "Håller med helt".', font=('Arial', 12), background='#f9f9f9', foreground='#333333')
        instructions_label.pack(pady=0)
        instructions_label2 = tk.Label(entry_frame, text='\nKlicka på Start för att påbörja testet.',font=('Arial', 12),
                                      background='#f9f9f9', foreground='#333333')
        instructions_label2.pack(pady=0)

        start_button = ttk.Button(entry_frame, text='Start', command=self.start_quiz)
        start_button.pack(pady=0)

        aux_label = tk.Label(entry_frame, text="Auxillium", font=('Arial', 18, 'bold'), bg='#f9f9f9', fg='#555555')
        aux_label.place(relx=0.625, rely=0.85, anchor=tk.NE)

    def start_quiz(self):
        # Create a new frame
        content_frame = tk.Frame(self.master, bg='#f9f9f9')
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)

        # Create a label to display the current question
        self.question_label = ttk.Label(content_frame, text=self.questions[self.current_question], font=('Arial', 16),
                                        background='#f9f9f9', foreground='#333333')
        self.question_label.pack(pady=40)

        # Create a frame to hold the scale and its labels
        scale_frame = tk.Frame(content_frame, bg='#f9f9f9')
        scale_frame.pack()

        # Create labels for the scale numbers with spacing
        for i in range(1, 6):
            label = tk.Label(scale_frame, text=str(i), font=('Arial', 12), bg='#f9f9f9', fg='#555555')
            label.pack(side=tk.LEFT, padx=40)

        # Create a scale to allow the user to select their answer
        self.answer_scale = ttk.Scale(content_frame, from_=1, to=5, orient=tk.HORIZONTAL, length=400, style='TScale')
        self.answer_scale.pack()

        next_button = ttk.Button(content_frame, text='Nästa', command=self.next_question)
        next_button.pack(pady=30)

    def next_question(self):
        self.answers.append(self.answer_scale.get())

        self.current_question += 1

        # If there are no more questions, close the window
        if self.current_question >= len(self.questions):
            self.show_results(self.answers)

        else:
            # Update the question label and reset the answer scale
            self.question_label.config(text=self.questions[self.current_question])
            self.answer_scale.set(1)

    def show_results(self,answers):
        self.answers = answers

        ext = (quiz.answers[0] + quiz.answers[5]) / 2
        agr = (quiz.answers[1] + quiz.answers[6]) / 2
        con = (quiz.answers[2] + quiz.answers[7]) / 2
        emo = (quiz.answers[3] + quiz.answers[8]) / 2
        int = (quiz.answers[4] + quiz.answers[9]) / 2

        # Features and target
        X = df[['Extraversion', 'Medmänsklighet', 'Samvetsgrannhet', 'Emotionell stabilitet', 'Öppenhet för erfarenhet']]
        y = df['Job Title']

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

        trait = top_three_job_titles[0]
        trait2 = top_three_job_titles[1]
        trait3 = top_three_job_titles[2]

        for widget in self.master.winfo_children():
            widget.destroy()

        # Display the results to the user
        results_text = f"Personlighetstest avklarat!\n\nDina bäst passande jobbroller:\n\n1: {trait} \n2: {trait2}\n3: {trait3}"
        results_label = ttk.Label(self.master, text=results_text, font=('Arial', 16),
                                background='#f9f9f9', foreground='#333333', anchor='center', justify='center')
        results_label.pack(pady=40)

        close_button = ttk.Button(self.master, text='Nästa', command=lambda: self.submit(trait, trait2, trait3))
        close_button.pack(pady=10)

        aux_label = tk.Label(self.master, text="Auxillium", font=('Arial', 18, 'bold'), bg='#f9f9f9', fg='#555555')
        aux_label.place(relx=0.6, rely=0.85, anchor=tk.NE)
    

    def submit(self, trait, trait2, trait3):
        self.trait = trait
        self.trait2 = trait2
        self.trait3 = trait3

        for widget in self.master.winfo_children():
            widget.destroy()

        # Create the checkboxes and submit button
        checkbox_label = tk.Label(self.master, text="Vilka kompetenser har du?",bg="#f9f9f9")
        checkbox1 = tk.Checkbutton(self.master, text="Python", variable=self.checkbox1_var, bg="#f9f9f9")
        checkbox2 = tk.Checkbutton(self.master, text="Azure", variable=self.checkbox2_var, bg="#f9f9f9")
        checkbox3 = tk.Checkbutton(self.master, text="Java", variable=self.checkbox3_var, bg="#f9f9f9")
        checkbox4 = tk.Checkbutton(self.master, text="C#", variable=self.checkbox4_var, bg="#f9f9f9")
        checkbox5 = tk.Checkbutton(self.master, text=".NET", variable=self.checkbox5_var, bg="#f9f9f9")
        submit_button = ttk.Button(self.master, text="Submit", command=lambda: self.display_matching_rows(trait, trait2, trait3))

        # Pack all of the GUI elements onto the root window
        checkbox_label.pack()
        checkbox1.pack()
        checkbox2.pack()
        checkbox3.pack()
        checkbox4.pack()
        checkbox5.pack()
        submit_button.pack()

    def display_matching_rows(self, trait, trait2, trait3):
        # Get the state of the checkboxes
        checkbox1_state = self.checkbox1_var.get()
        checkbox2_state = self.checkbox2_var.get()
        checkbox3_state = self.checkbox3_var.get()
        checkbox4_state = self.checkbox4_var.get()
        checkbox5_state = self.checkbox5_var.get()

        with open('jobs.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)

            matching_rows = []

            for row in reader:
                if row[2] == self.trait:
                    # Check if any of the checkbox values are in the fifth column
                    if (checkbox1_state and 'Python' in row[4]) or \
                            (checkbox2_state and 'Azure' in row[4]) or \
                            (checkbox3_state and 'Java' in row[4]) or \
                            (checkbox4_state and 'C#' in row[4]) or \
                            (checkbox5_state and '.NET' in row[4]):
                        # Add the first and fourth columns to the list of matching rows
                        matching_rows.append((row[0], row[3]))

            for widget in self.master.winfo_children():
                widget.destroy()

            results_label = ttk.Label(self.master, font=('Arial', 10), background='#f9f9f9', foreground='#333333')
            results_label.pack(pady=40)

            if len(matching_rows) > 0:
                results_text = " Matchande jobbannonser:\n"
                for row in matching_rows:
                    results_text += f"{row[0]}, Arbetsformedlingen.se{row[1]}\n"
            else:
                results_text = "Inga matchande jobbannonser hittades."

            results_label.config(text=results_text)



root = tk.Tk()
root.geometry('800x500')
quiz = Quiz(root)
root.mainloop()



