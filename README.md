# praktikum_new_diplom

# Для примера
# yamdb_final

![status workflow](https://github.com/Angelina91/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Краткое описание проекта
YaMDb_final - программный интерфейс для социальной сети.
Он позволяет неравнодушным творческим людям обсудить заинтересовавшие их произведения: оставить отзывы к книгам, фильмам и т.д. и прокоментировать уже существующие отзывы

## Документация

[redoc](http://84.201.158.17/redoc/)
## :dash: Установка и запуск проекта

### :dancers: Клонирование репозитория

git clone [SSH](git@github.com:Angelina91/yamdb_final.git)

### :whale: Запуск всех контейнеров

Из директории infra/ выполнить команду

```bash
docker-compose up -d --build
```

### :feet: Выполнить миграции

```bash
docker-compose exec web python manage.py migrate
```

### :bowtie: Создать суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

### :crystal_ball: Собрать статику

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

### :love_letter: Заполнить базу данных

```bash
docker-compose exec web python manage.py loaddata ../infra/fixtures.json
```

## :dizzy: Стек

_Python,
Rest Api,
Docker,
PostgreSQL,
Redoc,
Django,
djangorestframework_

## Путь до удаленного сервера

```bash
ssh angelina91@84.201.158.17
```

## Автор

[Angelina91](https://github.com/Angelina91)
