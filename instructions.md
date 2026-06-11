1 - Container & Image Prune

```
docker rm -vf $(docker ps -aq)

docker rmi -f $(docker images -aq)

```

2 - Clean Docker Volume

```

docker volume rm $(docker volume ls -qf dangling=true)

docker volume prune

```

3 - Dentro da raiz do projeto do bookstore, rode:

```

docker-compose up -d --build 

```

4 - Execute as migrações do Django

```
docker-compose exec web python manage.py migrate

```

5 - Para executar os testes dentro do Docker

```
docker-compose exec web python manage.py test

```
