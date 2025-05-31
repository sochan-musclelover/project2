from django.shortcuts import render
from django.db import connection
import csv
import os
from datetime import datetime

# トップページのビュー
# 英語表記、概要付き
# This is the top page view for the Project Idea Auto Generator System.
def top(request):
    context = {
        'title': 'Project Idea Auto Generator System',
        'description': (
            'This system generates project ideas by combining Japanese words. '
            'The core concept is to create unique ideas by generating combinations of words, '
            'which form the basis of new project proposals.'
        )
    }
    return render(request, 'top.html', context)

# アイデアgeneratorページのモック
# This is a mock page for the idea generator.
def idea_generator(request):
    idea = None
    csv_path = None
    job_id = None
    jobs = []
    if request.method == 'POST':
        generate_count = 1  # 生成数（必要に応じてフォームから取得も可）
        started_at = datetime.now()
        # ジョブ登録
        with connection.cursor() as cur:
            cur.execute("""
                INSERT INTO idea_gen.generation_jobs (generate_count, started_at)
                VALUES (%s, %s) RETURNING job_id;
            """, [generate_count, started_at])
            job_id = cur.fetchone()[0]
        # 単語を3つランダム取得
        with connection.cursor() as cur:
            cur.execute("SELECT word FROM idea_gen.idea_words ORDER BY random() LIMIT 3;")
            rows = cur.fetchall()
        if len(rows) == 3:
            xxx, yyy, zzz = [row[0] for row in rows]
            idea = f"Although {xxx} is believed to be {yyy}, I think {xxx} is {zzz}, and I will deny everything in this world."
            # 結果CSV出力
            now = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_dir = os.path.join('appresult')
            os.makedirs(result_dir, exist_ok=True)
            csv_path = os.path.join(result_dir, f'idea_{now}.csv')
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['XXX', 'YYY', 'ZZZ', 'Idea'])
                writer.writerow([xxx, yyy, zzz, idea])
            # 結果テーブルに登録
            finished_at = datetime.now()
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO idea_gen.generated_ideas (job_id, xxx, yyy, zzz, idea, generated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [job_id, xxx, yyy, zzz, idea, finished_at])
                # ジョブテーブルに結果ファイルと終了時間を更新
                cur.execute("""
                    UPDATE idea_gen.generation_jobs
                    SET result_file = %s, finished_at = %s
                    WHERE job_id = %s
                """, [csv_path, finished_at, job_id])
            connection.commit()  # ここで明示的にコミット
    # 過去のジョブ一覧を取得
    with connection.cursor() as cur:
        cur.execute("""
            SELECT job_id, started_at, finished_at, result_file, generate_count
            FROM idea_gen.generation_jobs
            ORDER BY started_at DESC
            LIMIT 20
        """)
        jobs = cur.fetchall()
    return render(request, 'generator.html', {'idea': idea, 'csv_path': csv_path, 'jobs': jobs})

# アイデアリストページのモック
# This is a mock page for the idea list.
def idea_list(request):
    job_id = request.GET.get('job_id')
    ideas = []
    with connection.cursor() as cur:
        if job_id:
            cur.execute("""
                SELECT g.id, g.xxx, g.yyy, g.zzz, g.idea, j.result_file, g.generated_at
                FROM idea_gen.generated_ideas g
                JOIN idea_gen.generation_jobs j ON g.job_id = j.job_id
                WHERE g.job_id = %s
                ORDER BY g.generated_at DESC
                LIMIT 100
            """, [job_id])
        else:
            # 直近の最新job_idを取得
            cur.execute("SELECT job_id FROM idea_gen.generation_jobs ORDER BY started_at DESC LIMIT 1;")
            row = cur.fetchone()
            if row:
                latest_job_id = row[0]
                cur.execute("""
                    SELECT g.id, g.xxx, g.yyy, g.zzz, g.idea, j.result_file, g.generated_at
                    FROM idea_gen.generated_ideas g
                    JOIN idea_gen.generation_jobs j ON g.job_id = j.job_id
                    WHERE g.job_id = %s
                    ORDER BY g.generated_at DESC
                    LIMIT 100
                """, [latest_job_id])
                ideas = cur.fetchall()
                return render(request, 'idea_list.html', {'ideas': ideas, 'job_id': latest_job_id})
            else:
                ideas = []
    return render(request, 'idea_list.html', {'ideas': ideas, 'job_id': job_id})
