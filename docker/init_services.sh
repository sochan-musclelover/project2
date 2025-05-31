#!/bin/bash
set -e

# PostgreSQLデータディレクトリの権限修正
chown -R postgres:postgres /var/lib/pgsql/16/data

# PostgreSQL初期化（初回のみ）
if [ ! -s "/var/lib/pgsql/16/data/PG_VERSION" ]; then
    su - postgres -c "/usr/pgsql-16/bin/initdb -D /var/lib/pgsql/16/data"
fi

# ApacheのDocumentRootの権限修正（必要に応じて）
chown -R apache:apache /var/www/project2/app

# サービス起動
su - postgres -c "/usr/pgsql-16/bin/postgres -D /var/lib/pgsql/16/data" &
httpd -D FOREGROUND
