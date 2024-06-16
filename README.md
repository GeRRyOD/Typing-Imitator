# Typing Imitator

Программа Typing Imitator позволяет имитировать статус "печатает" в Telegram для указанных контактов, используя библиотеку Telethon.

## Установка и Запуск

Для установки и запуска Typing Imitator выполните следующие шаги:

### 1. Клонировать репозиторий

```bash
git clone https://github.com/GeRRyOD/typing-imitator.git
cd typing-imitator
```

### 2. Установить зависимости
```
pip install -r requirements.txt
```

### 3. Запустить программу
```
python typing_imitator.py
```

### 4. Первый запуск
При первом запуске программа запросит следующие данные:
1. API ID и API Hash Telegram
   
   Перейдите на сайт my.telegram.org и войдите в систему, используя свой номер телефона.
   
   Выберите "API development tools" и заполните форму для регистрации нового приложения.
   
   Введите в программу сперва API ID, затем API HASH
   
3. Номер телефона для логина: Введите ваш номер телефона, который вы используете для входа в Telegram. Программа автоматически создаст файлы, необходимые для дальнейшей работы.
4. После успешной авторизации программа спросит о желаемом рандомном таймауте отправки команды "typing"
5. Затем программа запрашивает @username или ID пользователей, которым мы будем отправлять статус "typing"
6. В случае, когда все цели выбраны - оставьте поле пустым и нажмите Enter
7. Программа начала свою работу. Для завершения программы отправьте сочетание клавиш ctrl+c в окно терминала
8. Have Fun :)

## 5. Повторный запуск
При повторном запуске приложения Ваша сессия загружается автоматически, от вас требуется только id/username жертвы
