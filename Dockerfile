FROM python:3.14-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

ARG APP_PATH="/app"
ENV APP_PATH=${APP_PATH}
WORKDIR ${APP_PATH}

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN wget https://git.croakland.ru/mrfufl4ik/croak-bash-utils/raw/branch/main/wait-for/wait-for-it.sh \
    -q -O /usr/bin/wait-for-it.sh -L && \
    chmod +x /usr/bin/wait-for-it.sh

RUN wget https://git.croakland.ru/mrfufl4ik/croak-bash-utils/raw/branch/main/wait-for/wait-for-multiply.sh \
    -q -O /usr/bin/wait-for-multiply.sh -L && \
    chmod +x /usr/bin/wait-for-multiply.sh

CMD ["/usr/bin/wait-for-multiply.sh", "redis:6379", "--", "python", "src/main.py"]