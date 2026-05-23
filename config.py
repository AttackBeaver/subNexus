# пороги детекции
MIN_MONTHLY_OCCURRENCES = 3
MIN_YEARLY_OCCURRENCES = 2
WEEKLY_INTERVAL_DAYS = 7
MONTHLY_INTERVAL_MIN = 28
MONTHLY_INTERVAL_MAX = 31
YEARLY_INTERVAL_DAYS = 365
INTERVAL_TOLERANCE_DAYS = 2

# пороги для статусов
PRICE_RISE_THRESHOLD_PERCENT = 20

# дата
SIMULATED_CURRENT_DATE = None

# шанс появления "лишних" подписок
UNUSED_PROBABILITY = 0.5
UNUSED_MONTHLY_DAYS = 30
UNUSED_YEARLY_DAYS = 180
MIN_SUBSCRIPTION_AMOUNT = 50
MAX_CV_FOR_SUBSCRIPTION = 0.3

# для специальных подписок
TRIAL_PROBABILITY = 0.7
PRICE_RISE_PROBABILITY = 0.7

# справочник: сервис - категория
MERCHANT_CATEGORIES = {

    # МУЗЫКА
    "Яндекс.Музыка": "Музыка",
    "VK Музыка": "Музыка",
    "Spotify": "Музыка",
    "Zvuk": "Музыка",
    "YouTube Music": "Музыка",
    "Boom": "Музыка",
    "МТС Музыка": "Музыка",
    "Apple Music": "Музыка",
    "Deezer": "Музыка",

    # ВИДЕО / СТРИМИНГ
    "Кинопоиск": "Видео",
    "IVI": "Видео",
    "Okko": "Видео",
    "START": "Видео",
    "Wink": "Видео",
    "Premier": "Видео",
    "RUTUBE": "Видео",
    "RUTUBE x PREMIER": "Видео",
    "RUTUBE x PREMIER x START": "Видео",
    "Netflix": "Видео",
    "Amediateka": "Видео",
    "KION": "Видео",
    "YouTube Premium": "Видео",
    "VK Видео": "Видео",
    "Twitch": "Видео",
    "Prime Video": "Видео",
    "More.tv": "Видео",

    # ХРАНИЛИЩЕ
    "Яндекс 360": "Хранилище",
    "Google Drive": "Хранилище",
    "Apple iCloud": "Хранилище",
    "Dropbox": "Хранилище",
    "OneDrive": "Хранилище",
    "Mail Cloud": "Хранилище",
    "СберДиск": "Хранилище",
    "VK WorkDisk": "Хранилище",
    "Облако Mail.ru": "Хранилище",

    # ОБРАЗОВАНИЕ
    "Skillbox": "Образование",
    "GeekBrains": "Образование",
    "Skyeng": "Образование",
    "Нетология": "Образование",
    "Stepik": "Образование",
    "Яндекс Практикум": "Образование",
    "Uchi.ru": "Образование",
    "Дневник.ру PRO": "Образование",
    "Фоксфорд": "Образование",
    "Lingualeo": "Образование",
    "Puzzle English": "Образование",

    # ИГРЫ
    "Steam": "Игры",
    "Xbox Game Pass": "Игры",
    "PlayStation Plus": "Игры",
    "VK Play": "Игры",
    "Battle.net": "Игры",
    "Kupikod": "Игры",
    "EA Play": "Игры",
    "Nintendo Switch Online": "Игры",

    # ЭКОСИСТЕМЫ
    "Яндекс Плюс": "Экосистема",
    "Самокат+": "Экосистема",
    "Ozon Premium": "Экосистема",
    "Wildberries Plus": "Экосистема",
    "СберПрайм": "Экосистема",
    "МТС Premium": "Экосистема",
    "Пакет X5": "Экосистема",
    "Combo Mail.ru": "Экосистема",

    # SOFTWARE
    "ChatGPT Plus": "Software",
    "Claude Pro": "Software",
    "Notion": "Software",
    "Canva Pro": "Software",
    "Adobe Creative Cloud": "Software",
    "Microsoft 365": "Software",
    "Miro": "Software",
    "Figma": "Software",
    "Suno": "Software",
    "GitHub Copilot": "Software",
    "JetBrains All Products": "Software",
    "Cursor Pro": "Software",

    # VPN / БЕЗОПАСНОСТЬ
    "Kaspersky Plus": "Безопасность",
    "Dr.Web": "Безопасность",
    "NordVPN": "VPN",
    "Surfshark": "VPN",
    "ProtonVPN": "VPN",

    # КНИГИ
    "ЛитРес": "Книги",
    "MyBook": "Книги",
    "Bookmate": "Книги",
    "Wattpad": "Книги",
    "Storytel": "Книги",

    # ФИТНЕС / ЗДОРОВЬЕ
    "FitStars": "Фитнес",
    "World Class": "Фитнес",
    "Ясно": "Здоровье",
    "Flo Premium": "Здоровье",
    "Yazio": "Здоровье",

    # БАНКОВСКИЕ ПОДПИСКИ
    "ТБанк Pro": "Банковская подписка",
    "СберПрайм+": "Банковская подписка",
    "Альфа-Смарт": "Банковская подписка",
}

