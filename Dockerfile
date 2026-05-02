FROM python:3.14-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

ARG APP_PATH="/app"
ENV APP_PATH=${APP_PATH}
WORKDIR ${APP_PATH}

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN wget https://raw.githubusercontent.com/MrFufl4ik/croak-bash-utils/refs/heads/main/wait-for/wait-for-it.sh \
    -q -O /usr/bin/wait-for-it.sh -L && \
    chmod +x /usr/bin/wait-for-it.sh

RUN wget https://raw.githubusercontent.com/MrFufl4ik/croak-bash-utils/refs/heads/main/wait-for/wait-for-multiply.sh \
    -q -O /usr/bin/wait-for-multiply.sh -L && \
    chmod +x /usr/bin/wait-for-multiply.sh

CMD ["/usr/bin/wait-for-multiply.sh", "database:5432", "redis:6379", "xray:1080", "--", "python", "src/main.py"]