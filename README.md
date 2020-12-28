# python-digitalocean

# Docker auto builds

Docker Hub: https://hub.docker.com/r/sfnagg/python-digitalocean

Рекомендую сохранить API токен в файле и далее забирать ключ из файла, выставить права 600:

`echo XXXXXXXXXXXXXX > ~/.mysecret_api.key`

`chmod 600 ~/.mysecret_api.key`

Создать алиас для команды запуска (~/.bashrc или ~/.zshrc)

alias manage_droplets="docker run -e API_TOKEN=`cat ~/.mysecret_api.key` -e DOMAIN_NAME=my.domain.com -it --rm --name py-do sfnagg/python-digitalocean python manage_droplets.py"

# Docker manual builds

`docker build -t py-do .`

`docker run -e API_TOKEN=XXXXXXXXXXXXXX -e DOMAIN_NAME=my.domain.com -it --rm --name py-do py-do python manage_droplets.py list|create|destroy|dkim|help`

Рекомендую сохранить API токен в файле и далее забирать ключ из файла, выставить права 600:

`echo XXXXXXXXXXXXXX > ~/.mysecret_api.key`

`chmod 600 ~/.mysecret_api.key`

`docker run -e API_TOKEN=`cat ~/.mysecret_api.key` -e DOMAIN_NAME=my.domain.com -it --rm --name py-do py-do python manage_droplets.py list|create|destroy|dkim|help`

Для удобства работы создать алиас:

alias manage_droplets="docker run -e API_TOKEN=XXXXXXXXXXXXXX -e DOMAIN_NAME=my.domain.com -it --rm --name py-do py-do python manage_droplets.py"

# Переменные

Для корректной работы скрипта, требуется указать следующие переменные:
* `API_TOKEN` - API-токен в DigitalOcean  
* `DOMAIN_NAME` - Домен, в котором будут добавлены DNS-записи для дроплетов  

# Использование

* `python manage_droplets.py list` - выведет список дроплетов  
* `python manage_droplets.py create` - попросит ввести короткий хостнейм, после создаст дроплет с CentOS 7 и A-запись в домене (в скобках предложит имя по умолчанию)  
* `python manage_droplets.py destroy` - выведет список дроплетов, попросит указать какой из них нужно удалить, удалит дроплет и A-запись  
* `python manage_droplets.py dkim` - запросит ID дроплета и содержимое DKIM-ключа  
* `python manage_droplets.py help` - помощь по субкомандам  

Пароль root для дроплета приходит на почту аккаунта, через API Token которого он создавался
