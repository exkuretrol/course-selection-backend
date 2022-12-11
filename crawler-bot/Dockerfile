FROM python:3.10-slim

ENV TZ="Asia/Taipei"

# System depts:
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY ["pyproject.toml", "poetry.lock", "./"]

# Project initialization
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["python", "web_crawler.py"]
