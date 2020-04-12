source .env-$CLUSTER
python manage.py makemigrations
python manage.py migrate
/usr/bin/supervisord -c /etc/supervisord.conf 
python manage.py runserver 0.0.0.0:$PORT
