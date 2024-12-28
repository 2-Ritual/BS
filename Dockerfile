FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y curl && \
    apt-get install -y --fix-missing build-essential pkg-config libmariadb-dev-compat libmariadb-dev mariadb-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt

WORKDIR /app/price_cmp/frontend
COPY price_cmp/frontend/package*.json /app/price_cmp/frontend/

EXPOSE 8000 3306

WORKDIR /app

RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /wait-for-it.sh && \
    chmod +x /wait-for-it.sh

CMD ["bash", "-c", "/wait-for-it.sh db:3306 --  python manage.py makemigrations && python manage.py migrate && python load.py && python manage.py runserver 0.0.0.0:8000"]
