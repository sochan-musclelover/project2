import csv
import psycopg2

# DB接続情報（docker-compose.ymlの設定に合わせて修正）
DB_HOST = 'localhost'  # または '127.0.0.1'
DB_PORT = 5432
DB_NAME = 'simulation_db'
DB_USER = 'simuser'
DB_PASS = 'simuser'

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

with open('tmp/wiktionary_nouns2.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダーをスキップ
    for row in reader:
        word_no, word, meaning = row
        cur.execute(
            "INSERT INTO idea_gen.idea_words (word_no, word, meaning) VALUES (%s, %s, %s)",
            (int(word_no), word, meaning)
        )

conn.commit()
cur.close()
conn.close()
print("Import completed.")