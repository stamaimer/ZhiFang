/ZhiFang/wait-for-it.sh db:3306 -t 30
python manage.py db_init
python manage.py runserver -h 0.0.0.0
