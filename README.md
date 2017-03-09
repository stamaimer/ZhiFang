### ZhiFang

1. create virtual environment

    - ./create_venv.sh
    
2. create mysql database named `zhifang` with utf-8 encoding

3. `cp instance/config.py.example instance/config.py`

4. fill in the SECRET_KEY, SECURITY_PASSWORD_SALT, DB_USER, DB_PSWD in `instance/config.py`

5. initial database(with venv activated)
    
    - python manage.py rebuild_db

6. run server(with venv activated)

    - ./start.sh