# популярные сервисы
POPULAR_SERVICES = [

    # МУЗЫКА
    {"name": "Яндекс.Музыка", "amount": 299, "period": "monthly"},
    {"name": "VK Музыка", "amount": 169, "period": "monthly"},
    {"name": "Spotify", "amount": 189, "period": "monthly"},
    {"name": "Zvuk", "amount": 199, "period": "monthly"},
    {"name": "YouTube Music", "amount": 299, "period": "monthly"},
    {"name": "Boom", "amount": 169, "period": "monthly"},
    {"name": "МТС Музыка", "amount": 169, "period": "monthly"},
    {"name": "МТС Музыка", "amount": 7, "period": "daily"},
    {"name": "Apple Music", "amount": 169, "period": "monthly"},
    {"name": "Deezer", "amount": 255, "period": "monthly"},

    # ВИДЕО
    {"name": "Кинопоиск", "amount": 399, "period": "monthly"},
    {"name": "IVI", "amount": 199, "period": "monthly"},
    {"name": "Okko", "amount": 399, "period": "monthly"},
    {"name": "START", "amount": 399, "period": "monthly"},
    {"name": "Wink", "amount": 299, "period": "monthly"},
    {"name": "Premier", "amount": 299, "period": "monthly"},
    {"name": "RUTUBE", "amount": 299, "period": "monthly"},
    {"name": "RUTUBE x PREMIER", "amount": 399, "period": "monthly"},
    {"name": "RUTUBE x PREMIER x START", "amount": 599, "period": "monthly"},
    {"name": "Netflix", "amount": 799, "period": "monthly"},
    {"name": "Amediateka", "amount": 599, "period": "monthly"},
    {"name": "KION", "amount": 249, "period": "monthly"},
    {"name": "YouTube Premium", "amount": 299, "period": "monthly"},
    {"name": "VK Видео", "amount": 299, "period": "monthly"},
    {"name": "Twitch", "amount": 410, "period": "monthly"},
    {"name": "Prime Video", "amount": 858, "period": "monthly"},
    {"name": "More.tv", "amount": 299, "period": "monthly"},

    # ОБЛАКО / ХРАНИЛИЩЕ
    {"name": "Яндекс 360", "amount": 249, "period": "monthly"},
    {"name": "Google Drive", "amount": 99, "period": "monthly"},
    {"name": "Apple iCloud", "amount": 149, "period": "monthly"},
    {"name": "Dropbox", "amount": 990, "period": "monthly"},
    {"name": "OneDrive", "amount": 499, "period": "monthly"},
    {"name": "Mail Cloud", "amount": 199, "period": "monthly"},
    {"name": "СберДиск", "amount": 99, "period": "monthly"},
    {"name": "СберДиск", "amount": 990, "period": "yearly"},
    {"name": "VK WorkDisk", "amount": 259, "period": "monthly"},
    {"name": "VK WorkDisk", "amount": 24860, "period": "yearly"},
    {"name": "Облако Mail.ru", "amount": 149, "period": "monthly"},

    # ОБРАЗОВАНИЕ
    {"name": "Skillbox", "amount": 1490, "period": "monthly"},
    {"name": "GeekBrains", "amount": 1290, "period": "monthly"},
    {"name": "Skyeng", "amount": 2990, "period": "monthly"},
    {"name": "Нетология", "amount": 1990, "period": "monthly"},
    {"name": "Stepik", "amount": 499, "period": "monthly"},
    {"name": "Яндекс Практикум", "amount": 3990, "period": "monthly"},
    {"name": "Uchi.ru", "amount": 490, "period": "monthly"},
    {"name": "Дневник.ру PRO", "amount": 149, "period": "monthly"},
    {"name": "Фоксфорд", "amount": 890, "period": "monthly"},
    {"name": "Lingualeo", "amount": 399, "period": "monthly"},
    {"name": "Puzzle English", "amount": 499, "period": "monthly"},

    # ИГРЫ
    {"name": "Steam", "amount": 699, "period": "monthly"},
    {"name": "Xbox Game Pass", "amount": 899, "period": "monthly"},
    {"name": "PlayStation Plus", "amount": 3299, "period": "yearly"},
    {"name": "PS Plus", "amount": 1848, "period": "monthly"},
    {"name": "PS Plus", "amount": 4149, "period": "quarterly"},
    {"name": "PS Plus", "amount": 12099, "period": "yearly"},
    {"name": "VK Play", "amount": 399, "period": "monthly"},
    {"name": "Battle.net", "amount": 599, "period": "monthly"},
    {"name": "Kupikod", "amount": 299, "period": "monthly"},
    {"name": "Kupikod", "amount": 2799, "period": "yearly"},
    {"name": "EA Play", "amount": 399, "period": "monthly"},
    {"name": "Nintendo Switch Online", "amount": 1699, "period": "yearly"},

    # ЭКОСИСТЕМЫ / ДОСТАВКА
    {"name": "Яндекс Плюс", "amount": 399, "period": "monthly"},
    {"name": "Самокат+", "amount": 199, "period": "monthly"},
    {"name": "Ozon Premium", "amount": 199, "period": "monthly"},
    {"name": "Wildberries Plus", "amount": 149, "period": "monthly"},
    {"name": "СберПрайм", "amount": 399, "period": "monthly"},
    {"name": "МТС Premium", "amount": 249, "period": "monthly"},
    {"name": "Пакет X5", "amount": 199, "period": "monthly"},
    {"name": "Combo Mail.ru", "amount": 199, "period": "monthly"},

    # SOFTWARE
    {"name": "ChatGPT Plus", "amount": 2000, "period": "monthly"},
    {"name": "Claude Pro", "amount": 1787, "period": "monthly"},
    {"name": "Notion", "amount": 990, "period": "monthly"},
    {"name": "Canva Pro", "amount": 1290, "period": "monthly"},
    {"name": "Adobe Creative Cloud", "amount": 2990, "period": "monthly"},
    {"name": "Microsoft 365", "amount": 599, "period": "monthly"},
    {"name": "Miro", "amount": 1200, "period": "monthly"},
    {"name": "Figma", "amount": 1390, "period": "monthly"},
    {"name": "Suno", "amount": 790, "period": "monthly"},
    {"name": "Suno", "amount": 9590, "period": "yearly"},
    {"name": "GitHub Copilot", "amount": 1000, "period": "monthly"},
    {"name": "JetBrains All Products", "amount": 2890, "period": "monthly"},
    {"name": "Cursor Pro", "amount": 2000, "period": "monthly"},

    # VPN / БЕЗОПАСНОСТЬ
    {"name": "Kaspersky Plus", "amount": 299, "period": "monthly"},
    {"name": "Dr.Web", "amount": 199, "period": "monthly"},
    {"name": "NordVPN", "amount": 1290, "period": "monthly"},
    {"name": "Surfshark", "amount": 1090, "period": "monthly"},
    {"name": "ProtonVPN", "amount": 990, "period": "monthly"},

    # КНИГИ
    {"name": "ЛитРес", "amount": 399, "period": "monthly"},
    {"name": "MyBook", "amount": 549, "period": "monthly"},
    {"name": "Bookmate", "amount": 499, "period": "monthly"},
    {"name": "Wattpad", "amount": 289, "period": "monthly"},
    {"name": "Wattpad", "amount": 2799, "period": "yearly"},
    {"name": "Storytel", "amount": 549, "period": "monthly"},

    # ЗДОРОВЬЕ / ФИТНЕС
    {"name": "FitStars", "amount": 799, "period": "monthly"},
    {"name": "World Class", "amount": 4990, "period": "monthly"},
    {"name": "Ясно", "amount": 1490, "period": "monthly"},
    {"name": "Flo Premium", "amount": 499, "period": "monthly"},
    {"name": "Yazio", "amount": 399, "period": "monthly"},

    # БАНКОВСКИЕ ПОДПИСКИ
    {"name": "ТБанк Pro", "amount": 299, "period": "monthly"},
    {"name": "СберПрайм+", "amount": 699, "period": "monthly"},
    {"name": "Альфа-Смарт", "amount": 399, "period": "monthly"},
]

# допы
NUM_MONTHS_HISTORY = 12
RANDOM_SEED = 42

# не являются подписками (даже если частые)
BLACKLIST_MERCHANTS = [
    "Перекрёсток", "Яндекс.Такси", "Starbucks", "Ozon", "Аптека",
    "Макдоналдс", "АЗС", "Пятёрочка", "Магнит", "ВкусВилл",
    "Delivery Club", "Яндекс.Еда", "СберМаркет", "KFC", "Burger King"
]
