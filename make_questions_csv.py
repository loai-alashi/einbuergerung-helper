import csv

OUT_FILE = "questions_seed_50.csv"

rows = [
    # category, question, option_a, option_b, option_c, option_d, correct_option, source_url
    ("leben_in_deutschland", "What is the capital of Germany?", "Munich", "Hamburg", "Berlin", "Frankfurt", "C", "https://www.lebenindeutschland.eu/fragenkatalog"),
    ("leben_in_deutschland", "Which institution checks whether laws follow the Grundgesetz?", "Bundestag", "Bundesrat", "Bundesverfassungsgericht", "Bundesbank", "C", "https://www.lebenindeutschland.eu/fragenkatalog"),
    ("geography", "Which river flows through Cologne (Köln)?", "Elbe", "Rhine (Rhein)", "Danube (Donau)", "Oder", "B", ""),
    ("culture", "Which is a famous German composer?", "Johann Sebastian Bach", "Antonio Vivaldi", "Frederic Chopin", "Pyotr Tchaikovsky", "A", ""),
    ("politics", "Germany is a ...", "Monarchy", "Federal republic", "One-party state", "Military dictatorship", "B", ""),
]

# duplicate these base questions in a safe way just to reach 50 rows (placeholder seed)
# IMPORTANT: later we replace with real unique questions
base = rows.copy()
while len(rows) < 50:
    i = len(rows) - len(base)
    c, q, a, b, copt, d, correct, url = base[i % len(base)]
    rows.append((c, q + f" (set {len(rows)+1})", a, b, copt, d, correct, url))

with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["category","question","option_a","option_b","option_c","option_d","correct_option","source_url"])
    writer.writerows(rows)

print(f"Created: {OUT_FILE} with {len(rows)} rows")
