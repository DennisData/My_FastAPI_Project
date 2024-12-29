## todo-service

### Загрузка с DockerHub пока недоступна, предлагается загрузить образ из GitHub

После скачивания необходимо выполнить (внутри директории Short_URL)
1. Сборка контейнера
docker build -t todo-service-image .

2. Команда для запуска контейнера
docker run --name todo-app -p 10001:10001 -d -v .:/app todo-service-image

3. (опционально) Войти внутрь контейнера
docker exec -it todo-app bash

Доступ: 0.0.0.0:10001