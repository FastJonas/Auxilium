import tkinter as tk
import csv

# Creating function to handle the button click event
def submit():
    selected_option = dropdown.get()

    # Get the state of the checkboxes
    checkbox1_state = checkbox1_var.get()
    checkbox2_state = checkbox2_var.get()
    checkbox3_state = checkbox3_var.get()
    checkbox4_state = checkbox4_var.get()
    checkbox5_state = checkbox5_var.get()

    # Öppna läs och fixa tom lista
    with open('jobs.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

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

        # Printar resultatet
        if len(matching_rows) > 0:
            print("Matching rows:")
            for row in matching_rows:
                print(row[0], row[1])
        else:
            print("No matching rows found.")

root = tk.Tk()
root.title("Checkbox and Dropdown Example")

# Create a list of options for the dropdown menu
options = []

# Open the CSV file using the built-in 'open' function
with open('jobs.csv', newline='') as csvfile:
    # Use the 'reader' function from the csv module to parse the CSV file
    reader = csv.reader(csvfile)
    # Loop through each row of the CSV file and append the value in the third column to the list
    for row in reader:
        value = row[2]
        if value not in options:
            options.append(value)

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

# Create a label for the dropdown menu
dropdown_label = tk.Label(root, text="Välj en jobbtitel")

# Create the dropdown menu
dropdown = tk.StringVar(root)
dropdown.set(options[0])
dropdown_menu = tk.OptionMenu(root, dropdown, *options)

# Create a button to submit the form
submit_button = tk.Button(root, text="Submit", command=submit)

# Pack all of the GUI elements onto the root window
checkbox_label.pack()
checkbox1.pack()
checkbox2.pack()
checkbox3.pack()
checkbox4.pack()
checkbox5.pack()
dropdown_label.pack()
dropdown_menu.pack()
submit_button.pack()

root.mainloop()
