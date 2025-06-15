# CarSpecialistBot

Telegram-бот + API + парсинг Drom.

## Возможности
- **Парсинг объявлений** с Drom.ru (цена, характеристики, контакты и др.)
- **Анализ вопросов** об автомобилях (интеграция с внешним API)

## Установка
1. Склонируйте репозиторий:
   ```
      git clone https://github.com/LenaNS/DromParsingBot.git
   ```
   
2. Соберите образ
   ```
      docker build --tag drom-parsing-bot:0.1 /path/to/Dockerfile
   ```
   
3. Запустите контейнер
   ```
      docker run drom-parsing-bot:0.1
   ```
   
4. Добавьте бота в telegram.

- Найдите бота по username @CarSpecialistBot
- Отправьте команду: '\start'

## Технологии
- **Python 3.12** 
- **Aiogram 3.20.0.post0** 
- **httpx** 
- **playwright**

## Команды бота
- **/start — приветствие и список команд.** 
- **/ask — задать вопрос об автомобиле.** 
- **/parse — парсинг объявления с Drom.ru (ссылка → данные).**




