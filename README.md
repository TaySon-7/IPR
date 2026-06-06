# Лабораторная работа №5

Django одностраничный сайт на kubernetes.
## Описание проекта

Реализован frontend для главной страницы, endpoints `/live/` и `/health/`, а также Kubernetes probes для Django и PostgreSQL.

В проекте есть docker-compose1 для отдельного запуска PostgreSQL, docker-compose для полного запуска и бд, и приложения.
Также есть возможность развернуть приложение на kubernetes: есть deployment и service под django и PostgreSQL

## Запуск Kubernetes

Образ приложения находится в Github container registry в публичном доступе.
```commandline
kubectl apply -f k8s/namespace
```
Подставьте свои секреты в файл secrers-example.yml по желанию.
```commandline
kubectl apply -f k8s/base
```
## Разработчик

Туревич Максим
Email: miturevich@mai.education

