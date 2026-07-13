import requests
import json
import os
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Токен из отдельного файла config.py
from config import TOKEN

# ======== ПРАВИЛЬНЫЙ ПУТЬ ДЛЯ ДАННЫХ ========
DATA_DIR = os.path.expanduser("~/dota_bot_data")
DATA_FILE = os.path.join(DATA_DIR, "user_data.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ======== ПОЛНЫЙ СПИСОК ГЕРОЕВ (резервный) ========
FALLBACK_HEROES = {
    1: "Anti-Mage", 2: "Axe", 3: "Bane", 4: "Bloodseeker", 5: "Crystal Maiden",
    6: "Drow Ranger", 7: "Earthshaker", 8: "Juggernaut", 9: "Mirana", 10: "Morphling",
    11: "Shadow Fiend", 12: "Phantom Lancer", 13: "Puck", 14: "Pudge", 15: "Razor",
    16: "Sand King", 17: "Storm Spirit", 18: "Sven", 19: "Tiny", 20: "Vengeful Spirit",
    21: "Windranger", 22: "Zeus", 23: "Kunkka", 25: "Lina", 26: "Lion",
    27: "Shadow Shaman", 28: "Slardar", 29: "Tidehunter", 30: "Witch Doctor",
    31: "Lich", 32: "Riki", 33: "Enigma", 34: "Tinker", 35: "Sniper",
    36: "Necrophos", 37: "Warlock", 38: "Beastmaster", 39: "Queen of Pain",
    40: "Venomancer", 41: "Faceless Void", 42: "Wraith King", 43: "Death Prophet",
    44: "Phantom Assassin", 45: "Pugna", 46: "Templar Assassin", 47: "Viper",
    48: "Luna", 49: "Dragon Knight", 50: "Dazzle", 51: "Clockwerk",
    52: "Leshrac", 53: "Nature's Prophet", 54: "Lifestealer", 55: "Dark Seer",
    56: "Clinkz", 57: "Omniknight", 58: "Enchantress", 59: "Huskar", 60: "Night Stalker",
    61: "Broodmother", 62: "Bounty Hunter", 63: "Weaver", 64: "Jakiro",
    65: "Batrider", 66: "Chen", 67: "Spectre", 68: "Ancient Apparition",
    69: "Doom", 70: "Ursa", 71: "Spirit Breaker", 72: "Gyrocopter",
    73: "Alchemist", 74: "Invoker", 75: "Silencer", 76: "Outworld Destroyer",
    77: "Lycan", 78: "Brewmaster", 79: "Shadow Demon", 80: "Lone Druid",
    81: "Chaos Knight", 82: "Meepo", 83: "Treant Protector", 84: "Ogre Magi",
    85: "Undying", 86: "Rubick", 87: "Disruptor", 88: "Nyx Assassin",
    89: "Naga Siren", 90: "Keeper of the Light", 91: "Io", 92: "Visage",
    93: "Slark", 94: "Medusa", 95: "Troll Warlord", 96: "Centaur Warrunner",
    97: "Magnus", 98: "Timbersaw", 99: "Bristleback", 100: "Tusk",
    101: "Skywrath Mage", 102: "Abaddon", 103: "Elder Titan", 104: "Legion Commander",
    105: "Techies", 106: "Ember Spirit", 107: "Earth Spirit", 108: "Underlord",
    109: "Terrorblade", 110: "Phoenix", 111: "Oracle", 112: "Winter Wyvern",
    113: "Arc Warden", 114: "Monkey King", 119: "Dark Willow", 120: "Pangolier",
    121: "Grimstroke", 123: "Hoodwink", 126: "Void Spirit", 128: "Snapfire",
    129: "Mars", 135: "Dawnbreaker", 136: "Marci", 137: "Primal Beast",
    138: "Muerta"
}

def load_heroes():
    try:
        response = requests.get("https://api.opendota.com/api/heroes", timeout=5)
        if response.status_code == 200:
            heroes_data = response.json()
            heroes = {hero['id']: hero['localized_name'] for hero in heroes_data}
            print(f"✅ Загружено {len(heroes)} героев из API")
            return heroes
    except Exception as e:
        print(f"⚠️ Не удалось загрузить героев из API: {e}")
    
    print(f"📋 Используется резервный список ({len(FALLBACK_HEROES)} героев)")
    return FALLBACK_HEROES

HEROES = load_heroes()

def get_hero_name(hero_id):
    return HEROES.get(hero_id, f"Герой {hero_id}")

# ======== РАБОТА С ДАННЫМИ ========

def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Данные сохранены в {DATA_FILE}")
    except Exception as e:
        print(f"❌ Ошибка сохранения данных: {e}")

user_data = load_user_data()
print(f"📁 Загружено {len(user_data)} записей из {DATA_FILE}")

# ======== КЛАВИАТУРЫ ========

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data='stats_menu')],
        [InlineKeyboardButton("🏆 Герои", callback_data='heroes_menu')],
        [InlineKeyboardButton("👤 Мой профиль", callback_data='profile_menu')],
        [InlineKeyboardButton("⚙️ Помощь", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def stats_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 Подробнее", callback_data='more'),
            InlineKeyboardButton("🔄 Обновить", callback_data='refresh')
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def profile_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить профиль", callback_data='refresh_profile')],
        [InlineKeyboardButton("🗑️ Отвязать аккаунт", callback_data='unregister_confirm')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def heroes_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить список", callback_data='refresh_heroes')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ======== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ========

def get_rank_tier(rank_tier):
    """Преобразует rank_tier в читаемый ранг"""
    if not rank_tier or rank_tier == 0:
        return "❌ Нет рейтинга"
    
    tier = rank_tier // 10
    star = rank_tier % 10
    
    rank_names = {
        1: "Рекрут", 2: "Страж", 3: "Рыцарь",
        4: "Герой", 5: "Легенда", 6: "Властелин",
        7: "Божество", 8: "Титан"
    }
    
    star_icons = {
        1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"
    }
    
    if tier == 0:
        return "❌ Нет рейтинга"
    
    if tier >= 8:
        return "🏆 Титан"
    
    rank_name = rank_names.get(tier, f"Уровень {tier}")
    stars = star_icons.get(star, "") if star > 0 and star <= 5 else ""
    
    return f"{rank_name} {stars}".strip()

def is_match_win(match):
    """Определяет, победил ли игрок в матче"""
    player_slot = match.get('player_slot', 0)
    radiant_win = match.get('radiant_win', False)
    is_radiant = player_slot < 5
    return (is_radiant and radiant_win) or (not is_radiant and not radiant_win)

def get_best_heroes(account_id, limit=10, min_games=30):
    """
    Получает лучших героев игрока.
    Учитывает комбинацию винрейта и количества игр.
    """
    try:
        url = f"https://api.opendota.com/api/players/{account_id}/heroes"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        heroes_data = response.json()
        
        filtered = [h for h in heroes_data if h.get('games', 0) >= min_games]
        
        if not filtered:
            return []
        
        for hero in filtered:
            hero_id = hero.get('hero_id', 0)
            games = hero.get('games', 0)
            wins = hero.get('win', 0)
            winrate = (wins / games * 100) if games > 0 else 0
            
            try:
                hero_stats_url = f"https://api.opendota.com/api/players/{account_id}/heroes/{hero_id}"
                hero_stats_response = requests.get(hero_stats_url, timeout=10)
                if hero_stats_response.status_code == 200:
                    hero_stats = hero_stats_response.json()
                    kills = hero_stats.get('kills', 0)
                    deaths = hero_stats.get('deaths', 0)
                    assists = hero_stats.get('assists', 0)
                    if deaths > 0:
                        kda = (kills + assists) / deaths
                    else:
                        kda = kills + assists
                    hero['kda'] = kda
                else:
                    hero['kda'] = 0
            except Exception as e:
                print(f"⚠️ Ошибка получения KDA для героя {hero_id}: {e}")
                hero['kda'] = 0
            
            max_games = max([h.get('games', 0) for h in filtered])
            games_weight = (games / max_games) * 100 if max_games > 0 else 0
            
            hero['score'] = (winrate * 0.6) + (games_weight * 0.4)
            hero['winrate'] = winrate
        
        sorted_heroes = sorted(filtered, key=lambda x: x['score'], reverse=True)
        
        return sorted_heroes[:limit]
    except Exception as e:
        print(f"❌ Ошибка получения героев: {e}")
        return []

def get_profile_stats(account_id):
    """Получает полную статистику игрока для профиля"""
    try:
        url = f"https://api.opendota.com/api/players/{account_id}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        
        player_data = response.json()
        
        wl_url = f"https://api.opendota.com/api/players/{account_id}/wl"
        wl_response = requests.get(wl_url, timeout=10)
        wl_data = wl_response.json() if wl_response.status_code == 200 else {'win': 0, 'lose': 0}
        
        matches_url = f"https://api.opendota.com/api/players/{account_id}/recentMatches"
        matches_response = requests.get(matches_url, timeout=10)
        matches = matches_response.json() if matches_response.status_code == 200 else []
        
        return {
            'player_data': player_data,
            'wl': wl_data,
            'matches': matches[:10]
        }
    except Exception as e:
        print(f"❌ Ошибка получения статистики профиля: {e}")
        return None

def format_profile_message(user_id, account_id):
    """Форматирует сообщение профиля с полной информацией"""
    if not account_id:
        return "❌ Ты не зарегистрирован.\n\nИспользуй /register {ID} чтобы привязать аккаунт."
    
    stats = get_profile_stats(account_id)
    if not stats:
        return f"❌ Не удалось получить статистику для ID: `{account_id}`\n\nПроверь правильность ID."
    
    player_data = stats['player_data']
    wl = stats['wl']
    matches = stats['matches']
    best_heroes = get_best_heroes(account_id, limit=5)
    
    profile_text = "═══════════════════════\n"
    profile_text += "     👤 **МОЙ ПРОФИЛЬ**\n"
    profile_text += "═══════════════════════\n\n"
    
    if 'profile' in player_data and 'personaname' in player_data['profile']:
        profile_text += f"📛 **Ник:** {player_data['profile']['personaname']}\n"
    
    profile_text += f"🆔 **Steam ID:** `{account_id}`\n"
    
    rank_tier = player_data.get('rank_tier', 0)
    rank_name = get_rank_tier(rank_tier)
    profile_text += f"🏅 **Звание:** {rank_name}\n"
    
    if 'mmr_estimate' in player_data and player_data['mmr_estimate']:
        mmr = player_data['mmr_estimate'].get('estimate', 0)
        if mmr > 0:
            profile_text += f"⭐ **MMR:** {mmr}\n"
    
    profile_text += "\n" + "─" * 30 + "\n\n"
    
    total_matches = wl.get('win', 0) + wl.get('lose', 0)
    profile_text += "📊 **ОБЩАЯ СТАТИСТИКА**\n"
    profile_text += "─" * 20 + "\n"
    profile_text += f"🎮 **Всего игр:** {total_matches}\n"
    
    if total_matches > 0:
        wins = wl.get('win', 0)
        loses = wl.get('lose', 0)
        winrate = (wins / total_matches) * 100
        
        profile_text += f"✅ Побед: {wins}\n"
        profile_text += f"❌ Поражений: {loses}\n"
        profile_text += f"🏆 **Винрейт:** {winrate:.1f}%\n\n"
    else:
        profile_text += "📭 Нет данных о матчах\n\n"
    
    profile_text += "─" * 30 + "\n\n"
    
    if matches:
        last_match = matches[0]
        last_match_time = last_match.get('start_time', 0)
        last_match_duration = last_match.get('duration', 0) // 60
        
        if last_match_time > 0:
            match_datetime = datetime.fromtimestamp(last_match_time)
            last_match_date = match_datetime.strftime("%d.%m.%Y %H:%M")
        else:
            last_match_date = "Неизвестно"
        
        profile_text += "⏰ **ПОСЛЕДНЯЯ ИГРА**\n"
        profile_text += "─" * 20 + "\n"
        profile_text += f"📅 **Дата:** {last_match_date}\n"
        profile_text += f"⏱️ **Длительность:** {last_match_duration} мин\n"
        
        hero_id = last_match.get('hero_id', 0)
        hero_name = get_hero_name(hero_id)
        kills = last_match.get('kills', 0)
        deaths = last_match.get('deaths', 0)
        assists = last_match.get('assists', 0)
        
        is_win = is_match_win(last_match)
        result_text = "🏆 **ПОБЕДА** ✅" if is_win else "💔 **ПОРАЖЕНИЕ** ❌"
        
        profile_text += f"🎯 **Герой:** {hero_name}\n"
        profile_text += f"📊 **Результат:** {result_text}\n"
        profile_text += f"⚔️ **KDA:** {kills}/{deaths}/{assists}\n\n"
    else:
        profile_text += "⏰ **Последняя игра:** Нет данных\n\n"
    
    profile_text += "─" * 30 + "\n\n"
    
    if best_heroes:
        profile_text += "🏆 **ЛУЧШИЕ ГЕРОИ**\n"
        profile_text += "─" * 20 + "\n"
        for i, hero in enumerate(best_heroes, 1):
            hero_id = hero.get('hero_id', 0)
            hero_name = get_hero_name(hero_id)
            games = hero.get('games', 0)
            wins = hero.get('win', 0)
            winrate = hero.get('winrate', 0)
            
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            medal = medals[i-1] if i <= 5 else f"{i}."
            
            bar_length = 10
            filled = int(winrate / 100 * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            profile_text += f"{medal} **{hero_name}**\n"
            profile_text += f"   📊 {games} игр  |  {winrate:.1f}% побед\n"
            profile_text += f"   {bar}\n"
    else:
        profile_text += "🏆 **Лучшие герои:** Недостаточно данных (нужно минимум 30 игр на герое)\n"
    
    profile_text += "\n" + "═" * 30 + "\n"
    profile_text += "🔄 Используй кнопки ниже для управления профилем."
    
    return profile_text

def format_heroes_message(account_id):
    """Форматирует сообщение с топ-героями игрока"""
    heroes = get_best_heroes(account_id, limit=10, min_games=30)
    
    if not heroes:
        return "❌ Не удалось получить данные по героям.\n\nВозможно, у игрока меньше 30 матчей на героях или нет данных."
    
    message = "╔═════════════════════════════════════════════╗\n"
    message += "║          🏆 ТОП ГЕРОИ                   ║\n"
    message += "╚═════════════════════════════════════════════╝\n"
    message += f"\n  🆔 ID: `{account_id}`\n"
    message += f"  📌 Минимум игр: `30`\n\n"
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, hero in enumerate(heroes, 1):
        hero_id = hero.get('hero_id', 0)
        hero_name = get_hero_name(hero_id)
        games = hero.get('games', 0)
        wins = hero.get('win', 0)
        winrate = hero.get('winrate', 0)
        kda = hero.get('kda', 0)
        
        medal = medals[i-1] if i <= 10 else f"{i}."
        
        bar_length = 15
        filled = int(winrate / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        message += f"  ┌─────────────────────────────────────┐\n"
        message += f"  │ {medal} **{hero_name}**\n"
        message += f"  │   📊 Игр: {games}  |  🏆 Винрейт: {winrate:.1f}%\n"
        message += f"  │   {bar}\n"
        message += f"  │   ⚔️ KDA: {kda:.2f}\n"
        message += f"  └─────────────────────────────────────┘\n\n"
    
    message += "  ═════════════════════════════════════════════╝\n"
    message += "\n📌 *Показаны герои с минимальным количеством игр: 30*"
    
    return message

# ======== ОСНОВНЫЕ КОМАНДЫ ========

def start(update, context):
    user_id = str(update.message.from_user.id)
    
    if user_id in user_data:
        welcome = f"👋 С возвращением! Твой ID: `{user_data[user_id]}`\n\n"
    else:
        welcome = "👋 Привет! Ты еще не зарегистрирован.\n"
        welcome += "Используй /register {ID} чтобы привязать аккаунт.\n\n"
    
    update.message.reply_text(
        welcome + "═══════════════════════\n"
        "     🏠 **ГЛАВНОЕ МЕНЮ**\n"
        "═══════════════════════\n\n"
        "📊 **Статистика** - Получить статистику игрока\n"
        "🏆 **Герои** - Топ героев игрока\n"
        "👤 **Мой профиль** - Управление аккаунтом\n"
        "⚙️ **Помощь** - Инструкция по использованию",
        reply_markup=main_menu_keyboard(),
        parse_mode='Markdown'
    )

def register(update, context):
    try:
        account_id = context.args[0]
    except IndexError:
        update.message.reply_text(
            "Пожалуйста, укажи ID игрока.\n"
            "Пример: /register 123456789\n\n"
            "Где найти ID:\n"
            "1️⃣ Зайди в свой профиль в Dota 2\n"
            "2️⃣ Скопируй ссылку на профиль\n"
            "3️⃣ В ссылке есть цифровой ID"
        )
        return
    
    url = f"https://api.opendota.com/api/players/{account_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        update.message.reply_text(
            "❌ Не удалось найти игрока с таким ID.\n"
            "Проверь правильность ввода."
        )
        return
    
    user_id = str(update.message.from_user.id)
    user_data[user_id] = account_id
    save_user_data(user_data)
    
    update.message.reply_text(
        f"✅ Регистрация успешна!\n\n"
        f"🆔 Твой ID: `{account_id}`\n\n"
        f"Теперь ты можешь использовать:\n"
        f"/stats - без указания ID\n"
        f"/profile - показать подробный профиль\n"
        f"/heroes - показать топ героев",
        parse_mode='Markdown'
    )

def stats(update, context):
    user_id = str(update.message.from_user.id)
    account_id = None
    
    if context.args:
        account_id = context.args[0]
    elif user_id in user_data:
        account_id = user_data[user_id]
    else:
        update.message.reply_text(
            "❌ Ты не зарегистрирован!\n\n"
            "Используй /register {ID} чтобы привязать аккаунт.\n"
            "Или укажи ID в команде: /stats 123456789"
        )
        return

    recent_matches_url = f"https://api.opendota.com/api/players/{account_id}/recentMatches"
    response = requests.get(recent_matches_url)

    if response.status_code != 200:
        update.message.reply_text(
            "❌ Не удалось найти игрока с таким ID.\n"
            "Проверь правильность ввода."
        )
        return

    matches = response.json()

    if not matches:
        update.message.reply_text("📭 Похоже, этот игрок еще не играл в Dota 2.")
        return

    temp_key = 'temp_' + user_id
    user_data[temp_key] = {
        'matches': matches[:10],
        'account_id': account_id
    }

    recent_matches = matches[:10]
    
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_matches = len(recent_matches)
    
    match_details = []
    for i, match in enumerate(recent_matches, 1):
        kills = match.get('kills', 0)
        deaths = match.get('deaths', 0)
        assists = match.get('assists', 0)
        hero_id = match.get('hero_id', 0)
        hero_name = get_hero_name(hero_id)
        is_win = is_match_win(match)
        
        total_kills += kills
        total_deaths += deaths
        total_assists += assists
        
        result_emoji = "✅" if is_win else "❌"
        result_text = "Победа" if is_win else "Поражение"
        
        match_details.append(
            f"{result_emoji} Матч {i}: {hero_name} | K: {kills} / D: {deaths} / A: {assists} | {result_text}"
        )
    
    avg_kills = total_kills / total_matches
    avg_deaths = total_deaths / total_matches
    avg_assists = total_assists / total_matches
    
    if total_deaths == 0:
        kda = total_kills + total_assists
    else:
        kda = (total_kills + total_assists) / total_deaths

    full_message = (
        "╔═════════════════════════════════════════════╗\n"
        "║              📊 СТАТИСТИКА                 ║\n"
        "╚═════════════════════════════════════════════╝\n"
        "\n"
        f"  🆔 **ID:** `{account_id}`\n"
        "\n"
        "  ┌─────────────────────────────────────┐\n"
        f"  │  📈 KDA:     {avg_kills:.1f} / {avg_deaths:.1f} / {avg_assists:.1f}\n"
        f"  │  🏆 Общий KDA:  {kda:.2f}\n"
        f"  │  🎮 Матчей:    {total_matches}\n"
        "  └─────────────────────────────────────┘\n"
        "\n"
        "  ╔═════════════════════════════════════════════╗\n"
        "  ║           📋 ПОСЛЕДНИЕ МАТЧИ              ║\n"
        "  ╚═════════════════════════════════════════════╝\n"
    )
    
    for detail in match_details:
        full_message += f"  {detail}\n"
    
    full_message += "  ═════════════════════════════════════════════╝\n"
    
    user_data[temp_key]['short_stats'] = full_message
    save_user_data(user_data)

    update.message.reply_text(
        full_message,
        reply_markup=stats_keyboard(),
        parse_mode='Markdown'
    )

def heroes(update, context):
    """Команда /heroes - показывает топ героев игрока"""
    user_id = str(update.message.from_user.id)
    
    if user_id not in user_data:
        update.message.reply_text(
            "❌ Ты не зарегистрирован!\n\n"
            "Используй /register {ID} чтобы привязать аккаунт."
        )
        return
    
    account_id = user_data[user_id]
    
    message = update.message.reply_text("🔄 Загружаю список героев...")
    
    heroes_message = format_heroes_message(account_id)
    
    message.edit_text(
        heroes_message,
        reply_markup=heroes_keyboard(),
        parse_mode='Markdown'
    )

def profile(update, context):
    """Команда /profile - показывает подробный профиль"""
    user_id = str(update.message.from_user.id)
    
    if user_id not in user_data:
        update.message.reply_text(
            "❌ Ты не зарегистрирован!\n\n"
            "Используй /register {ID} чтобы привязать аккаунт."
        )
        return
    
    account_id = user_data[user_id]
    
    message = update.message.reply_text("🔄 Загружаю данные профиля...")
    
    profile_text = format_profile_message(user_id, account_id)
    
    message.edit_text(
        profile_text,
        reply_markup=profile_keyboard(),
        parse_mode='Markdown'
    )

def myid(update, context):
    user_id = str(update.message.from_user.id)
    
    if user_id in user_data:
        update.message.reply_text(
            f"👤 Твой сохраненный ID: `{user_data[user_id]}`\n\n"
            f"Используй /profile чтобы увидеть подробную информацию.",
            parse_mode='Markdown'
        )
    else:
        update.message.reply_text(
            "❌ Ты не зарегистрирован.\n\n"
            "Используй /register {ID} чтобы привязать аккаунт."
        )

def unregister(update, context):
    user_id = str(update.message.from_user.id)
    
    if user_id in user_data:
        del user_data[user_id]
        temp_key = 'temp_' + user_id
        if temp_key in user_data:
            del user_data[temp_key]
        save_user_data(user_data)
        update.message.reply_text(
            "✅ Твой аккаунт отвязан!\n\n"
            "Используй /register {ID} чтобы привязать новый."
        )
    else:
        update.message.reply_text(
            "❌ Ты не зарегистрирован.\n"
            "Используй /register {ID} чтобы привязать аккаунт."
        )

# ======== ОБРАБОТЧИК КНОПОК ========

def button_callback(update, context):
    query = update.callback_query
    query.answer()
    
    user_id = str(query.from_user.id)
    temp_key = 'temp_' + user_id
    temp_data = user_data.get(temp_key, {})
    matches = temp_data.get('matches', [])
    short_stats_text = temp_data.get('short_stats', '')
    account_id = temp_data.get('account_id', '')
    
    # Главное меню
    if query.data == 'main_menu':
        welcome = "🏠 **Главное меню**\n\n"
        if user_id in user_data:
            welcome += f"👤 Твой ID: `{user_data[user_id]}`\n\n"
        else:
            welcome += "⚠️ Ты не зарегистрирован. Используй /register\n\n"
        
        query.edit_message_text(
            welcome + "Выбери нужный раздел:",
            reply_markup=main_menu_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # ======== СТАТИСТИКА ========
    if query.data == 'stats_menu':
        if user_id in user_data:
            account_id = user_data[user_id]
            
            query.edit_message_text("🔄 Загружаю статистику...")
            
            recent_matches_url = f"https://api.opendota.com/api/players/{account_id}/recentMatches"
            response = requests.get(recent_matches_url)

            if response.status_code != 200:
                query.edit_message_text(
                    "❌ Не удалось получить статистику. Проверь ID.",
                    reply_markup=back_to_main_keyboard()
                )
                return

            matches = response.json()

            if not matches:
                query.edit_message_text(
                    "📭 Похоже, этот игрок еще не играл в Dota 2.",
                    reply_markup=back_to_main_keyboard()
                )
                return

            user_data[temp_key] = {
                'matches': matches[:10],
                'account_id': account_id
            }

            recent_matches = matches[:10]
            
            total_kills = 0
            total_deaths = 0
            total_assists = 0
            total_matches = len(recent_matches)
            
            match_details = []
            for i, match in enumerate(recent_matches, 1):
                kills = match.get('kills', 0)
                deaths = match.get('deaths', 0)
                assists = match.get('assists', 0)
                hero_id = match.get('hero_id', 0)
                hero_name = get_hero_name(hero_id)
                is_win = is_match_win(match)
                
                total_kills += kills
                total_deaths += deaths
                total_assists += assists
                
                result_emoji = "✅" if is_win else "❌"
                result_text = "Победа" if is_win else "Поражение"
                
                match_details.append(
                    f"{result_emoji} Матч {i}: {hero_name} | K: {kills} / D: {deaths} / A: {assists} | {result_text}"
                )
            
            avg_kills = total_kills / total_matches
            avg_deaths = total_deaths / total_matches
            avg_assists = total_assists / total_matches
            
            if total_deaths == 0:
                kda = total_kills + total_assists
            else:
                kda = (total_kills + total_assists) / total_deaths

            full_message = (
                "╔═════════════════════════════════════════════╗\n"
                "║              📊 СТАТИСТИКА                 ║\n"
                "╚═════════════════════════════════════════════╝\n"
                "\n"
                f"  🆔 **ID:** `{account_id}`\n"
                "\n"
                "  ┌─────────────────────────────────────┐\n"
                f"  │  📈 KDA:     {avg_kills:.1f} / {avg_deaths:.1f} / {avg_assists:.1f}\n"
                f"  │  🏆 Общий KDA:  {kda:.2f}\n"
                f"  │  🎮 Матчей:    {total_matches}\n"
                "  └─────────────────────────────────────┘\n"
                "\n"
                "  ╔═════════════════════════════════════════════╗\n"
                "  ║           📋 ПОСЛЕДНИЕ МАТЧИ              ║\n"
                "  ╚═════════════════════════════════════════════╝\n"
            )
            
            for detail in match_details:
                full_message += f"  {detail}\n"
            
            full_message += "  ═════════════════════════════════════════════╝\n"
            
            user_data[temp_key]['short_stats'] = full_message
            save_user_data(user_data)

            query.edit_message_text(
                full_message,
                reply_markup=stats_keyboard(),
                parse_mode='Markdown'
            )
        else:
            keyboard = [
                [InlineKeyboardButton("✅ Зарегистрироваться", callback_data='register_suggest')],
                [InlineKeyboardButton("📝 Ввести ID вручную", callback_data='manual_id')],
                [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            query.edit_message_text(
                "⚠️ **Ты не зарегистрирован!**\n\n"
                "Чтобы увидеть свою статистику:\n"
                "1️⃣ Зарегистрируй свой аккаунт (рекомендуется)\n"
                "2️⃣ Или используй команду /stats {ID}\n\n"
                "Выбери действие:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        return
    
    # ======== ГЕРОИ ========
    if query.data == 'heroes_menu':
        if user_id not in user_data:
            query.edit_message_text(
                "❌ Ты не зарегистрирован!\n\n"
                "Используй /register {ID} чтобы привязать аккаунт.",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        query.edit_message_text("🔄 Загружаю список героев...")
        
        account_id = user_data[user_id]
        heroes_message = format_heroes_message(account_id)
        
        query.edit_message_text(
            heroes_message,
            reply_markup=heroes_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # Обновить героев
    if query.data == 'refresh_heroes':
        if user_id not in user_data:
            query.edit_message_text(
                "❌ Ты не зарегистрирован!",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        query.edit_message_text("🔄 Обновляю список героев...")
        
        account_id = user_data[user_id]
        heroes_message = format_heroes_message(account_id)
        
        query.edit_message_text(
            heroes_message,
            reply_markup=heroes_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # ======== ПРЕДЛОЖЕНИЕ РЕГИСТРАЦИИ ========
    if query.data == 'register_suggest':
        query.edit_message_text(
            "📝 **Регистрация аккаунта**\n\n"
            "Чтобы зарегистрироваться, отправь команду:\n"
            "`/register {ID_игрока}`\n\n"
            "Где `{ID_игрока}` - твой числовой ID в Dota 2.\n\n"
            "Например:\n"
            "`/register 1065224574`\n\n"
            "Где найти ID:\n"
            "1️⃣ Зайди в свой профиль в Dota 2\n"
            "2️⃣ Скопируй ссылку на профиль\n"
            "3️⃣ В ссылке есть цифровой ID\n\n"
            "После регистрации нажми кнопку статистики снова!",
            reply_markup=back_to_main_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # ======== ПРЕДЛОЖЕНИЕ ВВЕСТИ ID ВРУЧНУЮ ========
    if query.data == 'manual_id':
        query.edit_message_text(
            "📝 **Введите ID вручную**\n\n"
            "Используй команду:\n"
            "`/stats {ID_игрока}`\n\n"
            "Где `{ID_игрока}` - числовой ID игрока в Dota 2.\n\n"
            "Например:\n"
            "`/stats 1065224574`\n\n"
            "Также ты можешь зарегистрироваться, чтобы больше не вводить ID каждый раз.",
            reply_markup=back_to_main_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # Профиль
    if query.data == 'profile_menu':
        if user_id not in user_data:
            query.edit_message_text(
                "❌ Ты не зарегистрирован!\n\n"
                "Используй /register {ID} чтобы привязать аккаунт.",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        query.edit_message_text("🔄 Загружаю профиль...")
        
        account_id = user_data[user_id]
        profile_text = format_profile_message(user_id, account_id)
        
        query.edit_message_text(
            profile_text,
            reply_markup=profile_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # Обновить профиль
    if query.data == 'refresh_profile':
        if user_id not in user_data:
            query.edit_message_text(
                "❌ Ты не зарегистрирован!",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        query.edit_message_text("🔄 Обновляю профиль...")
        
        account_id = user_data[user_id]
        profile_text = format_profile_message(user_id, account_id)
        
        query.edit_message_text(
            profile_text,
            reply_markup=profile_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # Подтверждение отвязки
    if query.data == 'unregister_confirm':
        keyboard = [
            [
                InlineKeyboardButton("✅ Да, отвязать", callback_data='unregister_yes'),
                InlineKeyboardButton("❌ Нет, отмена", callback_data='unregister_no')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            "⚠️ **Подтверждение**\n\n"
            "Ты уверен, что хочешь отвязать аккаунт?\n"
            "Все сохраненные данные будут удалены.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Отвязать аккаунт (подтверждено)
    if query.data == 'unregister_yes':
        if user_id in user_data:
            del user_data[user_id]
            temp_key = 'temp_' + user_id
            if temp_key in user_data:
                del user_data[temp_key]
            save_user_data(user_data)
            
            query.edit_message_text(
                "✅ Аккаунт успешно отвязан!\n\n"
                "Используй /register {ID} чтобы привязать новый.",
                reply_markup=back_to_main_keyboard()
            )
        else:
            query.edit_message_text(
                "❌ Ты не зарегистрирован.",
                reply_markup=back_to_main_keyboard()
            )
        return
    
    # Отвязать аккаунт (отмена)
    if query.data == 'unregister_no':
        if user_id not in user_data:
            query.edit_message_text(
                "❌ Ты не зарегистрирован.",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        account_id = user_data[user_id]
        profile_text = format_profile_message(user_id, account_id)
        
        query.edit_message_text(
            profile_text,
            reply_markup=profile_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # Помощь
    if query.data == 'help_menu':
        query.edit_message_text(
            "⚙️ **Помощь**\n\n"
            "**Команды бота:**\n"
            "/start - Главное меню\n"
            "/register {ID} - Привязать аккаунт\n"
            "/stats {ID} - Статистика игрока\n"
            "/heroes - Топ героев\n"
            "/profile - Подробный профиль\n"
            "/myid - Показать ID\n"
            "/unregister - Отвязать аккаунт\n\n"
            "**Пример использования:**\n"
            "/register 1065224574\n"
            "/stats\n"
            "/heroes\n"
            "/profile\n\n"
            "**Где найти ID:**\n"
            "1️⃣ Зайди в свой профиль в Dota 2\n"
            "2️⃣ Скопируй ссылку на профиль\n"
            "3️⃣ В ссылке есть цифровой ID",
            reply_markup=back_to_main_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    # ======== ПОДРОБНАЯ СТАТИСТИКА ========
    if query.data == 'more':
        if not matches:
            query.edit_message_text(
                "❌ Нет данных. Сначала используй /stats.",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        detailed_text = "╔══════════════════════════════════╗\n"
        detailed_text += "║     📊 **ПОДРОБНАЯ СТАТИСТИКА**  ║\n"
        detailed_text += "╚══════════════════════════════════╝\n\n"
        
        for i, match in enumerate(matches, 1):
            hero_id = match.get('hero_id', 0)
            hero_name = get_hero_name(hero_id)
            kills = match.get('kills', 0)
            deaths = match.get('deaths', 0)
            assists = match.get('assists', 0)
            gpm = match.get('gold_per_min', 0)
            xpm = match.get('xp_per_min', 0)
            duration = match.get('duration', 0) // 60
            is_win = is_match_win(match)
            
            result_text = "🏆 ПОБЕДА" if is_win else "💔 ПОРАЖЕНИЕ"
            result_emoji = "✅" if is_win else "❌"
            
            detailed_text += f"┌────────────────────────────────┐\n"
            detailed_text += f"│        **Матч {i}**            │\n"
            detailed_text += f"├────────────────────────────────┤\n"
            detailed_text += f"│ ⏱️ Длительность: {duration} мин\n"
            detailed_text += f"│ {result_emoji} Результат: {result_text}\n"
            detailed_text += f"│ 🎯 Герой: {hero_name}\n"
            detailed_text += f"│ 📊 KDA: {kills} / {deaths} / {assists}\n"
            detailed_text += f"│ 💰 GPM: {gpm}  |  XP: {xpm}\n"
            detailed_text += f"└────────────────────────────────┘\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔙 Назад к статистике", callback_data='back_to_stats')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            detailed_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    if query.data == 'back_to_stats':
        if not short_stats_text:
            query.edit_message_text(
                "❌ Нет сохраненной статистики. Используй /stats.",
                reply_markup=back_to_main_keyboard()
            )
            return
        
        query.edit_message_text(
            short_stats_text,
            reply_markup=stats_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    if query.data == 'refresh':
        query.edit_message_text(
            "🔄 Обновляю данные...\nИспользуй /stats для нового запроса.",
            reply_markup=back_to_main_keyboard()
        )
        return

# ======== ЗАПУСК ========

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("heroes", heroes))
    dp.add_handler(CommandHandler("profile", profile))
    dp.add_handler(CommandHandler("myid", myid))
    dp.add_handler(CommandHandler("unregister", unregister))
    dp.add_handler(CallbackQueryHandler(button_callback))
    
    updater.start_polling()
    print("✅ Бот запущен!")
    print(f"📁 Данные сохраняются в {DATA_FILE}")
    print(f"📋 Загружено героев: {len(HEROES)}")
    updater.idle()

if __name__ == "__main__":
    main()