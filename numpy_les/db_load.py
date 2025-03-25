import sqlite3
import pandas as pd

# CSV-bestand inlezen met pandas
csv_file = 'd:\\temp\\games.csv'  # Vervang dit door jouw CSV-bestandsnaam
data = pd.read_csv(csv_file)

# Verbinden met de SQLite3-database (of maak er een als deze niet bestaat)
db_name = 'd:\\temp\\example.db'  # Vervang dit met jouw database naam
conn = sqlite3.connect(db_name)

# Zet de DataFrame om naar een SQL-tabel
table_name = 'universal'  # Kies een gewenste tabelnaam
data.to_sql(table_name, conn, if_exists='replace', index=False)


print(f"De data uit {csv_file} is succesvol geladen in de tabel '{table_name}'.")

# Sluit de verbinding
conn.close()
