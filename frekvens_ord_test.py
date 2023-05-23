import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
from nltk.stem import SnowballStemmer
import csv

personlighetstyper = {
    "Öppenhet för erfarenhet": ["kreativ", "intellektuell", "nyfiken", "konstnärlig", "uppfinning",
                                "reflekterande", "fantasifull", "visionär",
                                "innovativ", "intuitiv", "uttrycksfull",
                                "tankeväckande", "analytisk", "komplex", "intresserad"],
    "Samvetsgrannhet": ["organiserad", "ansvarsfull", "plikttrogen", "effektiv",
                        "punktlig", "målmedveten", "disciplin", "strukturerad", "ordentlig",
                        "noggrann", "självdisciplin", "engagerad", "ambition",
                        "arbetsam", "utföra", "korrekt", "fokuserad", "tillförlitlig"],
    "Extraversion": ["utåtriktad", "social", "energi", "prat", "självsäker", "entusiasm",
                     "äventyr", "entreprenör", "samarbetsvillig", "charmig", "aktiv",
                     "utåtriktning", "livlig", "drivande", "självförtroende", "överväldigande",
                     "målinriktad", "glad", "karisma"],
    "Medmänsklighet": ["empatisk", "samarbete", "tolerer", "hjälp", "tillit",
                       "omtänksamhet", "altruistisk", "mottaglig", "harmonisk", "inkluderande", "stöttande",
                       "generös", "medkän", "respekt", "medlidande", "omsorgsfull",
                       "medmänsklig", "tacksam", "förtroende"],
    "Emotionell stabilitet": ["stabil", "uthållig", "balanserad", "självsäker",
                              "positiv", "flexibel", "självkontroll", "optimist", "tålmodig",
                              "lugn", "tålamod", "självständig", "självmedveten", "behärskad",
                              "mjuk", "rofylld", "balans", "självförbättring", "säker", "modig", "varm", "bekväm"]
}
data = pd.read_excel('250perTitel.xlsx')
jobbeskrivningar = data.iloc[:, 1].astype(str).tolist()


def calculate_scores(jobbeskrivningar):
    regex_mönster = r'\b(?:{})\b'.format(
        '|'.join([re.escape(word) for words in personlighetstyper.values() for word in words])) + r'\b\w*\b'

    class RegexpTokenizer:
        def __init__(self, pattern):
            self.pattern = pattern

        def __call__(self, doc):
            return re.findall(self.pattern, doc)

    tokenizer = RegexpTokenizer(regex_mönster)
    vectorizer = TfidfVectorizer(tokenizer=tokenizer)

    vektoriserad_text = vectorizer.fit_transform(jobbeskrivningar)

    features = vectorizer.get_feature_names_out()
    scores = vektoriserad_text.toarray().sum(axis=0)

    df_scores = pd.DataFrame({'Ord': features, 'Poäng': scores})

    return df_scores


stemmer = SnowballStemmer('swedish')
stemmed_personlighetstyper = {personlighetstyp: [stemmer.stem(word) for word in ordlista]
                              for personlighetstyp, ordlista in personlighetstyper.items()}

resultat_per_personlighetstyp = {}
total_scores = {}



# Create a list to store the column headers
headers = ['Value'] + list(stemmed_personlighetstyper.keys())

# Create a list to store the rows
rows = []

for value in data.iloc[:, 2].unique():
    job_ads = data[data.iloc[:, 2] == value]
    job_descriptions = job_ads.iloc[:, 1].astype(str).tolist()

    scores = calculate_scores(job_descriptions)
    scores['Ord'] = scores['Ord'].apply(stemmer.stem)

    resultat_per_personlighetstyp[value] = {}

    for personlighetstyp, ordlista in stemmed_personlighetstyper.items():
        total_score = 0
        for word in ordlista:
            fuzzy_matches = scores[
                scores['Ord'].apply(lambda x: fuzz.ratio(x, word) >= 80)]
            if not fuzzy_matches.empty:
                total_score += fuzzy_matches['Poäng'].sum()
        resultat_per_personlighetstyp[value][personlighetstyp] = total_score

    total_scores[value] = sum(resultat_per_personlighetstyp[value].values())

    # Create a row for the current value
    row = [value]
    for personlighetstyp in stemmed_personlighetstyper.keys():
        score = resultat_per_personlighetstyp[value].get(personlighetstyp, 0)
        row.append(score)
    
    # Add the row to the list of rows
    rows.append(row)

    print(f"\nTotalpoäng för {value}: {total_scores[value]} poäng")
    print("Poäng per personlighetstyp:")
    for personlighetstyp, score in resultat_per_personlighetstyp[value].items():
        print(f"{personlighetstyp}: {score} poäng")

# Write the results to a CSV file
filename = 'results.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"\nResults written to {filename}")


