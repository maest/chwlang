#!/bin/bash
echo Reinstalling jieba
pip install --upgrade --force-reinstall jieba
echo Running migration
python manage.py migrate
