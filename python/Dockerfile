FROM python:latest

ENV FLASK_APP=pyserver.py

# System depts:
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY ["pyproject.toml", "poetry.lock", "./"]

EXPOSE 5000

# Project initialization
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# run app
EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]