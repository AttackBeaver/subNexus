# Пороги детекции
MIN_MONTHLY_OCCURRENCES = 3
MIN_YEARLY_OCCURRENCES = 2
WEEKLY_INTERVAL_DAYS = 7
MONTHLY_INTERVAL_MIN = 28
MONTHLY_INTERVAL_MAX = 31
YEARLY_INTERVAL_DAYS = 365
INTERVAL_TOLERANCE_DAYS = 2

# Пороги для статусов
PRICE_RISE_THRESHOLD_PERCENT = 20
UNUSED_MONTHLY_DAYS = 60
UNUSED_YEARLY_DAYS = 330  # примерно 11 месяцев

# Дата
SIMULATED_CURRENT_DATE = None

# Справочник: сервис - категория
MERCHANT_CATEGORIES = {
    "Яндекс.Музыка": "Музыка",
    "Netflix": "Видео",
    "IVI": "Видео",
    "Apple iCloud": "Хранилище",
    "Skillbox": "Образование",
    "Spotify": "Музыка",
    "Amazon Prime": "Видео",
    "Google Drive": "Хранилище",
}

# Популярные сервисы
POPULAR_SERVICES = [
    {"name": "Яндекс.Музыка", "amount": 299, "period": "monthly"},
    {"name": "Netflix", "amount": 799, "period": "monthly"},
    {"name": "IVI", "amount": 199, "period": "monthly"},
    {"name": "Apple iCloud", "amount": 149, "period": "monthly"},
    {"name": "Skillbox", "amount": 1490, "period": "monthly"},
    {"name": "Spotify", "amount": 189, "period": "monthly"},
    {"name": "Amazon Prime", "amount": 499, "period": "yearly"},
    {"name": "Google Drive", "amount": 99, "period": "monthly"},
]

# Дополнительно
NUM_MONTHS_HISTORY = 6
RANDOM_SEED = 42
