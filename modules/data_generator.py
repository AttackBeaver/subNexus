from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from config import (
    POPULAR_SERVICES, NUM_MONTHS_HISTORY, RANDOM_SEED, BLACKLIST_MERCHANTS,
    UNUSED_PROBABILITY, UNUSED_MONTHLY_DAYS,
    TRIAL_PROBABILITY, PRICE_RISE_PROBABILITY
)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_user_transactions(num_months=NUM_MONTHS_HISTORY, user_id=0):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_months * 30)

    transactions = []
    transaction_counter = 0

    available_services = [
        s for s in POPULAR_SERVICES if s['name'] not in BLACKLIST_MERCHANTS]
    num_subs = random.randint(4, 15)
    selected = random.sample(available_services, min(
        num_subs, len(available_services)))

    for service in selected:
        merchant = service["name"]
        base_amount = service["amount"]
        period = service["period"]

        has_trial = random.random() < TRIAL_PROBABILITY
        has_price_rise = random.random() < PRICE_RISE_PROBABILITY

        is_unused = random.random() < UNUSED_PROBABILITY

        if period == "monthly":
            interval_days = random.randint(28, 31)
        elif period == "yearly":
            interval_days = 365
        else:
            interval_days = 7

        dates = []
        amounts = []
        current = start_date
        first_date = None

        while current <= end_date:
            if current >= start_date:
                dates.append(current)
                if first_date is None:
                    first_date = current
            current += timedelta(days=interval_days)

        price_rise_date = None
        if has_price_rise and first_date:
            price_rise_date = first_date + timedelta(days=30)

        cutoff_date = end_date - timedelta(days=UNUSED_MONTHLY_DAYS)
        if is_unused:
            dates = [d for d in dates if d <= cutoff_date]

        trial_applied = False
        for d in dates:
            if has_trial and not trial_applied:
                amount = 0.0
                trial_applied = True
            else:
                amount = base_amount
                if has_price_rise and price_rise_date and d >= price_rise_date:
                    amount = base_amount * 1.25
            amounts.append(round(amount, 2))

        for d, am in zip(dates, amounts):
            transaction_counter += 1
            transactions.append({
                "date": d,
                "merchant_name": merchant,
                "amount": am,
                "transaction_id": f"tx_{user_id}_{transaction_counter}"
            })

    num_noise = random.randint(10, 15)
    for _ in range(num_noise):
        date_noise = fake.date_between(
            start_date=start_date, end_date=end_date)
        merchant = random.choice(BLACKLIST_MERCHANTS)
        amount = round(random.uniform(50, 5000), 2)
        transaction_counter += 1
        transactions.append({
            "date": date_noise,
            "merchant_name": merchant,
            "amount": amount,
            "transaction_id": f"tx_{user_id}_{transaction_counter}"
        })

    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    return df


def generate_all_users_transactions(num_users=100):
    users_data = {}
    for uid in range(num_users):
        users_data[uid] = generate_user_transactions(NUM_MONTHS_HISTORY, uid)
    return users_data
