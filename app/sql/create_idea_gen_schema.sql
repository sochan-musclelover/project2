-- スキーマ作成
CREATE SCHEMA IF NOT EXISTS idea_gen;

-- アイデア元の単語テーブル
CREATE TABLE IF NOT EXISTS idea_gen.idea_words (
    id SERIAL PRIMARY KEY,
    word_no INTEGER NOT NULL,
    word TEXT NOT NULL,
    meaning TEXT
);

-- 企画生成ジョブリストテーブル（修正版）
CREATE TABLE IF NOT EXISTS idea_gen.generation_jobs (
    job_id SERIAL PRIMARY KEY,
    generate_count INTEGER NOT NULL,
    result_file TEXT,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP
);

-- 企画生成結果テーブル
CREATE TABLE IF NOT EXISTS idea_gen.generated_ideas (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES idea_gen.generation_jobs(job_id) ON DELETE CASCADE,
    xxx TEXT NOT NULL,
    yyy TEXT NOT NULL,
    zzz TEXT NOT NULL,
    idea TEXT NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
