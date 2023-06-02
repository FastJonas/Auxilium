import pandas as pd
import random

# Läs in Excel-filen
df = pd.read_excel('Svenska_ej_dubbletter.xlsx')

# Hämta namnet på den andra kolumnen (jobbtitelkolumnen)
job_title_column = df.columns[2]

# Skapa en tom DataFrame för lagring av resultatet
output_df = pd.DataFrame()

# Loopa igenom de unika värdena för jobbtitlarna
for value in df[job_title_column].unique():
    # Filtrera rader med det aktuella värdet
    filtered_rows = df[df[job_title_column] == value]

    # Kontrollera om det finns minst 250 rader för varje jobbtitel
    if len(filtered_rows) >= 250:
        # Slumpa 250 rader från varje titel
        random_rows = filtered_rows.sample(n=250, random_state=42)

        # Lägg till dom raderna i dataframen
        output_df = pd.concat([output_df, random_rows])

# Skapa en ny Excel-fil
output_df.to_excel('Final250PerTitle.xlsx', index=False)



