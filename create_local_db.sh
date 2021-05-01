set -e

cd "$(dirname "$0")"

echo "Remove old db file"
rm -f db.sqlite3

echo "Initialize"
docker-compose run web python manage.py migrate
docker-compose run web python manage.py create_default_admin
docker-compose run web python manage.py init_db