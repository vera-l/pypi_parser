# Парсер Pypi

Фоново собирает информацию по сайту https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3 :

1. Имя пакета
2. Имя автора (если доступно)
2. Количество звёзд проекта на гитхабе и список контрибьюторов (если указана ссылка на домашнюю страницу, и это страница репозитория проекта на гитхабе)

## Запуск сервера

```bash
./run.sh
```

Парсинг осуществляется в фоновом режиме, следить за процессом можно по логам:

```bash
tail -f parse.log
```

## Запрос для получения собранной информации

```
GET /api/most_popular?page={int}&on_page={int}&order_by={json_field}
```

## Формат ответа

```javascript
[
    {
        "package": "aiohttp",
        "author": "Nikolay Kim",
        "last_deploy": "2019-10-09T16:54:45+0000",
        "stars": 8730,
        "git_repo": "https://github.com/aio-libs/aiohttp",
        "maintainers": ["Nikolay Kim", "Andrew Svetlov"]
    },
    // ...
]
```
