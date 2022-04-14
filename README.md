# API-YATUBE

### Краткое описание проекта

Проект представляет собой API-платформу для социальных сетей [YATUBE](https://github.com/Skakovsku/hw05_final.git). Может быть использован веб- и бэкенд-разработчиками с целью поддержки коммуникации пользователей без создания отдельного сервиса, а также для создания возможности корпоративного (группового) общения.

### Установка проекта на локальном компьютере

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Skakovsku/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```
Далее необходимо сгенерировать секретный ключ Django. Для этого при активированном виртуальном окружении в терминале введите следующую команду:

```
(venv) $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Создайте в директории yatube/yatube/ (в одной папке с файлом settings.py) файл с именем .env со следующим содержимым:
```
SECRET_KEY=сгенерированный_ключ
```
Информацию следует печатать без кавычек, скобок и пробелов.

Установить зависимости из файла requirements.txt:

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

### Примеры отправки запросов

- GET-запрос:
```
api/v1/posts/ # Получение полного списка публикаций всех авторов
GET api/v1/posts/2/comments/ # Получение списка коммнетариев к публикации с id=2
```
GET-запросы могут выполняться анонимными пользователями
- POST-запрос:
```
POST api/v1/follow/ # Подписка на автора с id=1. Доступен авторизованному пользователю
Authorization: <Ваш токен>
{
    "following": "<username>"
}
```
- Получение JWT-токена доступно зарегестрированным пользователям по следующему запросу:
```
POST api/lwt/create/
{
    "username": "<username пользователя>",
    "password": "<пароль пользователя username"
}
```
**Более подробную информацию по использованию API-платформы можно получить в _ФАЙЛЕ ДОКУМЕНТАЦИИ_, который будет доступен после запуска проекта на локальном компьютере по _[этой ссылке](http://127.0.0.1:8000/redoc/)_.**