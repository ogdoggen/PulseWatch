# PulseWatch

Backend-сервис для мониторинга доступности HTTP API.

Проект развивается поэтапно. Сейчас реализован каркас приложения: запуск API и PostgreSQL через Docker Compose, настройки окружения, проверки работоспособности и подключение к БД.

## Текущее состояние

Реализовано:

- FastAPI-приложение с документацией Swagger.
- Типизированные настройки через pydantic-settings.
- Асинхронное подключение к PostgreSQL через SQLAlchemy и asyncpg.
- Liveness и readiness endpoint.
- Запуск окружения через Docker Compose.
- Проверка и форматирование Python-кода через Ruff.

Запланировано:

- API управления мониторами и историей проверок.
- Ручные и периодические HTTP-проверки.
- Фоновое выполнение через Celery и Redis.
- Открытие инцидентов после последовательных сбоев.
- Уведомления о сбое и восстановлении в Telegram.
- Статистика результатов проверок.

## Технологии

- Python 3.13
- FastAPI, Uvicorn
- PostgreSQL 17
- SQLAlchemy async, asyncpg
- pydantic-settings
- Docker, Docker Compose
- Ruff

Зависимости приложения находятся в `requirements.txt`.
Инструменты разработки добавляются через `requirements-dev.txt`.

## Быстрый старт

Потребуется работающий Docker с Docker Compose v2, например Docker Desktop.

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ogdoggen/PulseWatch.git
cd PulseWatch
```

### 2. Подготовить настройки

При первом запуске:

```bash
cp .env.example .env
```

Проверь значения в `.env`. Имя БД, пользователь и пароль в `DATABASE_URL` должны соответствовать `POSTGRES_DB`, `POSTGRES_USER` и `POSTGRES_PASSWORD`.

Внутри сети Compose приложение обращается к PostgreSQL по имени сервиса `postgres`:

```dotenv
DATABASE_URL=postgresql+asyncpg://pulsewatch:pulsewatch_dev_password@postgres:5432/pulsewatch
```

Значения из `.env.example` предназначены для локальной разработки. Файл `.env` исключён из Git.

### 3. Собрать и запустить

```bash
docker compose config -q
docker compose up --build -d
docker compose ps
```

При первоначальном запуске API ожидает успешного healthcheck PostgreSQL.

После запуска:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

Обработчики текущего каркаса доступны по адресам `/health/live` и `/health/ready`.

## Настройки

| Переменная | Назначение |
| --- | --- |
| `APP_NAME` | Название приложения в документации API |
| `ENVIRONMENT` | Окружение, например `local` |
| `APP_VERSION` | Версия приложения |
| `POSTGRES_DB` | Имя БД при первоначальной инициализации PostgreSQL |
| `POSTGRES_USER` | Пользователь при первоначальной инициализации PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль пользователя при первоначальной инициализации PostgreSQL |
| `DATABASE_URL` | Строка подключения приложения к БД |

`DATABASE_URL` — обязательная настройка. Если она отсутствует, приложение завершит запуск с ошибкой валидации.

Изменение `POSTGRES_*` в `.env` не меняет учётные данные уже инициализированной БД.

## Проверки работоспособности

| Endpoint | Назначение | Ответ |
| --- | --- | --- |
| `GET /health/live` | Проверяет, что API обрабатывает запросы | `200` |
| `GET /health/ready` | Проверяет подключение к PostgreSQL выполнением `SELECT 1` | `200` при успехе, `503` при недоступной БД |

```bash
curl -i http://localhost:8000/health/live
curl -i http://localhost:8000/health/ready
```

Успешный ответ readiness:

```json
{"status": "ok", "database": "ok"}
```

### Проверка восстановления подключения

Остановить PostgreSQL:

```bash
docker compose stop postgres
```

При этом `/health/live` продолжает возвращать `200`, а `/health/ready` возвращает `503`.

Запустить БД снова:

```bash
docker compose start postgres
docker compose ps
```

После готовности PostgreSQL readiness снова возвращает `200` без перезапуска API.

## Разработка

Папка `app` подключена в контейнер через bind mount. Изменения Python-кода доступны контейнеру сразу, а Uvicorn с `--reload` перезапускает приложение.

После изменения зависимостей, Dockerfile или `pyproject.toml`:

```bash
docker compose up -d --build api
```

После изменения настроек API в `.env`:

```bash
docker compose up -d --force-recreate api
```

### Проверка кода

```bash
docker compose exec api ruff check app
docker compose exec api ruff format --check app
```

Автоматическое исправление доступных нарушений и форматирование:

```bash
docker compose exec api ruff check --fix app
docker compose exec api ruff format app
git diff -- app
```

Настройки Ruff находятся в `pyproject.toml`.

### Проверка зависимостей

```bash
docker compose exec api python -m pip check
```

## Логи и остановка

Посмотреть последние сообщения:

```bash
docker compose logs --tail=50 api postgres
```

Следить за логами API:

```bash
docker compose logs -f api
```

Остановить окружение:

```bash
docker compose down
```

Данные PostgreSQL хранятся в named volume и сохраняются после обычного `docker compose down`.

## Документация проекта

- [Требования и правила работы](docs/requirements.md)
- [План разработки](docs/plan.md)