# Персональний помічник (CLI)

## Локально (pip + venv, Python 3.13)
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python Contact.py

## Docker
docker build -t personal-assistant .
# зайти в контейнер:
docker run -it personal-assistant /bin/bash
# внутри:
python Contact.py

# (опционально) Flask-режим
# docker run -p 5000:5000 -e MODE=flask personal-assistant
