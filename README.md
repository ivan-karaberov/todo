# Todo List API



## Реализовано:
- Регистрация пользователя
- Авторизация пользователя (JWT)
- Создание задачи
- Обновление задачи
- Удаление задачи
- Получения списка задач


## Запуск

#### Docker

```
docker compose up
```

#### Linux

1) Отредактируйте `.env` файл, заполнив в нём все переменные окружения:

Для управления зависимостями используется [poetry](https://python-poetry.org/),
требуется Python 3.10.

2) Установка зависимостей:

```bash
poetry install
```

3) Сгенерируйте пару ключей `jwt-private.pem` и `jwt-public.pem`
```bash
mkdir todo/core/certs && \
openssl genrsa -out todo/core/certs/jwt-private.pem 2048 && \
openssl rsa -in todo/core/certs/jwt-private.pem -pubout -out todo/core/certs/jwt-public.pem
```

4) Создание БД (требуется PostgreSQL 14):
```
cd todo && alembic upgrade head
```

5) Запуск
```
poetry run python main.py
```