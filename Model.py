import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# 1. Import danych z pliku CSV
df = pd.read_csv("listaFirm.csv", sep=";", encoding="utf-8")

# Zakładamy, że kolumny mają nazwy:
# 'NazwaPodmiotu', 'Nip', 'Przeważająca działalność gospodarcza'

X = df["NazwaPodmiotu"]
y = df["Przeważająca działalność gospodarcza"]

# 2. Pipeline: TF-IDF + klasyfikacja
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1
    )),
    ("clf", LogisticRegression(max_iter=300))
])

# 3. Trening modelu
model.fit(X, y)

# 4. Przykład predykcji
przyklad = ["Ogrodnik i usługi ogrodnicze Jan Kowalski"]
wynik = model.predict(przyklad)

print("Przewidywana działalność gospodarcza:", wynik[0])
