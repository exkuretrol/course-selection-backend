FROM python:3.10-slim

ENV TZ="Asia/Taipei"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install micropipenv[toml] && \
    micropipenv install --deploy && \
    pip cache purge

COPY . .

CMD ["python", "web_crawler.py"]
