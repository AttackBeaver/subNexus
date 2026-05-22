from config import POPULAR_SERVICES, NUM_MONTHS_HISTORY, RANDOM_SEED
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# импорт из config
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_user_transactions(num_months=NUM_MONTHS_HISTORY):
    """
    Генерирует DataFrame с транзакциями пользователя за последние num_months месяцев.

    Возвращает:
        pd.DataFrame с колонками: date, merchant_name, amount, transaction_id
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_months * 30)

    transactions = []
    transaction_counter = 0

    # берем случайные 3-6 подписок
    num_subscriptions = random.randint(3, 6)
    selected_services = random.sample(POPULAR_SERVICES, num_subscriptions)

    # для одной из подписок "рост цены" через 3 месяца
    price_rise_service = random.choice(selected_services)
    # для другой пробный период
    trial_services = [s for s in selected_services if s != price_rise_service]
    trial_service = random.choice(trial_services) if trial_services else None

    # для каждой - транзакция
    for service in selected_services:
        merchant = service["name"]
        base_amount = service["amount"]
        period = service["period"]  # "monthly", "yearly", "weekly"

        # считаем в днях
        if period == "monthly":
            interval_days = random.randint(28, 31)
        elif period == "yearly":
            interval_days = 365
        else:  # weekly
            interval_days = 7

        # первая возможная дата транзакции - не ранее start_date
        # каждые interval_days, начиная с даты, которая попадает в диапазон
        # сгенерируем список дат от start_date до end_date с шагом interval_days
        current_date = start_date
        dates = []
        amounts = []

        # пробный период: первый платёж = 0
        is_trial = (service == trial_service)
        trial_applied = False

        # рост цены: после определённой даты сумма увеличивается
        price_rise_date = None
        if service == price_rise_service:

            pass

        # даты
        first_date = None
        while current_date <= end_date:
            # оставляем хотя бы одну транзакцию
            if current_date >= start_date:
                dates.append(current_date)
                # если пробный период и ещё не было платежа
                if is_trial and not trial_applied:
                    amount = 0.0
                    trial_applied = True  # первый платёж нулевой
                else:
                    amount = base_amount
                    # если установлена дата роста и текущая дата >= дата роста
                    if service == price_rise_service and price_rise_date and current_date >= price_rise_date:
                        amount = base_amount * 1.25  # +25%
                amounts.append(round(amount, 2))
                if first_date is None:
                    first_date = current_date
            current_date += timedelta(days=interval_days)

        # если рост, дата роста = first_date + 3 месяца
        if service == price_rise_service and first_date:
            price_rise_date = first_date + \
                timedelta(days=90)  # примерно 3 месяца
            # считаем суммы для всех транзакций после этой даты
            for i, d in enumerate(dates):
                if d >= price_rise_date:
                    amounts[i] = round(base_amount * 1.25, 2)

        # + транзакции
        for date, amount in zip(dates, amounts):
            transaction_counter += 1
            transactions.append({
                "date": date,
                "merchant_name": merchant,
                "amount": amount,
                "transaction_id": f"tx_{transaction_counter}"
            })

    # нерегулярные платежи
    num_noise = random.randint(10, 15)
    noise_merchants = ["Перекрёсток", "Яндекс.Такси",
                       "Starbucks", "Ozon", "Аптека", "Макдоналдс", "АЗС"]
    for _ in range(num_noise):
        date = fake.date_between(start_date=start_date, end_date=end_date)
        merchant = random.choice(noise_merchants)
        amount = round(random.uniform(50, 5000), 2)
        transaction_counter += 1
        transactions.append({
            "date": date,
            "merchant_name": merchant,
            "amount": amount,
            "transaction_id": f"tx_{transaction_counter}"
        })

    # создаем данные и сортируем по дате
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    return df


# для проверки
if __name__ == "__main__":
    df_test = generate_user_transactions(6)
    print(df_test.head(10))
    print(f"\nВсего транзакций: {len(df_test)}")
    print("Уникальные merchant:", df_test['merchant_name'].unique())
