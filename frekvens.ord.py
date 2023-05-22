import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
from nltk.stem import SnowballStemmer

personlighetstyper = {
    "Öppenhet för erfarenhet": ["kreativ", "intellektuell", "nyfiken", "konstnärlig", "uppfinning",
                                "reflekterande", "originell", "fantasifull", "visionär", "ovanlig",
                                "innovativ", "inspirera", "utforskande", "intuitiv", "uttrycksfull",
                                "tankeväckande", "analytisk", "komplex", "intresserad", "lärd"],
    "Samvetsgrannhet": ["organiserad", "ansvar", "plikttrogen", "pålitlig", "effektiv",
                        "punktlig", "målmedveten", "disciplin", "strukturerad", "ordentlig",
                        "noggrann", "systematisk", "självdisciplin", "engagerad", "ambition",
                        "arbetsam", "utföra", "korrekt", "fokus", "tillförlitlig"],
    "Extraversion": ["utåtriktad", "social", "energisk", "pratglad", "självsäker", "entusiasm",
                     "äventyr", "entreprenör", "samarbetsvillig", "charmig", "aktiv",
                     "utåtriktning", "livlig", "drivande", "självförtroende", "överväldigande",
                     "målinriktad", "modig", "glad", "karisma"],
    "Medmänsklighet": ["vänlig", "empatisk", "samarbete", "tolererant", "hjälpsam", "tillit",
                       "omtänksamhet", "altruistisk", "mottaglig", "harmonisk", "inkluderande", "stöttande",
                       "generös", "medkännande", "respekt", "medlidande", "omsorgsfull",
                       "medmänsklig", "tacksam", "förtroende"],
    "Emotionell stabilitet": ["stabil", "uthållig", "balanserad", "självsäker",
                              "positiv", "flexibel", "självkontroll", "optimist", "tålmodig",
                              "lugn", "tålamod", "självständig", "självmedveten", "behärskad",
                              "mjuk", "rofylld", "balans", "självförbättring", "säker", "modig"]
}

data = pd.read_excel('mjukvaru_data.xlsx')
jobbeskrivningar = data.iloc[:, 8].astype(str).tolist()


def calculate_scores(jobbeskrivningar):
    # Create a regex pattern for word matching
    regex_mönster = r'\b(?:{})\b'.format(
        '|'.join([re.escape(word) for words in personlighetstyper.values() for word in words])) + r'\b\w*\b'

    class RegexpTokenizer:
        def __init__(self, pattern):
            self.pattern = pattern

        def __call__(self, doc):
            return re.findall(self.pattern, doc)

    tokenizer = RegexpTokenizer(regex_mönster)
    vectorizer = TfidfVectorizer(tokenizer=tokenizer)

    # Perform text vectorization using tf-idf
    vektoriserad_text = vectorizer.fit_transform(jobbeskrivningar)

    # Get feature names and their tf-idf scores
    features = vectorizer.get_feature_names_out()
    scores = vektoriserad_text.toarray().sum(axis=0)

    # Create a DataFrame for words and their scores
    df_scores = pd.DataFrame({'Ord': features, 'Poäng': scores})

    return df_scores


# Initialize SnowballStemmer for Swedish
stemmer = SnowballStemmer('swedish')

# Stem the words in personlighetstyper
stemmed_personlighetstyper = {personlighetstyp: [stemmer.stem(word) for word in ordlista]
                              for personlighetstyp, ordlista in personlighetstyper.items()}

scores = calculate_scores(jobbeskrivningar)

# Stem the words in scores
scores['Ord'] = scores['Ord'].apply(stemmer.stem)

# Calculate total scores for each personality type
resultat_per_personlighetstyp = {}

for personlighetstyp, ordlista in stemmed_personlighetstyper.items():
    total_score = 0
    for word in ordlista:
        fuzzy_matches = scores[
            scores['Ord'].apply(lambda x: fuzz.ratio(x, word) >= 80)]
        if not fuzzy_matches.empty:
            total_score += fuzzy_matches['Poäng'].sum()
    resultat_per_personlighetstyp[personlighetstyp] = total_score

# Calculate total scores adjusted for the number of job advertisements
total_scores = {}
num_job_ads = len(jobbeskrivningar)

for personlighetstyp, score in resultat_per_personlighetstyp.items():
    adjusted_score = score / num_job_ads
    total_scores[personlighetstyp] = adjusted_score

# Print the total scores for each personality type
for personlighetstyp, score in total_scores.items():
    print(f"{personlighetstyp}: {score} poäng")

print("\nTop 10 mest förekomna ord per personlighetstyp:")

for personlighetstyp in personlighetstyper:
    print(personlighetstyp)
    ordlista = stemmed_personlighetstyper[personlighetstyp]
    ord_scores_personlighetstyp = scores[scores['Ord'].isin(ordlista)]
    ord_scores_personlighetstyp_sorted = ord_scores_personlighetstyp.sort_values(by='Poäng', ascending=False)
    top_10_ord = ord_scores_personlighetstyp_sorted.head(10)
    print(top_10_ord)
    print()










































                                        












