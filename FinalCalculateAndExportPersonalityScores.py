import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv

personlighetstyper = {
    "Öppenhet för erfarenhet": ["öppen","kreativ", "intellektuell", "nyfiken", "reflektiv", "konstnärlig", "uppfinningsrik",
                                "reflekterande", "fantasifull", "visionär", "experimentell", "inspirerad", "nytänkande",
                                "innovativ","innovatör", "intuitiv", "uttrycksfull", "utforskande", "undersökande",
                                "tankeväckande", "analytisk", "komplex", "intresserad", "idérik"],

    "Samvetsgrannhet": ["organiserad", "ansvarsfull", "plikttrogen", "effektiv", "ansvarstagande",
                        "punktlig", "målmedveten", "disciplinerad", "strukturerad", "ordentlig",
                        "noggrann", "självdisciplin", "engagerad","engagemang", "ambitiös","ambition","korrekt",
                        "arbetsam", "utföra", "fokuserad"],

    "Extraversion": ["utåtriktad", "social", "energisk","prat", "entusiastisk", "initiativtagande",
                     "äventyr", "entrepenör", "kommunikativ", "charmig", "aktiv", "entusiasm",
                     "utåtriktning", "livlig", "drivande", "självförtroende",
                     "målinriktad", "glad", "karisma", "framåt"],

    "Medmänsklighet": ["empatisk", "samarbete", "tolererant", "hjälp", "samarbetsförmåga",
                       "omtänksam", "mottaglig", "stöttande", "stödjande", 
                       "generös", "medkänsla", "medlidande", "omsorgsfull",
                       "medmänsklig", "tacksam", "förtroende", "tillförlitlig"],

    "Emotionell stabilitet": ["stabil", "uthållig", "balanserad", "harmonisk","stresstålig", "trygg", 
                              "positiv", "flexibel", "självkontroll", "optimist", "tålmodig", "självgående",
                              "lugn", "tålamod", "självständig","självinsikt", "självmedveten", "behärskad", "stadig",
                              "mjuk", "rofylld", "balans", "självförbättras", "modig", "varm", "bekväm", "självsäker"]
}

def is_similar(word1, word2):
    similarity_ratio = fuzz.ratio(word1, word2)
    return similarity_ratio >= 70

data = pd.read_excel('Final250PerTitleWithoutStopwords.xlsx')

combined_scores = {}

for key, value in personlighetstyper.items():
    vectorizer = TfidfVectorizer(vocabulary=value)
    tfidf_matrix = vectorizer.fit_transform(data['description'])
    tfidf_scores = tfidf_matrix.toarray().sum(axis=1)

    similar_words = []
    for word in value:
        similar_word = process.extractOne(word, vectorizer.get_feature_names(), scorer=fuzz.ratio)
        if similar_word and is_similar(word, similar_word[0]):
            similar_words.append(similar_word[0])

    combined_scores[key] = tfidf_scores

grouped_data = data.groupby('occupation')
summed_scores = {}

for title, group in grouped_data:
    scores = [combined_scores[key][group.index].sum() for key in combined_scores.keys()]
    summed_scores[title] = scores

# Prepare the data for writing to CSV
headers = ['Job Title'] + list(combined_scores.keys())
rows = []

for title, scores in summed_scores.items():
    row = [title] + scores
    rows.append(row)

# Write the results to a CSV file
filename = 'resultAndScore.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"\nResults written to {filename}")
