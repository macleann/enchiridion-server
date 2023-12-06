FROM python:3.8.5

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    g++ \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

ENV NAME World

CMD ["pipenv", "run", "gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
