# SOAP WebSerivce
###Запуск:

``python -m pip install -r requitements.txt``

Создать таблицы для БД:

``python -c "from soap_service.storage import db;db.init_db()"``

WSGI сервер из стандартной библиотеки:

``python server.py``

Gunicorn:

``gunicorn -b {HOST}:{PORT} soap_service.server.server``

Docker-compose:

``docker-compose up``

###Переменные окружения:
* **DB_TYPE** - тип БД (пустая строка)
* **DB_NAME** - имя БД (app.db)
* **DB_HOST** - адресс БД (127.0.0.1)
* **DB_PORT** - порт БД (5432)
* **DB_USER** - пользователь БД
* **DB_PASSWORD** - пароль пользователя
* **DB_PATH** - путь к БД, если используется Sqlite

По умолчанию используется Sqlite.

Для использования PostgreSQL задать **DB_TYPE** = 'postgres', а также хост, порт, пользователя и пароль.

###URLs

* **WSDL** ``http://host:port/?wsdl``