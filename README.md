# Мини-трекер задач (Todo API)

Простое REST API для управления задачами, построенное на Flask + PostgreSQL, развёрнутое в Docker Compose.

## Технологический стек

- Python 3.11 + Flask
- PostgreSQL 15 (в контейнере)
- Docker + Docker Compose
- psycopg2-binary

---

## 1. Запуск приложения

```bash
docker compose up --build -d
```

---

## 2. Проверка работы endpoint'ов

### Создать задачу

```bash
curl localhost:5000/create/learn_docker
# Вывод: created
```

### Отметить задачу выполненной

```bash
curl localhost:5000/done/1
# Вывод: updated
```

### Список невыполненных задач

```bash
curl localhost:5000/pending
# Вывод:
# 1 learn_docker
# 2 setup_postgres
```

### Статистика

```bash
curl localhost:5000/stats
# Вывод:
# total: 2
# done: 0
# pending: 2
```

---

## 3. Демонстрация сохранения данных после перезапуска

```bash
# Шаг 1 — Создать задачи
curl localhost:5000/create/learn_docker
curl localhost:5000/create/setup_postgres
curl localhost:5000/create/write_readme

# Шаг 2 — Отметить одну выполненной
curl localhost:5000/done/1

# Шаг 3 — Проверить статистику ДО перезапуска
curl localhost:5000/stats
# Вывод:
# total: 3
# done: 1
# pending: 2

# Шаг 4 — Перезапустить контейнеры
docker compose down
docker compose up -d

# Шаг 5 — Проверить статистику ПОСЛЕ перезапуска
curl localhost:5000/stats
# Ожидаемый результат — данные сохранились:
# total: 3
# done: 1
# pending: 2
```

---

## 4. Полезные команды

```bash
# Посмотреть логи
docker compose logs web
docker compose logs db

# Подключиться к PostgreSQL напрямую
docker compose exec db psql -U user -d tododb

# Посмотреть данные в таблице
SELECT * FROM tasks;

# Остановить всё
docker compose down

# Удалить данные (удалить volume)
docker compose down -v
```
