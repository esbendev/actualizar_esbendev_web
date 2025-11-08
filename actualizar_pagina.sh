#!/bin/bash

# me aseguro que los repos estén up to date
cd ~/esbendev/repos/esbendev.github.io
git pull

# instrucciones previas porque ahora uso playwright en docker
kitty sh -c "sudo systemctl start docker; docker run -p 3000:3000 --rm --init -it   --workdir /home/pwuser --user pwuser   mcr.microsoft.com/playwright:v1.52.0-noble   npx -y playwright@1.52.0 run-server --port 3000 --host 0.0.0.0" &

read -p "presionar enter cuando termine de abrir docker..."

# corro programa para actualizar videos
cd ~/esbendev/repos/actualizar_esbendev_web
source venv/bin/activate
#python3 main.py
python3 main_with_docker.py
deactivate

# subo cambios a github
cd ~/esbendev/repos/esbendev.github.io
git add .
git commit -m "bot: actualizo videos"
git push
