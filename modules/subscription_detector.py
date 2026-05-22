from config import (
    WEEKLY_INTERVAL_DAYS,
    MONTHLY_INTERVAL_MIN,
    MONTHLY_INTERVAL_MAX,
    YEARLY_INTERVAL_DAYS,
    INTERVAL_TOLERANCE_DAYS,
    MIN_MONTHLY_OCCURRENCES,
    MIN_YEARLY_OCCURRENCES
)
from datetime import timedelta
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def detect_subscriptions(transactions_df):
    """
    Автоматически находит подписки в истории транзакций.

    Параметры:
        transactions_df (pd.DataFrame): date, merchant_name, amount, transaction_id

    Возвращает:
        pd.DataFrame:
            merchant_name, amount (медианная сумма), period_days,
            last_payment_date, next_payment_date, first_payment_date
    """
    if transactions_df.empty:
        return pd.DataFrame(columns=[
            "merchant_name", "amount", "period_days",
            "last_payment_date", "next_payment_date", "first_payment_date"
        ])

    # по продавцу
    grouped = transactions_df.groupby("merchant_name")
    subscriptions = []

    for merchant, group in grouped:
        # по дате
        group = group.sort_values("date")
        dates = group["date"].values
        amounts = group["amount"].values
        n = len(dates)

        if n < 2:
            continue  # минимум 2 платежа

        # интервалы между последовательными платежами (в днях)
        intervals = []
        for i in range(1, n):
            delta = (dates[i] - dates[i-1]) / np.timedelta64(1, 'D')
            intervals.append(int(delta))

        # подходит ли под одну из типовых периодичностей
        #    с учётом допуска INTERVAL_TOLERANCE_DAYS
        #    медианный интервал и проверяем, попадает ли он в один из диапазонов
        median_interval = int(np.median(intervals))

        is_weekly = abs(median_interval -
                        WEEKLY_INTERVAL_DAYS) <= INTERVAL_TOLERANCE_DAYS
        is_monthly = (MONTHLY_INTERVAL_MIN <=
                      median_interval <= MONTHLY_INTERVAL_MAX)
        is_yearly = abs(median_interval -
                        YEARLY_INTERVAL_DAYS) <= INTERVAL_TOLERANCE_DAYS

        period_days = None
        if is_weekly:
            period_days = WEEKLY_INTERVAL_DAYS
        elif is_monthly:
            period_days = median_interval
        elif is_yearly:
            period_days = YEARLY_INTERVAL_DAYS
        else:
            # если не подходит - пропускаем
            continue

        # минимальное количество повторений
        required_occurrences = MIN_MONTHLY_OCCURRENCES
        if is_yearly:
            required_occurrences = MIN_YEARLY_OCCURRENCES
        # weekly/monthly используем MIN_MONTHLY_OCCURRENCES (3)
        if n < required_occurrences:
            continue

        # медианная сумма (пробный 0 или рост цены)
        median_amount = np.median(amounts)

        # последняя дата платежа и первая
        last_date = dates[-1]
        first_date = dates[0]

        # следующая дата платежа (последняя + period_days)
        next_date = last_date + timedelta(days=period_days)

        subscriptions.append({
            "merchant_name": merchant,
            "amount": round(median_amount, 2),
            "period_days": period_days,
            "last_payment_date": last_date,
            "next_payment_date": next_date,
            "first_payment_date": first_date
        })

    result_df = pd.DataFrame(subscriptions)
    return result_df


# тест
if __name__ == "__main__":
    # импорт data_generator
    from modules.data_generator import generate_user_transactions

    # тестовые данные
    df_trans = generate_user_transactions(6)
    print("Сгенерировано транзакций:", len(df_trans))
    print("Пример транзакций:")
    print(df_trans.head(10))

    # детектор
    subs_df = detect_subscriptions(df_trans)
    print("\nОбнаруженные подписки:")
    print(subs_df.to_string())
