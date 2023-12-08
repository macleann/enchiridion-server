FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    g++ \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "enchiridion.wsgi:application", "--bind", "0.0.0.0:8000"]
