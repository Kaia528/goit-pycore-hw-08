#!/usr/bin/env bash
set -e

if [ "$MODE" = "flask" ]; then
  export FLASK_APP=Doc.py     # если у тебя главный Flask-файл другой — подставь его
  flask run --host=0.0.0.0 --port=5000
else
  python Contact.py           # CLI-помощник (подставь своё имя файла, если иное)
fi
