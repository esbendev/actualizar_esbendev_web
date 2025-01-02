#!/bin/bash

# corro programa para actualizar videos
cd ~/esbendev/repos/actualizar_esbendev_web
source venv/bin/activate
python3 main.py
deactivate

# subo cambios a github
cd ~/esbendev/repos/esbendev.github.io
git add .
git commit -m "bot: actualizo videos"
git push
