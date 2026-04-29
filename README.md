# Лабораторная работа №6

Django одностраничный сайт на kubernetes.
## Описание проекта

Реализовано 2 views /home и /health


## Запуск Kubernetes

### Сначала запускаете инфраструктуру

1. База данных вынесена как отдельная инфраструктура в infra:
- infra/helm
- infra/kustomization

# PostgreSQL Infrastructure

## Контракт для приложения

| Параметр | Dev                                            | Prod                                             |
|----------|------------------------------------------------|--------------------------------------------------|
| Хост | postgres-0.postgres.django-demo.svc.cluster.local | postgres-0.postgres.prod.svc.cluster.local       |
| Порт | 5432                                           | 5432                                             |
| База | django-db                                      | django-db                                        |
| Пользователь | postgres                                       | postgres                                         |
| Пароль | В Secret `dev-password` namespace `django-dev` | В Secret `prod-password` namespace `django-prod` |

перейдите в каталог postgres-infra: 

для запуска через helm:

dev-запуск
```commandline
helm upgrade --install postgrerd-db . --namespace=django-dev --create-namespace -f values-dev.yaml
```

prod-запуск
```commandline
helm upgrade --install postgrerd-db . --namespace=django-prod --create-namespace -f values-prod.yaml
```

для запуска через kustomize:
перейдите в каталог infra/:
dev-запуск:
создайте namespace 
```commandline
kubectl create namespace django-dev
```

```commandline
kubectl apply -k kustomization/overlays/dev
```

prod-запуск:
создайте namespace 
```commandline
kubectl create namespace django-prod
```

```commandline
kubectl apply -k kustomization/overlays/prod
```

### Длаее запускаете приложение

2. Django сайт в k8s:
- k8s/helm
- k8s/kustomization

перейдите в каталог k8s/helm/django-app: 

для запуска через helm:

dev-запуск
```commandline
helm upgrade --install django-app . --set django.SECRET_KEY="your_key" --namespace=django-dev --create-namespace -f values-dev.yaml
```

prod-запуск
```commandline
helm upgrade --install django-app . --set django.SECRET_KEY="your_key" --namespace=django-prod --create-namespace -f values-prod.yaml
```

для запуска через kustomize:
перейдите в каталог k8s/
Если инфраструктуру запускали через kustomization, то namespace создавать уже не надо.

dev-запуск:
создайте namespace 
```commandline
kubectl create namespace django-dev
```

```commandline
kubectl apply -k kustomization/overlays/dev
```

prod-запуск:
создайте namespace 
```commandline
kubectl create namespace django-prod
```

```commandline
kubectl apply -k kustomization/overlays/prod
```

## Разработчик

Туревич Максим
Email: miturevich@mai.education


