FROM python:3.9

# Install necessary tools
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    g++ \
    curl \
    apt-transport-https \
    --no-install-recommends

# Add Microsoft's repository for the ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install the ODBC Driver
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Clean up
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "enchiridion.wsgi:application", "--bind", "0.0.0.0:8000"]
