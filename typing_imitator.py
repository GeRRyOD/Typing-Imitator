import asyncio
import random
import os
from dotenv import load_dotenv
from telethon import TelegramClient, errors
from telethon.tl.types import PeerUser
import sys
import datetime

# Цвета ANSI для красного, зеленого и сброса цвета
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

async def main():
    print(f"{GREEN}Программа Typing Imitator запущена. Для завершения нажмите Ctrl+C.{RESET}")

    # Загрузка конфигурационных данных из .env файла
    load_dotenv()
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        config = await setup_config()
        api_id = config["API_ID"]
        api_hash = config["API_HASH"]

    # Запрашиваем задержку между действиями
    min_delay, max_delay = await get_delay_range()

    # Создаем клиента Telegram
    client = TelegramClient("anon", api_id, api_hash)
    
    try:
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
                await asyncio.gather(*[handle_user(client, user_input, min_delay, max_delay) for user_input in user_inputs])
                print(f"{GREEN}Все запросы обработаны.{RESET}")
            else:
                break

    except KeyboardInterrupt:
        print(f"\n{RED}Программа завершена пользователем.{RESET}")
    except Exception as e:
        print(f"{RED}Произошла ошибка при подключении к Telegram: {e}{RESET}")
    finally:
        await client.disconnect()
        print(f"{GREEN}Программа завершена.{RESET}")

async def handle_user(client, user_input, min_delay, max_delay):
    try:
        if user_input.isdigit():
            entity = await client.get_input_entity(PeerUser(int(user_input)))
        else:
            entity = await client.get_entity(user_input)

        while True:
            try:
                async with client.action(entity, 'typing'):
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"{GREEN}[{current_time}] Отправлен статус 'typing' для {user_input}.{RESET}")
                    await asyncio.sleep(random.uniform(min_delay, max_delay))
            except errors.FloodWaitError as e:
                print(f"{RED}Flood wait: ждём {e.seconds} секунд.{RESET}")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"{RED}Ошибка: {e}{RESET}")
                await asyncio.sleep(10)

    except ValueError:
        print(f"{RED}Не удалось найти пользователя с ID или username {user_input}.{RESET}")
        return
    except errors.UserNotMutualContactError:
        print(f"{RED}Пользователь {user_input} не является вашим взаимным контактом.{RESET}")
        return
    except Exception as e:
        print(f"{RED}Произошла ошибка при получении пользователя {user_input}: {e}{RESET}")
        return

async def setup_config():
    while True:
        api_id = input("Введите API ID: ").strip()
        api_hash = input("Введите API Hash: ").strip()

        if api_id.isdigit() and api_hash:
            save_config(api_id, api_hash)
            return {
                "API_ID": api_id,
                "API_HASH": api_hash
            }
        else:
            print("Неверный формат API ID или API Hash. Пожалуйста, введите корректные значения.")

def save_config(api_id, api_hash):
    with open(".env", "w") as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")

async def get_delay_range():
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{RED}Произошла ошибка: {e}{RESET}")
