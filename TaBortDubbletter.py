import pandas as pd

# Läser in den filen
df = pd.read_excel('HelaDataITSplitSvenska.xlsx')

# Tar bort dubbletter med samma text i kolumn 2 
df.drop_duplicates(subset=df.columns[1], keep='first', inplace=True)

# Skapar ny Excel-fil utan dubbletter
df.to_excel('Svenska_ej_dubbletter.xlsx', index=False)










