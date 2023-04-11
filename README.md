# sb-api-tests

Для локального запуска необходим локально установленный Docker.

Перед запуском необходимо собрать образ командой:

```
docker build -t sb-api-tests:latet .
```

Далее необходимо запустить контейнер, смонтировав текущую директорию с кодом в контейнер (для получения логов):

**Windows PowerShell**:

```
docker run --rm -v ${PWD}:/usr/src/app sb-api-tests:latest
```

**Windows cmd**:

```
docker run --rm -v %cd%:/usr/src/app sb-api-tests:latest
```

**Linux**:

```
docker run --rm -v $(pwd):/usr/src/app sb-api-tests:latest
```

В результате выполнения в текущей директории будет создана директория reports, в которой будет лежать html-отчет