# 📌 Conventional Commits (самый популярный стандарт)
- Формат:
  - type(scope): subject
- Где:
  - type → что именно сделал коммит:
    - feat — новая фича (увеличивает minor версию).
    - fix — исправление бага (увеличивает patch версию).
    - refactor — рефакторинг без изменения функционала.
    - perf — оптимизация производительности.
    - docs — документация.
    - test — только тесты.
    - build — сборка, зависимости, CI/CD.
    - chore — рутина, мелкие изменения, не влияющие на код.
    - style — форматирование, пробелы, без логики.
    - revert — откат коммита.
  - scope → область изменений (необязателен): api, auth, db, ui и т. д.
  - subject → коротко и в повелительном наклонении: «add endpoint», «fix bug», «update docs».

# Организация файлов в проекте
- V1
```text
service-users/
├─ pyproject.toml                  # PEP 621, deps, конфиги инструментов
├─ uv.lock | poetry.lock
├─ README.md                       # как запускать/тестировать/релизить
├─ .pre-commit-config.yaml         # ruff, ruff-format(or black), mypy, commitlint, detect-secrets
├─ .gitignore | .gitattributes     # игнор/строки (LF)
├─ .env.example                    # пример env (без секретов)
├─ Makefile | justfile             # run, test, fmt, lint, mypy, migrate, docker-build, release
├─ docker/
│  ├─ Dockerfile                   # multi-stage, slim, non-root, healthcheck
│  └─ entrypoint.sh                # только запуск app (миграции — отдельный job)
├─ deploy/
│  ├─ helm/                        # чарт сервиса (values-{dev,prod}.yaml)
│  └─ ghactions/ci.yml             # CI: lint/type/tests/image/scan/release
├─ alembic/
│  ├─ env.py                       # автоподхват models из features/*/infrastructure/db
│  ├─ versions/
│  └─ alembic.ini
├─ tests/
│  ├─ unit/{domain,application}
│  ├─ integration/{db,cache,http}  # testcontainers
│  └─ e2e/http                     # httpx + asgi-lifespan
└─ src/
   └─ service_users/               # имя пакета = имя сервиса
      ├─ core/                     # платформенные вещи
      │  ├─ config.py              # Pydantic Settings (ENV-only; в проде .env не читаем)
      │  ├─ logging.py             # structlog JSON + request_id/trace_id
      │  ├─ security.py            # CORS/headers, body-size, rate-limit hooks
      │  └─ instrumentation/       # OTEL, Prometheus /metrics
      ├─ db/
      │  ├─ base.py                # DeclarativeBase + naming_convention
      │  ├─ session.py             # create_async_engine, async_sessionmaker
      │  └─ uow.py                 # Async UoW (context manager), expire_on_commit=False
      ├─ integration/clients/      # внешние клиенты (httpx/grpc), генерённые SDK
      ├─ tasks/                    # фоновые воркеры/консьюмеры
      ├─ features/                 # ВЕРТИКАЛЬНЫЕ СЛАЙСЫ
      │  └─ users/
      │     ├─ api/
      │     │  ├─ routers/v1/{users.py, health.py, readiness.py}
      │     │  ├─ deps/{uow.py, auth.py}
      │     │  ├─ schemas/{user_in.py, user_out.py}
      │     │  └─ errors.py
      │     ├─ application/
      │     │  ├─ commands/{create_user.py, ...}
      │     │  ├─ queries/{get_user.py, ...}
      │     │  ├─ handlers/{command_handlers.py, query_handlers.py, event_handlers.py}
      │     │  ├─ mappers.py      # домен ↔ DTO/ORM
      │     │  └─ bus.py          # диспетчер (Command/Query → handler)
      │     ├─ domain/
      │     │  ├─ aggregates/user.py
      │     │  ├─ value_objects.py # Email, FullName, PasswordHash ...
      │     │  ├─ events.py
      │     │  ├─ errors.py
      │     │  └─ ports/           # ЧИСТЫЕ интерфейсы (typing.Protocol)
      │     │     ├─ repositories.py
      │     │     ├─ uow.py
      │     │     └─ event_bus.py
      │     └─ infrastructure/
      │        ├─ db/{models.py, repositories/user_repo.py}
      │        ├─ messaging/{event_bus.py, outbox.py}   # Transactional Outbox
      │        ├─ cache/redis.py
      │        └─ http/clients/...
      ├─ main.py                    # create_app(), сборка фич, роутинг /api/v1
      └─ lifespan.py                # startup/shutdown (engine, telemetry, warmups)
```
- V2
```text
service-name/
├── .env.example                   # Пример переменных окружения для локальной разработки
├── .github/                       # Автоматизация CI/CD
│   └─ workflows/
│      └─ ci.yml                    # Линтинг, тесты, сборка Docker, сканирование безопасности
├── .gitignore
├── .pre-commit-config.yaml        # Хуки для автоформатирования и линтинга (ruff, mypy)
├── ADRs/                          # (Architecture Decision Records) Записи об архитектурных решениях
├── Makefile                       # Удобные шорткаты (make test, make lint, make run, make migrate)
├── README.md                      # Полное описание: как запустить, тестировать, развернуть
├── alembic.ini                    # Конфигурация Alembic
├── alembic/                       # Директория для миграций базы данных
│   └─ versions/
├── deploy/                        # Все для развертывания (IaC)
│   └─ helm/
│      ├─ Chart.yaml
│      ├─ values.yaml
│      └─ templates/
├── docker/
│   ├─ Dockerfile                 # Multi-stage сборка, запуск от non-root пользователя
│   └─ compose.dev.yml            # Docker Compose для локального окружения (DB, Redis, Jaeger...)
├── pyproject.toml                 # Зависимости и конфигурация инструментов (uv/poetry, ruff, mypy)
├── tests/
│   ├─ conftest.py                # Общие фикстуры для тестов
│   ├─ e2e/                       # Сквозные тесты (проверка API через HTTP, с прогоном миграций)
│   ├─ integration/               # Интеграционные тесты (с реальной БД/кэшем в testcontainers)
│   └─ unit/                      # Юнит-тесты (изолированная проверка доменной логики)
└─ src/
   └─ service/                    # Имя пакета вашего сервиса
      ├─ main.py                  # Точка входа: FastAPI app, подключение роутеров из фич, middleware
      ├─ lifespan.py              # Логика startup/shutdown (пулы соединений, клиенты)
      ├─ core/                    # Сквозные платформенные компоненты
      │  ├─ config.py             # Конфигурация (Pydantic-Settings)
      │  ├─ logging.py            # Настройка логирования (structlog, JSON-формат)
      │  └─ telemetry.py          # Настройка телеметрии (OpenTelemetry, Prometheus metrics)
      ├─ db/                      # Настройка подключения к БД
      │  ├─ base.py               # DeclarativeBase для SQLAlchemy моделей
      │  ├─ session.py            # Engine, sessionmaker
      │  └─ uow.py                # Реализация паттерна Unit of Work (UoW)
      ├─ shared/                  # Общий код, используемый РАЗНЫМИ фичами
      │  ├─ domain/               # Общие доменные примитивы (напр., BaseEntity, DomainEvent)
      │  └─ dto.py                # Общие DTO, если необходимо
      ├─ features/                # <-- СЕРДЦЕ АРХИТЕКТУРЫ: ВЕРТИКАЛЬНЫЕ СЛАЙСЫ
      │  ├─ users/                # Пример фичи "Пользователи"
      │  │  ├─ api.py             # FastAPI Router, DTO (схемы Pydantic), зависимости для этой фичи
      │  │  ├─ application.py     # Use-cases: команды, запросы и их обработчики (CQRS)
      │  │  ├─ domain.py          # Чистая доменная модель: Агрегат, VO, события, порты (интерфейсы)
      │  │  └─ infrastructure.py  # Адаптеры: реализация репозитория, маппинг ORM
      │  └─ orders/               # Пример другой фичи "Заказы" со своей структурой
      │     ├─ api.py
      │     ├─ application.py
      │     ├─ domain.py
      │     └─ infrastructure.py
      ├─ integrations/            # Клиенты для взаимодействия с ВНЕШНИМИ системами
      │  ├─ payment_gateway_client.py
      │  └─ notification_service_client.py
      └─ workers/                 # Фоновые задачи и обработчики сообщений
         ├─ outbox_processor.py   # Воркер для паттерна Transactional Outbox
         └─ kafka_consumers.py    # Потребители сообщений из Kafka/RabbitMQ
```