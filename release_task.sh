#!/bin/bash
echo Reinstalling jieba
pip3 install --upgrade --force-reinstall jieba
echo Running migration
python manage.py migrate
