#!/bin/bash

# Generate migrations based on the changes detected in your models
echo "Generating migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Clear data and load fixtures
echo "Clearing old data and loading fixtures..."
python manage.py flush --no-input

fixtures=("users" "tokens" "episodes" "playlists" "playlistepisodes")
for fixture in "${fixtures[@]}"
do
    echo "Loading fixture ${fixture}.json..."
    python manage.py loaddata enchiridionapi/fixtures/${fixture}.json
done

echo "Database seeding completed."