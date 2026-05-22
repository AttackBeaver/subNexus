from config import PRICE_RISE_THRESHOLD_PERCENT, UNUSED_MONTHLY_DAYS, UNUSED_YEARLY_DAYS
from datetime import timedelta
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def assign_statuses(subscriptions_df, transactions_df, current_date):
    """
    Добавляет статус каждой подписке.
    Возвращает DataFrame с исходными колонками + колонка 'status'.
    """
    if subscriptions_df.empty:
        return pd.DataFrame(columns=list(subscriptions_df.columns) + ['status'])

    result_df = subscriptions_df.copy()
    statuses = []

    for idx, row in result_df.iterrows():
        merchant = row['merchant_name']
        period_days = row['period_days']
        last_payment = row['last_payment_date']
        next_payment = row['next_payment_date']
        first_payment = row['first_payment_date']

        last_payment_date = last_payment.date() if hasattr(
            last_payment, 'date') else last_payment
        next_payment_date = next_payment.date() if hasattr(
            next_payment, 'date') else next_payment

        merchant_txs = transactions_df[transactions_df['merchant_name'] == merchant].sort_values(
            'date')
        amounts = merchant_txs['amount'].values
        dates = merchant_txs['date'].values

        is_trial = False
        if len(amounts) >= 2 and amounts[0] == 0 and any(a > 0 for a in amounts[1:]) and next_payment_date > current_date:
            is_trial = True

        price_rose = False
        non_zero = [a for a in amounts if a > 0]
        if len(non_zero) >= 2:
            first_positive = non_zero[0]
            last_positive = non_zero[-1]
            if first_positive > 0:
                increase = (last_positive - first_positive) / \
                    first_positive * 100
                if increase >= PRICE_RISE_THRESHOLD_PERCENT:
                    price_rose = True
        if not price_rose and len(amounts) >= 3:
            prev_vals = [a for a in amounts[:-1] if a > 0]
            if prev_vals and amounts[-1] > 0:
                median_prev = np.median(prev_vals)
                if median_prev > 0:
                    increase = (amounts[-1] - median_prev) / median_prev * 100
                    if increase >= PRICE_RISE_THRESHOLD_PERCENT:
                        price_rose = True

        unused = False
        is_monthly = 28 <= period_days <= 31
        is_yearly = period_days == 365
        if is_monthly:
            days_since = (current_date - last_payment_date).days
            if days_since > UNUSED_MONTHLY_DAYS:
                unused = True
        elif is_yearly:
            days_since = (current_date - last_payment_date).days
            if days_since > UNUSED_YEARLY_DAYS:
                unused = True

        days_until = (next_payment_date - current_date).days
        upcoming = 1 <= days_until <= 3

        if is_trial:
            status = "Пробный период"
        elif upcoming:
            status = "Скоро списание"
        elif price_rose:
            status = "Цена выросла"
        elif unused:
            status = "Возможно не используется"
        else:
            status = "Активна"

        statuses.append(status)

    result_df['status'] = statuses
    return result_df
