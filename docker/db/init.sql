-- ユーザー作成
CREATE USER simuser WITH PASSWORD 'simpassword';

-- データベース作成
CREATE DATABASE simulation_db OWNER simuser;

-- システムでは \c は使えないのでスクリプト外にする必要あり（compose init時点で既にDBに接続）

-- スキーマ作成（接続後に実行される）
\connect simulation_db

CREATE SCHEMA IF NOT EXISTS simschema AUTHORIZATION simuser;

-- デフォルトスキーマ設定
ALTER ROLE simuser SET search_path TO simschema,public;

CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    initial_population INTEGER,
    final_population INTEGER,
    result VARCHAR(32),
    output_file_path TEXT
);

CREATE TABLE IF NOT EXISTS person_info (
    job_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    birth_year INTEGER NOT NULL,
    sex VARCHAR(2) NOT NULL,
    death_year INTEGER,
    fertility INTEGER NOT NULL,
    marriage_status VARCHAR(16),
    adaptation_ability INTEGER NOT NULL,
    leverage_ability INTEGER NOT NULL,
    PRIMARY KEY (job_id, year, person_id)
);

CREATE TABLE IF NOT EXISTS person_list (
    job_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, year, person_id)
);

CREATE TABLE IF NOT EXISTS parent_child_relation (
    job_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, year, parent_id, child_id)
);
