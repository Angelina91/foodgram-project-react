# Foodgram-project-react

## _«Продуктовый помощник»_

[![Я|Практикум](https://img.shields.io/badge/-ЯндексПрактикум-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)

![status workflow](https://github.com/Angelina91/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Базовые модели проекта

- краткая информация по проекту ниже
- ✨Magic ✨

## Базовые модели проекта

### Рецепт

> Рецепт должен описываться такими полями:

- Автор публикации (пользователь).
- Название.
- Картинка.
- Текстовое описание.
- Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
- Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
- Время приготовления в минутах.

> Все поля обязательны для заполнения.

### Тэг
> Тег должен описываться такими полями:

- Название.
- Цветовой HEX-код (например, #49B64E).
- Slug.

> Все поля обязательны для заполнения и уникальны.

### Ингредиенты

> Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент должен описываться такими полями:

- Название.
- Количество.
- Единицы измерения.

> Все поля обязательны для заполнения.

## Стек технологий

[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST framework](https://img.shields.io/badge/-Django%20REST%20framework-464646?style=flat&logo=Django%20REST%20framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org)

## Docker & docker-compose

Foodgram-project очень лекго `установить` _(распаковать у себя на сервере)_ `или задеплоить` с помощью Docker, docker-compose.

Поумолчанию Docker будет использовать порт 8080, но это при необходимости можно поменять.

`Поехали!`

- ### Установка Docker (на платформе Ubuntu)

Проект поставляется в четырех контейнерах Docker (db, frontend, backend, nginx).  
Для запуска необходимо установить Docker и Docker Compose.  
Подробнее об установке на других платформах можно узнать на [официальном сайте](https://docs.docker.com/engine/install/).

Для начала необходимо скачать и выполнить официальный скрипт:

```bash
apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

При необходимости удалить старые версии Docker:

```bash
apt remove docker docker-engine docker.io containerd runc 
```

Установить пакеты для работы через протокол https:

```bash
apt update
```

```bash
apt install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y 
```

Добавить ключ GPG для подтверждения подлинности в процессе установки:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Добавить репозиторий Docker в пакеты apt и обновить индекс пакетов:

```bash
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 

```

```bash
apt update
```

Установить Docker(CE) и Docker Compose:

```bash
apt install docker-ce docker compose -y
```

Проверить что  Docker работает можно командой:

```bash
systemctl status docker
```

---

- ### База данных и переменные окружения

Проект использует базу данных PostgreSQL.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в папке "./infra/".

Шаблон для заполнения файла ".env":

```python
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=food_postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1723
DB_HOST=db
DB_PORT=5432
SECRET_KEY='указать ключ'
CONTACT_EMAIL='linatintin@yandex.ru'
ALLOWED_HOSTS=['84.201.158.17', 'localhost', '127.0.0.1', 'backend']
```

---

- ### START-PROJECT

Перед запуском необходимо склонировать проект:

```bash
SSH: git clone git@github.com:Angelina91/foodgram-project-react.git
```

#### :whale: Запуск всех контейнеров

Из директории infra/ выполнить команду

```bash
docker compose up -d --build
```

## Путь до удаленного сервера

```bash
ssh foodgram@84.201.158.17
```

## Автор

# [![Angelina91](https://img.shields.io/badge/-Angelina91-464646?style=flat&logo=Angelina&logoColor=56C0C0&color=000)](https://github.com/Angelina91)
