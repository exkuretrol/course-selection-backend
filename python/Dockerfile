FROM python:3.10-slim

ENV FLASK_APP=pyserver.py

# System depts:
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY ["pyproject.toml", "poetry.lock", "./"]

# Project initialization
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 5000

# run app
CMD [ "flask", "run", "--host=0.0.0.0" ]