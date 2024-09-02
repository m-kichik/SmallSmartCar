# SmallSmartCar
![pixel_car](media/car_and_pyramid.png)

Репозиторий содержит код для запуска телеграм-бота SmartSmallCar, который умеет обрабатывать голосовые и текстовые команды из набора "поверни направо/налево", "едь вперёд/назад", "сделай фото", на русском языке (формулировки не обязаны совпадать) и передавать их на исполнение, находясь на борту [Jetbot Nano](https://jetbot.org/master/). В тестовом режиме запускается из докера на любой машине с x86_64. Обработка команд построена на if-else и re, исполнение команд реализовано с использованием библиотеки jetbot. Для логирования команд используется база данных sqlite3, также доступны тесты бота (unittest).

Демо работы:

https://github.com/m-kichik/SmallSmartCar/assets/74000706/2a36bfb2-12a6-44fa-923c-f0546d223eaa



**Запуск десктопной версии**

Запуск в тестовом режиме доступен в двух вариантах:
1. Запуск из докер-контейнера;
2. Запуск из виртуальной среды.

**Запуск десктопной версии из контейнера**
- Клонирование репозитория:
```bash
git clone https://github.com/m-kichik/SmallSmartCar
```
- Сборка контейнера:
```bash
cd SmallSmartCar
docker build . \
        -f docker/Dockerfile.x86_64 \
        -t x86_64_smallcar/smallcar_desktop:latest \
        --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```
- Запуск контейнера:
```bash
cd SmallSmartCar
docker run -it -d --rm \
        --env="DISPLAY=$DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --privileged \
        --name smallcar_desktop \
        --net=host --ipc=host --pid=host \
        -v `pwd`/source:/home/docker_smallcar_desktop/dev/SmallSmartCar \
        x86_64_smallcar/smallcar_desktop:latest
```
- Вход в контейнер:
```bash
cd SmallSmartCar
docker exec --user "docker_smallcar_desktop" -it smallcar_desktop \
        /bin/bash -c "cd /home/docker_smallcar_desktop/dev/SmallSmartCar; /bin/bash"
```
- Запуск бота. Перед запуском необходимо скопировать файл credentials_template.py модуля smallcarbot в credentials.py того же модуля и спецализировать токен и юзернейм.
```bash
python app.py
```

**Запуск десктопной версии с использованием venv**

Тестовая версия имеет зависимости, обозначенные в requirements.txt и требование к python: 3.8+. Для запуска бота необходимо выполнить следующее:
- Клонирование репозитория:
```bash
git clone https://github.com/m-kichik/SmallSmartCar
```
- Создание venv и установка зависимостей:
```bash
cd SmallSmartCar
python3.10 -m venv botenv
source botenv/bin/activate
pip install requirements.txt
```
- Запуск бота. Перед запуском необходимо скопировать файл credentials_template.py модуля smallcarbot в credentials.py того же модуля и спецализировать токен и юзернейм.
```bash
cd source
python app.py
```

**Запуск на Jetbot Nano**

Запуск на роботе Jetbot Nano возможен только из виртуального окружения. Системные требования совпадают с требованиями к десктопной версии, 
однако для выполнения некоторых вызовов использован системный интерпретатор python3.6.9. Очень важно, чтобы системный интерпретатор на борту 
робота поддерживал вызовы библиотеки jetbot. Установка и запуск сводятся к выполнению следующих команд:
- Клонирование репозитория:
```bash
git clone https://github.com/m-kichik/SmallSmartCar
```
- Создание venv и установка зависимостей:
```bash
cd SmallSmartCar
python3.8 -m venv botenv
source botenv/bin/activate
pip install requirements_jetbot.txt
```
- Запуск бота. Перед запуском необходимо скопировать файл credentials_template.py модуля smallcarbot в credentials.py того же модуля и спецализировать токен и юзернейм.
```bash
cd source
python app.py --on_board
```
Флаг **--on_board** соответствует запуску на борту робота (без этого флага приложение будет запущено в тестовом режиме). Не включайте при запуске на обычной машине.

