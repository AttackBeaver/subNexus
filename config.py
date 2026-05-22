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
    # музыка
    "Яндекс.Музыка": "Музыка",
    "VK Музыка": "Музыка",
    "Spotify": "Музыка",
    "Zvuk": "Музыка",
    "YouTube Music": "Музыка",
    "Boom": "Музыка",

    # видео
    "Кинопоиск": "Видео",
    "IVI": "Видео",
    "Okko": "Видео",
    "START": "Видео",
    "Wink": "Видео",
    "Premier": "Видео",
    "Netflix": "Видео",
    "Amediateka": "Видео",
    "KION": "Видео",
    "YouTube Premium": "Видео",

    # облако / хранилище
    "Яндекс 360": "Хранилище",
    "Google Drive": "Хранилище",
    "Apple iCloud": "Хранилище",
    "Dropbox": "Хранилище",
    "OneDrive": "Хранилище",
    "Mail Cloud": "Хранилище",

    # образование
    "Skillbox": "Образование",
    "GeekBrains": "Образование",
    "Skyeng": "Образование",
    "Нетология": "Образование",
    "Stepik": "Образование",
    "Яндекс Практикум": "Образование",
    "Uchi.ru": "Образование",

    # игры
    "Steam": "Игры",
    "Xbox Game Pass": "Игры",
    "PlayStation Plus": "Игры",
    "VK Play": "Игры",
    "Battle.net": "Игры",

    # доставка
    "Яндекс Плюс": "Доставка",
    "Самокат+": "Доставка",
    "Ozon Premium": "Доставка",
    "Wildberries Plus": "Доставка",
    "СберПрайм": "Доставка",

    # soft
    "ChatGPT Plus": "Software",
    "Notion": "Software",
    "Canva Pro": "Software",
    "Adobe Creative Cloud": "Software",
    "Microsoft 365": "Software",
    "Miro": "Software",

    # VPN / безопаность
    "Kaspersky Plus": "Безопасность",
    "Dr.Web": "Безопасность",
    "NordVPN": "VPN",
    "Surfshark": "VPN",

    # книги
    "ЛитРес": "Книги",
    "MyBook": "Книги",
    "Bookmate": "Книги",

    # спорт / здоровье
    "FitStars": "Фитнес",
    "World Class": "Фитнес",
    "Ясно": "Здоровье",
}

# популярные сервисы
POPULAR_SERVICES = [
    # музыка
    {"name": "Яндекс.Музыка", "amount": 299, "period": "monthly"},
    {"name": "VK Музыка", "amount": 169, "period": "monthly"},
    {"name": "Spotify", "amount": 189, "period": "monthly"},
    {"name": "Zvuk", "amount": 199, "period": "monthly"},
    {"name": "YouTube Music", "amount": 299, "period": "monthly"},
    {"name": "Boom", "amount": 169, "period": "monthly"},

    # видео
    {"name": "Кинопоиск", "amount": 399, "period": "monthly"},
    {"name": "IVI", "amount": 199, "period": "monthly"},
    {"name": "Okko", "amount": 399, "period": "monthly"},
    {"name": "START", "amount": 399, "period": "monthly"},
    {"name": "Wink", "amount": 299, "period": "monthly"},
    {"name": "Premier", "amount": 299, "period": "monthly"},
    {"name": "Netflix", "amount": 799, "period": "monthly"},
    {"name": "Amediateka", "amount": 599, "period": "monthly"},
    {"name": "KION", "amount": 249, "period": "monthly"},
    {"name": "YouTube Premium", "amount": 299, "period": "monthly"},

    # облако
    {"name": "Яндекс 360", "amount": 249, "period": "monthly"},
    {"name": "Google Drive", "amount": 99, "period": "monthly"},
    {"name": "Apple iCloud", "amount": 149, "period": "monthly"},
    {"name": "Dropbox", "amount": 990, "period": "monthly"},
    {"name": "OneDrive", "amount": 499, "period": "monthly"},
    {"name": "Mail Cloud", "amount": 199, "period": "monthly"},

    # образование
    {"name": "Skillbox", "amount": 1490, "period": "monthly"},
    {"name": "GeekBrains", "amount": 1290, "period": "monthly"},
    {"name": "Skyeng", "amount": 2990, "period": "monthly"},
    {"name": "Нетология", "amount": 1990, "period": "monthly"},
    {"name": "Stepik", "amount": 499, "period": "monthly"},
    {"name": "Яндекс Практикум", "amount": 3990, "period": "monthly"},
    {"name": "Uchi.ru", "amount": 490, "period": "monthly"},

    # игры
    {"name": "Steam", "amount": 699, "period": "monthly"},
    {"name": "Xbox Game Pass", "amount": 899, "period": "monthly"},
    {"name": "PlayStation Plus", "amount": 3299, "period": "yearly"},
    {"name": "VK Play", "amount": 399, "period": "monthly"},
    {"name": "Battle.net", "amount": 599, "period": "monthly"},

    # доставка
    {"name": "Яндекс Плюс", "amount": 399, "period": "monthly"},
    {"name": "Самокат+", "amount": 199, "period": "monthly"},
    {"name": "Ozon Premium", "amount": 199, "period": "monthly"},
    {"name": "Wildberries Plus", "amount": 149, "period": "monthly"},
    {"name": "СберПрайм", "amount": 399, "period": "monthly"},

    # soft
    {"name": "ChatGPT Plus", "amount": 2000, "period": "monthly"},
    {"name": "Notion", "amount": 990, "period": "monthly"},
    {"name": "Canva Pro", "amount": 1290, "period": "monthly"},
    {"name": "Adobe Creative Cloud", "amount": 2990, "period": "monthly"},
    {"name": "Microsoft 365", "amount": 599, "period": "monthly"},
    {"name": "Miro", "amount": 1200, "period": "monthly"},

    # VPN / безопасность
    {"name": "Kaspersky Plus", "amount": 299, "period": "monthly"},
    {"name": "Dr.Web", "amount": 199, "period": "monthly"},
    {"name": "NordVPN", "amount": 1290, "period": "monthly"},
    {"name": "Surfshark", "amount": 1090, "period": "monthly"},

    # книги
    {"name": "ЛитРес", "amount": 399, "period": "monthly"},
    {"name": "MyBook", "amount": 549, "period": "monthly"},
    {"name": "Bookmate", "amount": 499, "period": "monthly"},

    # здоровье
    {"name": "FitStars", "amount": 799, "period": "monthly"},
    {"name": "World Class", "amount": 4990, "period": "monthly"},
    {"name": "Ясно", "amount": 1490, "period": "monthly"},
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
