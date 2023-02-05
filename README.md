# api_final_yatube
## Описание проекта api_yatube_final:
Проект является API-сервисом для приложения **Yatube**, который настраивает взаимодействие между фронтендом Django-проекта и бэкендом.

## Примеры некоторых запросов к API:
### Получить JWT-токен
Получение JWT-токена.
```
POST http://127.0.0.1:8000/api/v1/jwt/create/
```
```
{
  "username": "string",
  "password": "string"
}
```
### Получение публикаций
Получить список всех публикаций. При указании параметров limit и offset выдача должна работать с пагинацией.
```
GET http://127.0.0.1:8000/api/v1/posts/
```
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
### Добавление комментария
Добавление нового комментария к публикации.
```
POST http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
```
{
  "text": "string"
}
```
### Информация о сообществе
Получение информации о сообществе по id.
```
http://127.0.0.1:8000/api/v1/groups/{id}/
```
```
{
  "id": 0,
  "title": "string",
  "slug": "string",
  "description": "string"
}
```
### Подписка
Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса.
```
http://127.0.0.1:8000/api/v1/follow/
```
```
{
  "following": "string"
}
```

## Как запустить проект:

**Клонировать репозиторий и перейти в него в командной строке:**
```
git@github.com:Denis-Krapp/api_final_yatube.git
```
```
cd api_final_yatube
```
**Cоздать и активировать виртуальное окружение:**
```
py -m venv env
```
```
source venv/Scripts/activate
```
**Установить зависимости из файла requirements.txt:**
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
**Выполнить миграции:**
```
python3 manage.py migrate
```
**Запустить проект:**
```
python3 manage.py runserver
```
