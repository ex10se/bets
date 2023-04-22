# Система, принимающая пользовательские ставки на определённые события

Система состоит из двух независимых сервисов:
- сервис line-provider — провайдер информации о событиях,
- сервис bet-maker, принимающий ставки на эти события от пользователя.

### line-provider
Сервис выдает информацию о событиях, на которые можно совершать ставки. Принимаются ставки только на выигрыш первой команды.

### bet-maker
Сервис отвечает за постановку ставок на события пользователями. Информация о событиях получается из line-provider. 

## Запуск системы локально
Выполняется с помощью docker следующим образом:
```shell
cd ci
docker-compose up -d
```

## Технологии
Используется FastAPI с Python 3.10 и PostgreSQL
