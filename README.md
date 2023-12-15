# api_yamdb

api_yamdb - комадный проект, веб-приложение для отзывов и рецензий

## Используемые технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)
](https://www.django-rest-framework.org/)
[![Postman](https://img.shields.io/badge/-Postman-464646?style=flat&logo=Postman&logoColor=56C0C0&color=008080)
](https://www.postman.com/)



### работа с GIT

Создание ветки и одновременный переход в нее:

```
git checkout -b branchname
```

Связь ветки с удаленным репозиторием.

```
git push -u origin branchname
```

Последовательность действий перед пушем в удаленный репозиторий:

Добавляем файлы:

```
git add .
```

или

```
git add filename
```

Описываем изменения:

```
git commit -m "message about changes"
```

Пушим:

```
git push
```

или

```
git push -u origin branchname
```

Далее на github создаем pull request, после одобрения и мерджа
переходим в другую ветку, а старую удаляем.

```
git branch -d branchname
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:GrebenschikovDI/api_yamdb.git
```

``` 
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Создание суперпользователя
- В директории с файлом manage.py выполнить команду
```
python manage.py createsuperuser
```
- Заполнить поля в терминале
```
Username: <ваше_имя>
Email address: <ваш_email>
Password: <ваш_пароль>
Password (again): <ваш_пароль>
```
## Регистрация нового пользователя
- Передать на эндпоинт 127.0.0.1:8000/api/v1/auth/signup/ **username** и **email**
- Получить код подтверждения на переданный **email**. Права доступа: Доступно без токена. Использовать имя 'me' в качестве **username** запрещено. Поля **email** и **username** должны быть уникальными. 

## Получение JWT-токена
- Передать на эндпоинт 127.0.0.1:8000/api/v1/auth/token/ **username** и **confirmation** code из письма. Права доступа: Доступно без токена.

## Примеры запросов
- Отправить POST-запрос на адрес http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ и передать поле text и поле score <br>
Пример запроса на создание отзыва: 
```
{
"text": "Отзыв на произведение",
"score": 5
}
```
Пример ответа: 
```
{
"id": 0,
"text": "Отзыв на произведение",
"author": "voronovsv",
"score": 5,
"pub_date": "2019-08-24T14:15:22Z"
}
```
- Отправить POST-запрос на адрес http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ и передать поле text <br>
Пример запроса на создание комментария к отзыву:
```
{
"text": "Классный отзыв!"
}
```
Пример ответа:
```
{
"id": 0,
"text": "Классный отзыв!",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```
## Полная документация к API проекта:

Перечень запросов к ресурсу можно посмотреть в описании API

```
http://127.0.0.1:8000/redoc/
```
## Над проектом работали
<br>[Кирилл Козлов](https://github.com/Deyterriy)</br>
<br>[Дмитрий Гребенщиков](https://github.com/GrebenschikovDI)</br>
<br>[Евгений Реутов](https://github.com/EvReutov23)</br>
