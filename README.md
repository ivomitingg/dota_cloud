🎮 Dota 2 Stats Telegram Bot
A Telegram bot that provides detailed statistics for Dota 2 players. Get match history, KDA, hero rankings, and player profiles right in your messenger.

📋 Features
📊 Match Statistics – View last 10 matches with KDA and results

🏆 Top Heroes – Best heroes by winrate and games (minimum 30 matches)

👤 Player Profile – Nickname, rank, MMR, total games, winrate, last match

✅ Registration – Link your Steam ID to your Telegram account

🔄 Auto-update – Always fresh data from OpenDota API

🛠️ Tech Stack
Python 3.9+

python-telegram-bot – Telegram API wrapper

OpenDota API – Dota 2 statistics source

Requests – HTTP client for API calls

🚀 Installation
Clone the repository

bash
git clone https://github.com/ivomitingg/dota-stats-bot.git
cd dota-stats-bot
Install dependencies

bash
pip install -r requirements.txt
Create config file

bash
echo 'TOKEN = "your_bot_token_here"' > config.py
Run the bot

bash
python test_tg.py
📝 Commands
Command	Description
/start	Show main menu
/register {ID}	Link your Steam ID
/stats	Show match statistics
/heroes	Show top heroes
/profile	Show detailed profile
/myid	Show your saved ID
/unregister	Unlink your account
🔒 Security
Your bot token stored in separate config.py file (excluded from Git)

User data stored locally in dota_bot_data/ folder

No data shared with third parties

👨‍💻 Developer
ivomiting – Telegram

📄 License
MIT License – feel free to use and modify!

🎮 Telegram-бот для статистики Dota 2
Телеграм-бот, который показывает детальную статистику игроков Dota 2. История матчей, KDA, рейтинг героев и профиль игрока — всё в одном месте.

📋 Возможности
📊 Статистика матчей – Последние 10 игр с KDA и результатами

🏆 Топ героев – Лучшие герои по винрейту и количеству игр (минимум 30 матчей)

👤 Профиль игрока – Ник, звание, MMR, общее количество игр, винрейт, последняя игра

✅ Регистрация – Привязка Steam ID к аккаунту Telegram

🔄 Автообновление – Всегда свежие данные из OpenDota API

🛠️ Технологии
Python 3.9+

python-telegram-bot – Обёртка для Telegram API

OpenDota API – Источник статистики Dota 2

Requests – HTTP-клиент для запросов к API

🚀 Установка
Клонируйте репозиторий

bash
git clone https://github.com/ivomitingg/dota-stats-bot.git
cd dota-stats-bot
Установите зависимости

bash
pip install -r requirements.txt
Создайте файл конфигурации

bash
echo 'TOKEN = "токен_вашего_бота"' > config.py
Запустите бота

bash
python test_tg.py
📝 Команды
Команда	Описание
/start	Главное меню
/register {ID}	Привязать Steam ID
/stats	Показать статистику матчей
/heroes	Показать топ героев
/profile	Показать подробный профиль
/myid	Показать сохранённый ID
/unregister	Отвязать аккаунт
🔒 Безопасность
Токен бота хранится в отдельном файле config.py (исключён из Git)

Данные пользователей хранятся локально в папке dota_bot_data/

Данные не передаются третьим лицам

👨‍💻 Разработчик
ivomiting – Telegram

📄 Лицензия
MIT License – свободно используйте и модифицируйте!
