import csv

# サンプル単語データ
words = [
    (1, '愛', 'Love'),
    (2, '青', 'Blue'),
    (3, '赤', 'Red'),
    (4, '秋', 'Autumn'),
    (5, '朝', 'Morning'),
    (6, '足', 'Foot'),
    (7, '雨', 'Rain'),
    (8, '家', 'House'),
    (9, '医者', 'Doctor'),
    (10, '犬', 'Dog'),
]

with open('idea_generator/source_words/sample_words.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['No.', 'Word', 'Meaning'])
    for row in words:
        writer.writerow(row)

# 日本語コメント: このスクリプトを app ディレクトリで実行すると sample_words.csv が出力されます。
