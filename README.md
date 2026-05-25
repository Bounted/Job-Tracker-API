# Task Manager API

API для управления задачами. Можно:
- зарегистрироваться
- авторизоваться (JWT)
- обновлять токен без повторного входа
- выходить из системы (logout)
- создавать задачи
- менять статус задач
- удалять задачи
- получать список своих задач

## Технологии

- Python 3.13
- FastAPI
- SQLAlchemy + PostgreSQL (async)
- Alembic (миграции)
- Docker + Docker Compose
- Pytest + pytest-asyncio + httpx
- Poetry
- Refresh-токены + Logout
- Health check + Readiness probe
- Connection pooling
- Стандартизированные ответы ошибок

## Тесты

Все тесты асинхронные. Запуск:
docker compose exec web poetry run pytest --cov

## CI/CD

При каждом пуше GitHub Actions автоматически запускает тесты.

## Деплой

Проект развёрнут на Render: https://fastapi-task-api-kzur.onrender.com/docs

## Структура проекта

├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── alembic.ini
├── main.py
├── core/            # конфиг, безопасность, исключения
├── db/              # подключение к БД
├── models/          # SQLAlchemy модели
├── schemas/         # Pydantic схемы
├── repositories/    # запросы к БД
├── services/        # бизнес-логика
├── api/             # роутеры и зависимости
├── tests/           # тесты
├── alembic/         # миграции
├── .github/workflows/

## Запуск

1. Клонировать репозиторий
2. Скопировать в .env и указать свои значения:

SECRET_KEY=любой_секретный_ключ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://postgres:пароль@db:5432/todo_app

3. docker compose up -d --build
4. docker compose exec web poetry run alembic upgrade head
5. Открыть http://localhost:8000/docs