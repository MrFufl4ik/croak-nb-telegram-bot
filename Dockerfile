FROM python:3.14-slim

ARG APP_PATH="/app"
ENV APP_PATH=${APP_PATH}
WORKDIR ${APP_PATH}

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]