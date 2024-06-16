import asyncio
import random
import json
from telethon import TelegramClient, errors
from telethon.tl.types import PeerUser
import datetime
from dotenv import load_dotenv, set_key
import os

# Цвета ANSI для красного, зеленого и сброса цвета
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ASCII-арт "Typing Imitator"
ASCII_ART = r"""
 _______                _                 _____             _  _           _                
|__   __|              (_)               |_   _|           (_)| |         | |               
   | |    _   _  _ __   _  _ __    __ _    | |   _ __ ___   _ | |_   __ _ | |_   ___   _ __ 
   | |   | | | || '_ \ | || '_ \  / _` |   | |  | '_ ` _ \ | || __| / _` || __| / _ \ | '__|
   | |   | |_| || |_) || || | | || (_| |  _| |_ | | | | | || || |_ | (_| || |_ | (_) || |   
   |_|    \__, || .__/ |_||_| |_| \__, | |_____||_| |_| |_||_| \__| \__,_| \__| \___/ |_|   
           __/ || |                __/ |                                                    
          |___/ |_|               |___/                                                     
"""

# Имя файла для хранения конфигурации
env_file = ".env"

async def main():
    # Выводим ASCII-арт при запуске программы
    print(f"{GREEN}{ASCII_ART}{RESET}")

    # Выводим сообщение о запуске программы с зеленым цветом
    print(f"{GREEN}Программа Typing Imitator запущена. Для завершения нажмите Ctrl+C.{RESET}")
    
    # Загружаем конфигурацию или запрашиваем у пользователя, если она отсутствует или неполная
    config = load_config()

    if not config or "API_ID" not in config or "API_HASH" not in config:
        config = await setup_config()

    # Запрашиваем задержку между действиями
    min_delay, max_delay = await get_delay_range()

    # Создаем клиента Telegram
    client = TelegramClient("anon", config["API_ID"], config["API_HASH"])
    
    try:
        # Запускаем клиента Telegram
        await client.start()

        # Основной цикл для ввода ID или username пользователей
        while True:
            user_inputs = []
            while True:
                user_input = input("Введите ID пользователя или username (пустой ввод для завершения): ").strip()
                if not user_input:
                    break
                user_inputs.append(user_input)

            if user_inputs:
                # Обрабатываем каждый введенный ID или username асинхронно
                await asyncio.gather(*[handle_user(client, user_input, min_delay, max_delay) for user_input in user_inputs])
                print(f"{GREEN}Все запросы обработаны.{RESET}")
            else:
                break

    except KeyboardInterrupt:
        # Перехватываем KeyboardInterrupt (нажатие Ctrl+C) для корректного завершения программы
        print(f"\n{RED}Программа завершена пользователем.{RESET}")
    except Exception as e:
        # Обработка остальных исключений
        print(f"{RED}Произошла ошибка при подключении к Telegram: {e}{RESET}")
    finally:
        # Отключаем клиента Telegram и выводим сообщение о завершении программы
        await client.disconnect()
        print(f"{GREEN}Программа завершена.{RESET}")

async def handle_user(client, user_input, min_delay, max_delay):
    try:
        # Получаем сущность пользователя по введенному ID или username
        if user_input.isdigit():
            entity = await client.get_input_entity(PeerUser(int(user_input)))
        else:
            entity = await client.get_entity(user_input)

        while True:
            try:
                # Отправляем статус 'typing' для пользователя с заданной задержкой
                async with client.action(entity, 'typing'):
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"{GREEN}[{current_time}] Отправлен статус 'typing' для {user_input}.{RESET}")
                    await asyncio.sleep(random.uniform(min_delay, max_delay))  # Рандомная задержка в заданном диапазоне
            except errors.FloodWaitError as e:
                # Обработка ошибки FloodWaitError (слишком много запросов)
                print(f"{RED}Flood wait: ждём {e.seconds} секунд.{RESET}")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                # Обработка других ошибок
                print(f"{RED}Ошибка: {e}{RESET}")
                await asyncio.sleep(10)  # Ждем 10 секунд перед повторной попыткой

    except ValueError:
        # Обработка ошибки неверного ID или username
        print(f"{RED}Не удалось найти пользователя с ID или username {user_input}.{RESET}")
        return
    except errors.UserNotMutualContactError:
        # Обработка ошибки, когда пользователь не является взаимным контактом
        print(f"{RED}Пользователь {user_input} не является вашим взаимным контактом.{RESET}")
        return
    except Exception as e:
        # Общая обработка других исключений
        print(f"{RED}Произошла ошибка при получении пользователя {user_input}: {e}{RESET}")
        return

def load_config():
    # Загрузка конфигурации из файла .env
    load_dotenv(env_file)
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if api_id and api_hash:
        return {
            "API_ID": api_id,
            "API_HASH": api_hash
        }
    return None

async def setup_config():
    # Запрос API ID и API Hash у пользователя, сохранение в .env
    while True:
        api_id = input("Введите API ID: ").strip()
        api_hash = input("Введите API Hash: ").strip()

        if api_id.isdigit() and api_hash:
            config = {
                "API_ID": api_id,
                "API_HASH": api_hash
            }
            
            save_config(config)  # Сохранение конфигурации в файл .env
            return config
        else:
            print("Неверный формат API ID или API Hash. Пожалуйста, введите корректные значения.")

def save_config(config):
    # Сохранение конфигурации в файл .env
    set_key(env_file, "API_ID", config["API_ID"])
    set_key(env_file, "API_HASH", config["API_HASH"])

async def get_delay_range():
    # Запрос диапазона задержки у пользователя
    while True:
        delay_input = input("Введите диапазон задержки между действиями в формате 'мин_задержка, макс_задержка' (пустой ввод для значений по умолчанию 5, 20): ").strip()
        if not delay_input:
            return 5, 20

        try:
            min_delay, max_delay = map(int, delay_input.split(','))
            return min_delay, max_delay
        except ValueError:
            print("Неверный формат ввода. Пожалуйста, введите числа через запятую.")

if __name__ == "__main__":
    # Запускаем основную функцию с использованием asyncio.run
    asyncio.run(main())
