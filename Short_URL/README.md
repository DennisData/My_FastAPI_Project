## short-url-service

### Загрузка с DockerHub пока недоступна, предлагается загрузить образ из GitHub

После скачивания необходимо выполнить (внутри директории Short_URL)
1. Сборка контейнера
docker build -t short-url-service-image .

2. Команда для запуска контейнера
docker run --name short-url-app -p 10002:10002 -d -v .:/app short-url-service-image

3. (Опционально) Войти внутрь контейнера
docker exec -it short-url-app bash

Доступ: 0.0.0.0:10002