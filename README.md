# [Flask Education App](https://rotor.cloud/) `Курс 'Hello, DevOps!`

Для развертывания этого учебного приложения тебе потребуется сделать несколько действий:

- перейти на правильный сервер базы (зависит от задания)
- установить движок БД
- настроить доступ для нужного пользователя
---
- перейти на правильный сервер приложений (зависит от задания)
- установить библиотеки, которые потребуются для Python
- установить git, чтобы склонировать исходный код приложения
- подтянуть зависимости приложения
- выставить настройки приложения в `.env`-файле, согласно заданию
- проверить работоспособность приложения и запусить его в производственном веб-сервере
---
- перейти на правильный сервер балансировщика (зависит от задания)
- настроить установить и настроить балансировщик


## ⚠️ Внимание! Дальше идет решение.


Если установка с единой компоновкой, мы остаёмся на `controller`, иначе переходим на на `db01`
---

```
ssh db01
```

Установка MySQL
---

```
curl  -L  https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm  -O
sudo  dnf  install  -y  mysql80-community-release-el9-1.noarch.rpm
sudo  dnf  install  -y  mysql-server
sudo  systemctl  start  mysqld
sudo  systemctl  enable  mysqld
```

Получение root-пароля MySQL
---

```
sudo  cat  /var/log/mysqld.log
```

Зайти в консоль MySQL, используя пароль root
---

```
mysql  -uroot  -p
```

Установить новый пароль root
---

```
ALTER  USER  "root"@"localhost"  IDENTIFIED  BY  "DBs123!@#";
```

Создать пользователя (локального или глобального) и дать ему привилегии для базы. 
---

```
CREATE USER  "produser"@"localhost"  IDENTIFIED  BY  "rea11yStrongAndl0ngPass#ord";
GRANT  ALL PRIVILEGES  ON  shop.*  TO  "produser"@"localhost";
```

>‼️ Пользователь и база в задании могут быть другими!


Если установка с распределенной компоновкой, мы переходим на `srv01`
---

```
ssh  produser@srv01
```

Установка зависимостей Python
---

```
sudo  yum  -y  install  gcc  python-devel mysql-devel 
```

Установка Git и скачивание кода
---

```
sudo  yum  -y  install  git 
git  clone  https://github.com/rotoro-cloud/ecommerce-flask-stripe.git
```

Если пользователь службы будет отличаться от залогиненого, стоит действовать от лица того юзера
---

```
sudo  mv  ecommerce-flask-stripe/  /opt/ecommerce-flask-stripe/
sudo  chown  -R  regularuser:regularuser  /opt/ecommerce-flask-stripe/
su regularuser
```

Разрешение зависимостей приложения
---

```
cd  /opt/ecommerce-flask-stripe/
pip  install  -r  requirements.txt
```

Настройка приложения
---

```
cp  env.sample  .env
vi  .env
```

>🖊️ Исправь данные на те, которые раньше установил в `MySQL`

Запусти девелоперский сервер для проверки (порт 8080 может быть уже занят)
---

```
flask  run  --host="0.0.0.0"  --port="9090"
```

>‼️ Сделай `curl localhost:9090`, если он загружает страницу, значит связь с базой настроена верно.

Проверь запуск приложения в продуктовом веб-сервере, настройка gunicorn через файл `gunicorn.conf.py`
---

```
gunicorn  run:app
```

>‼️ Сделай `curl localhost:5005`, если он загружает страницу, значит связь с базой настроена верно.

Создай файл службы для `gunicorn`
---

>‼️ Следуй этому шаблону для файла `/etc/systemd/system/ecommerce.service`
```
[Unit]
Description=Gunicorn-server for ecommerce
After=network.target

[Service]
User=regularuser
WorkingDirectory=/opt/ecommerce-flask-stripe/
ExecStart=/home/regularuser/.local/bin/gunicorn run:app

[Install]
WantedBy=multi-user.target
```

Активация службы веб-приложения
---

```
sudo systemctl  start  ecommerce
sudo systemctl  enable  ecommerce
```

Если установка с распределенной компоновкой, мы переходим на `controller`
Устанавливаем Nginx
---

```
sudo dnf install nginx;
```

Настраиваем Nginx. Файл настроек есть в репо проекта в папке `nginx`, его нужно скопировать на машину с балансировщиком или создать вручную
---

`vi /etc/nginx/conf.d/appseed-app.conf`

```
upstream webapp {
    server localhost:5005;
}

server {
    listen 8000;
    server_name localhost;

    location / {
        proxy_pass http://webapp;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
```
>‼️ `server localhost:5005;` в одночной компоновке нужно изменить на `server app01:5005;` в распределенной

Запускаем Nginx
---

```
sudo systemctl enable nginx --now
```

## Теперь, если все сделано верно, приложение можно открыть через браузер



## ✨ Структура кода

```bash
< PROJECT ROOT >
   |
   |-- app/__init__.py
   |-- app/
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/
   |    |    |
   |    |    |-- includes/                 # Page chunks, components
   |    |    |    |-- navigation.html      # Top bar
   |    |    |    |-- sidebar.html         # Left sidebar
   |    |    |    |-- scripts.html         # JS scripts common to all pages
   |    |    |    |-- footer.html          # The common footer
   |    |    |
   |    |    |-- layouts/                  # App Layouts (the master pages)
   |    |    |    |-- base.html            # Used by common pages like index, UI
   |    |    |    |-- base-fullscreen.html # Used by auth pages (login, register)
   |    |    |
   |    |    |-- products/                        # Define your products here
   |    |    |    |-- nike-goalkeeper-match.json  # Sample product
   |
   |-- requirements.txt
   |
   |-- run.py
   |
   |-- ************************************************************************
```

<br />

## ✨ Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The official website
- [Stripe Dev Tools](https://stripe.com/docs/development) - official docs

<br />

---
