from config import (
    WEEKLY_INTERVAL_DAYS, MONTHLY_INTERVAL_MIN, MONTHLY_INTERVAL_MAX,
    YEARLY_INTERVAL_DAYS, INTERVAL_TOLERANCE_DAYS,
    MIN_MONTHLY_OCCURRENCES, MIN_YEARLY_OCCURRENCES,
    BLACKLIST_MERCHANTS, MIN_SUBSCRIPTION_AMOUNT, MAX_CV_FOR_SUBSCRIPTION
)
from datetime import timedelta
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def detect_subscriptions(transactions_df):
    if transactions_df.empty:
        return pd.DataFrame(columns=[
            "merchant_name", "amount", "period_days",
            "last_payment_date", "next_payment_date", "first_payment_date"
        ])

    grouped = transactions_df.groupby("merchant_name")
    subscriptions = []

    for merchant, group in grouped:
        if merchant in BLACKLIST_MERCHANTS:
            continue

        group = group.sort_values("date")
        dates = group["date"].values
        amounts = group["amount"].values
        n = len(dates)
        if n < 2:
            continue

        median_amount = np.median(amounts)
        if median_amount < MIN_SUBSCRIPTION_AMOUNT and all(a == 0 for a in amounts):
            continue

        intervals = []
        for i in range(1, n):
            delta = (dates[i] - dates[i-1]) / np.timedelta64(1, 'D')
            intervals.append(int(delta))

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
            continue

        required = MIN_MONTHLY_OCCURRENCES if not is_yearly else MIN_YEARLY_OCCURRENCES
        if n < required:
            continue

        last_date = dates[-1]
        first_date = dates[0]
        next_date = last_date + timedelta(days=period_days)

        median_amount = np.median(amounts)

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
