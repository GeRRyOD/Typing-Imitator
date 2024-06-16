#!/bin/bash

# Установка Python зависимостей
echo "Установка Python зависимостей..."
pip install -r requirements.txt

# Проверка наличия config.json и предложение настроить, если его нет
if [ ! -f "config.json" ]; then
    echo "Файл config.json не найден."
    echo "Пожалуйста, введите API ID и API Hash для Telegram:"
    read -p "API ID: " api_id
    read -p "API Hash: " api_hash
    echo "{\"API_ID\": \"$api_id\", \"API_HASH\": \"$api_hash\"}" > config.json
    echo "Файл config.json создан и заполнен."
fi

# Запуск программы
echo "Запуск программы Typing Imitator..."
python main.py

echo "Программа завершена."
