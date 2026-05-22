from config import PRICE_RISE_THRESHOLD_PERCENT, UNUSED_MONTHLY_DAYS, UNUSED_YEARLY_DAYS
from datetime import timedelta
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def assign_statuses(subscriptions_df, transactions_df, current_date):
    """
    Добавляет статус каждой подписке на основе истории транзакций и текущей даты.

    Параметры:
        subscriptions_df (pd.DataFrame): результат работы detect_subscriptions()
        transactions_df (pd.DataFrame): исходные транзакции (date, merchant_name, amount)
        current_date (datetime.date): дата, относительно которой вычисляются статусы

    Возвращает:
        pd.DataFrame: копия subscriptions_df с добавленной колонкой 'status'
    """
    if subscriptions_df.empty:
        return subscriptions_df.copy()

    # Копируем, чтобы не изменять оригинал
    result_df = subscriptions_df.copy()
    statuses = []

    for idx, row in result_df.iterrows():
        merchant = row['merchant_name']
        period_days = row['period_days']
        last_payment = row['last_payment_date']
        next_payment = row['next_payment_date']
        first_payment = row['first_payment_date']

        # Преобразуем pandas.Timestamp в datetime.date для корректного вычитания
        last_payment_date = last_payment.date() if hasattr(
            last_payment, 'date') else last_payment
        next_payment_date = next_payment.date() if hasattr(
            next_payment, 'date') else next_payment

        # Получаем все транзакции этого продавца
        merchant_txs = transactions_df[transactions_df['merchant_name'] == merchant].sort_values(
            'date')
        amounts = merchant_txs['amount'].values
        dates = merchant_txs['date'].values

        # 1. Пробный период
        is_trial = False
        if len(amounts) >= 2:
            # Если первая сумма 0, а вторая (или хотя бы одна из последующих) >0
            # и дата следующего платежа в будущем
            if amounts[0] == 0 and any(a > 0 for a in amounts[1:]) and next_payment_date > current_date:
                is_trial = True

        # 2. Рост цены (сравниваем последние две ненулевые суммы)
        price_rose = False
        non_zero_amounts = [a for a in amounts if a > 0]
        if len(non_zero_amounts) >= 2:
            last_amount = non_zero_amounts[-1]
            prev_amount = non_zero_amounts[-2]
            if prev_amount > 0:
                increase_pct = (last_amount - prev_amount) / prev_amount * 100
                if increase_pct >= PRICE_RISE_THRESHOLD_PERCENT:
                    price_rose = True

        # 3. Возможно не используется
        unused = False
        # Определяем, является ли подписка ежемесячной (интервал 28-31) или годовой (365)
        is_monthly = 28 <= period_days <= 31
        is_yearly = period_days == 365

        if is_monthly:
            days_since_last = (current_date - last_payment_date).days
            if days_since_last > UNUSED_MONTHLY_DAYS:
                unused = True
        elif is_yearly:
            days_since_last = (current_date - last_payment_date).days
            if days_since_last > UNUSED_YEARLY_DAYS:
                unused = True
        # Для недельных и других периодичностей не помечаем как неиспользуемые

        # 4. Скоро списание
        days_until_next = (next_payment_date - current_date).days
        upcoming = 1 <= days_until_next <= 3

        # Определяем итоговый статус
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


# Блок тестирования (запуск файла напрямую)
if __name__ == "__main__":
    from modules.data_generator import generate_user_transactions
    from modules.subscription_detector import detect_subscriptions
    from datetime import date

    # Генерируем данные и находим подписки
    df_trans = generate_user_transactions(6)
    subs_df = detect_subscriptions(df_trans)

    # Текущая дата (симулируем, можно взять сегодня)
    current = date.today()

    # Добавляем статусы
    subs_with_status = assign_statuses(subs_df, df_trans, current)

    print("Подписки со статусами:")
    print(subs_with_status[['merchant_name', 'amount',
          'next_payment_date', 'status']].to_string())
