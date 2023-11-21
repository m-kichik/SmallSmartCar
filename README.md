# SmallSmartCar
![pixel_car](media/car_and_apple_white.png)

**Сборка десктопной версии (не на jetbot)**
- Сборка контейнера:
```bash
docker build . \
        -f docker/Dockerfile.x86_64 \
        -t x86_64_smallcar/smallcar_desktop:latest \
        --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```
- Запуск контейнера:
```bash
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
docker exec --user "docker_smallcar_desktop" -it smallcar_desktop \
        /bin/bash -c "cd /home/docker_smallcar_desktop/dev/SmallSmartCar; /bin/bash"
```
