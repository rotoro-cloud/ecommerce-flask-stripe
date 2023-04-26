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
- выставить настройки приложения в `.env`-файле, сог
---
- настроить файрволл(ы)


## ⚠️ Внимание! Дальше идет решение.


Если установка с единой компоновкой, мы переходим на `srv01`, иначе на `db01`

```
ssh produser@srv01
```

Установка Mysql
---
```
curl  -L  https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm  -O
sudo dnf  install  mysql80-community-release-el9-1.noarch.rpm -y
sudo dnf  install  mysql-server  -y
sudo systemctl  start  mysqld
sudo systemctl  enable  mysqld
```

Получение root-пароля Mysql
---

```
sudo  cat  /var/log/mysqld.log
```

Настройка базы
---

```
CREATE  USER  "produser"@"%"  IDENTIFIED  BY  "rea11yStrongAndl0ngPassvvord";
GRANT  ALL PRIVILEGES  ON  ecommerce.*  TO  "produser"@"%";
```

>❗ Пользователь в задании может быть другим!


Если установка с распределенной компоновкой, мы переходим на `app01`

```
ssh  produser@app01
```


Установка зависимостей Python
---
```
sudo  yum  -y  install  gcc  python-devel mysql-devel 
```

Установка Git
---
```
sudo  yum  install  git  -y
git  clone  https://github.com/rotoro-cloud/ecommerce-flask-stripe.git
```

Разрешение зависимостей приложения
---
```
mv  ecommerce-flask-stripe/ ecommerce
cd  ecommerce-flask-stripe/
pip  install  -r  requirements.txt
```

Установка переменных окружения приложения
---
```
cp  env.sample  .env
vi  .env
```

>🖊️ Исправь данные на те, которые раньше установил в `MySQL`

Запусти девелоперский сервер для проверки
---
```
flask  run  --host="0.0.0.0"  --port="9090"
```

>‼️ Зайди в браузер, если ты видишь страницу, значит связь с базой настроена верно.

Проверь запуск приложения в продуктовом веб-сервере с 3-я вокрерами
---
```
gunicorn  --bind  0.0.0.0:9090  run:app  -w  3
```

Создай файл службы для `gunicorn`
---
>‼️ Следуй этому шаблону для файла `/etc/systemd/system/ecommerce.service`
```
[Unit]
Description=Gunicorn-server for ecommerce
After=network.target

[Service]
User=produser
WorkingDirectory=/home/produser/ecommerce
ExecStart=gunicorn --bind  0.0.0.0:9090  run:app  -w  3

[Install]
WantedBy=multi-user.target
```

Активация службы веб-сервера
---
```
sudo systemctl  start  mysqld
sudo systemctl  enable  mysqld
```


:TODO ПРОВЕРИТЬ! ПОХЖЕ НФТЭЙБЛ только в виртуалке!

Попробуем uncomlicated - пок не проверено

На вебе
sudo ufw default deny
sudo ufw allow 9090
sudo ufw allow 22
sudo ufw enable

На базе
sudo ufw default deny
sudo ufw allow from app01 to any port 3306
sudo ufw allow 22
sudo ufw enable


Установи FirewallD на нужных серверах
---
```
sudo  yum  install  -y  firewalld
sudo  service  firewalld  start
sudo  systemctl  enable  firewalld
```

##### sudo firewall-cmd --zone=public --add-port=5000/tcp

Настрой FirewallD для базы и продуктового веб-сервера
---






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
