import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def total_monthly_cost(subscriptions_df):
    """
    Рассчитывает общую сумму всех подписок в месяц.
    Приводит годовую и недельную стоимость к месячной.

    Параметры:
        subscriptions_df (pd.DataFrame): с колонками amount, period_days

    Возвращает:
        float: общая сумма в месяц
    """
    if subscriptions_df.empty:
        return 0.0

    total = 0.0
    for _, row in subscriptions_df.iterrows():
        amount = row['amount']
        period = row['period_days']

        if period == 365:  # годовая
            monthly = amount / 12
        elif period == 7:  # недельная
            monthly = amount * (30 / 7)  # ~4.2857 недель в месяце
        else:  # месячная (28-31 день)
            monthly = amount

        total += monthly

    return round(total, 2)


def top_expensive(subscriptions_df, n=3):
    """
    Возвращает топ N самых дорогих подписок по месячной стоимости.

    Параметры:
        subscriptions_df (pd.DataFrame): с колонками merchant_name, amount, period_days
        n (int): количество подписок в топе

    Возвращает:
        list of dict: [{"merchant_name": ..., "monthly_cost": ...}, ...]
    """
    if subscriptions_df.empty:
        return []

    # считаем месячную стоимость для каждой подписки
    monthly_costs = []
    for _, row in subscriptions_df.iterrows():
        amount = row['amount']
        period = row['period_days']

        if period == 365:
            monthly = amount / 12
        elif period == 7:
            monthly = amount * (30 / 7)
        else:
            monthly = amount

        monthly_costs.append({
            "merchant_name": row['merchant_name'],
            "monthly_cost": round(monthly, 2)
        })

    # по убыванию и берём первые n
    monthly_costs.sort(key=lambda x: x['monthly_cost'], reverse=True)
    return monthly_costs[:n]


def potential_savings(subscriptions_df, important_subscriptions=None):
    """
    Определяет потенциальную экономию, выбирая подписки со статусом
    «Возможно не используется» (до 2-х), исключая важные.

    Параметры:
        subscriptions_df (pd.DataFrame): с колонками merchant_name, status, amount, period_days
        important_subscriptions (set): названия подписок, отмеченных как важные

    Возвращает:
        tuple: (список названий, сумма экономии в месяц)
    """
    if subscriptions_df.empty:
        return [], 0.0

    important = important_subscriptions or set()

    # подписки со статусом "Возможно не используется" и не важные
    unused = subscriptions_df[
        (subscriptions_df['status'] == "Возможно не используется") &
        (~subscriptions_df['merchant_name'].isin(important))
    ]

    # не более 2-х самых дорогих из них
    if len(unused) > 2:
        # считаем месячную стоимость для сортировки
        unused_with_monthly = unused.copy()
        monthly_vals = []
        for _, row in unused_with_monthly.iterrows():
            amount = row['amount']
            period = row['period_days']
            if period == 365:
                monthly = amount / 12
            elif period == 7:
                monthly = amount * (30 / 7)
            else:
                monthly = amount
            monthly_vals.append(monthly)
        unused_with_monthly['monthly'] = monthly_vals
        unused = unused_with_monthly.nlargest(2, 'monthly')

    names = unused['merchant_name'].tolist()

    # считаем сумму экономии
    savings = 0.0
    for _, row in unused.iterrows():
        amount = row['amount']
        period = row['period_days']
        if period == 365:
            savings += amount / 12
        elif period == 7:
            savings += amount * (30 / 7)
        else:
            savings += amount

    return names, round(savings, 2)


def simulate_savings(subscriptions_df, subscription_names_to_disable):
    """
    Симулирует экономию при отключении переданных подписок.

    Параметры:
        subscriptions_df (pd.DataFrame): с колонками merchant_name, amount, period_days
        subscription_names_to_disable (list): названия подписок для отключения

    Возвращает:
        float: новая общая сумма в месяц после отключения
    """
    if subscriptions_df.empty:
        return 0.0

    # копируем и удаляем указанные подписки
    filtered_df = subscriptions_df[~subscriptions_df['merchant_name'].isin(
        subscription_names_to_disable)]

    return total_monthly_cost(filtered_df)


# тест
if __name__ == "__main__":
    from modules.data_generator import generate_user_transactions
    from modules.subscription_detector import detect_subscriptions
    from modules.status_tracker import assign_statuses
    from datetime import date

    # генерим
    df_trans = generate_user_transactions(6)
    subs_df = detect_subscriptions(df_trans)

    # статусы
    current = date.today()
    subs_df = assign_statuses(subs_df, df_trans, current)

    # аналитика
    total = total_monthly_cost(subs_df)
    print(f"Общая сумма в месяц: {total} руб.")

    top = top_expensive(subs_df, 3)
    print("Топ-3 дорогих подписок:")
    for t in top:
        print(f"  {t['merchant_name']}: {t['monthly_cost']} руб/мес")

    savings_names, savings_amount = potential_savings(subs_df)
    print(
        f"Потенциальная экономия (отключив {savings_names}): {savings_amount} руб/мес")

    new_total = simulate_savings(subs_df, savings_names)
    print(f"Новая сумма после отключения: {new_total} руб/мес")
