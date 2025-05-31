# ベースイメージ: Rocky Linux 9
FROM rockylinux:9

# 必要なパッケージのインストール
RUN dnf -y update && \
    dnf -y install epel-release && \
    dnf -y install \
    python3 \
    python3-pip \
    httpd \
    httpd-core \
    httpd-filesystem \
    mailcap \
    mod_wsgi \
    gcc \
    wget \
    git \
    make && \
    dnf clean all

# PostgreSQLのインストール
RUN dnf -y install epel-release && \
    dnf -y install https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    dnf -qy module disable postgresql && \
    dnf -y install postgresql16 postgresql16-server

# Python 仮想環境用のディレクトリ作成（任意）
WORKDIR /var/www/project2/app
RUN pip install requests beautifulsoup4
# Pythonパッケージ要件（Flaskや他フレームワークを入れるならここ）
COPY app/requirements.txt /var/www/project2/app/
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
RUN pip3 install psycopg2-binary
RUN dnf -y install httpd-filesystem
# アプリケーションとWSGIファイルの配置
COPY app/ /var/www/project2/app/

# Apacheの設定ファイルを差し替え（必要な場合）
COPY docker/httpd.conf /etc/httpd/conf/httpd.conf

# PostgreSQL設定ファイル（必要ならカスタマイズ）
# COPY docker/db/postgresql.conf /var/lib/pgsql/16/data/postgresql.conf
# COPY docker/db/pg_hba.conf /var/lib/pgsql/16/data/pg_hba.conf

# mime.typesが無い場合のため、最小限のmime.typesを用意
RUN echo 'text/html html\ntext/plain txt' > /etc/httpd/conf/mime.types

# Apache ポート開放
EXPOSE 80

# PostgreSQL ポート（任意：別ポートが必要な場合）
EXPOSE 5432

# PostgreSQL 初期化（永続化すれば一度だけ）
# RUN /usr/pgsql-16/bin/postgresql-16-setup initdb

# init_services.shをイメージにコピーし、実行権限を付与
COPY docker/init_services.sh /init_services.sh
RUN chmod +x /init_services.sh

RUN mkdir -p /var/log/httpd
RUN chown apache:apache /var/log/httpd
# シェルスクリプトをCMDで実行
CMD ["/init_services.sh"]
