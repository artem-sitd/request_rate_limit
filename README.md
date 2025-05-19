# 🚦 Request Rate Limiter API

HTTP-сервис для ограничения количества запросов (rate limiting) из одной подсети IPv4. При превышении лимита возвращает сообщение об ошибке, в противном случае — статический контент.

---

## 🚀 Возможности

- 📈 Ограничение количества запросов по подсети IPv4
- 🧠 Хранение статистики запросов в Redis
- 🔄 Сброс статистики по подсети через API
- 🐳 Развёртывание с использованием Docker Compose
- 🧪 Тестирование с использованием unittest

---

## 🧰 Технологии

- Python 3.10+
- Flask
- Redis
- python-dotenv
- unittest
- Docker & Docker Compose

---

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/artem-sitd/request_rate_limit.git
   cd request_rate_limit
   ```

2. **Настройте переменные окружения:**

   Переименуйте файл `.env.docker.template` в `.env.docker`:

   ```bash
   cp .env.docker.template .env.docker
   ```

   Отредактируйте файл `.env.docker`, указав необходимые значения:

   - `REDIS_HOST` — хост Redis
   - `REDIS_PORT` — порт Redis
   - `RATE_LIMIT` — максимальное количество запросов за период
   - `RATE_PERIOD` — период в секундах для ограничения запросов

3. **Запустите приложение с помощью Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Приложение будет доступно по адресу `http://localhost:5000`.

---

## 📁 Структура проекта

```
├── app/                   # Основная логика приложения
├── tests/                 # Тесты unittest
├── .env.docker.template   # Шаблон переменных окружения
├── docker-compose.yaml    # Конфигурация Docker Compose
├── main.py                # Точка входа в приложение
├── pyproject.toml         # Зависимости проекта
└── README.md              # Документация проекта
```

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл `LICENSE`.
