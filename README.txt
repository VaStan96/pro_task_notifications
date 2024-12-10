notifications_service/
├── app/
│   ├── __init__.py
│   ├── main.py         # Точка входа, запускает FastAPI
│   ├── config.py       # Настройки приложения (например, база данных, Kafka)
│   ├── models.py       # Описание моделей SQLAlchemy
│   ├── schemas.py      # Pydantic-схемы для валидации данных
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── notifications.py  # Эндпоинты для работы с уведомлениями
│   ├── services/
│   │   ├── __init__.py
│   │   ├── notification_service.py  # Логика работы с уведомлениями
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py  # Подключение к базе данных
│   ├── events/
│       ├── kafka_consumer.py  # Обработчик сообщений из Kafka
├── tests/
│   ├── test_main.py    # Тесты API
│   ├── test_services.py  # Тесты бизнес-логики
├── requirements.txt    # Список зависимостей
├── Dockerfile          # Контейнеризация сервиса
└── README.md           # Документация проекта