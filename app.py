import streamlit as st
import pandas as pd
from datetime import date, timedelta
from modules.data_generator import generate_all_users_transactions
from modules.subscription_detector import detect_subscriptions
from modules.status_tracker import assign_statuses
from modules.analytics import total_monthly_cost, top_expensive, simulate_savings, potential_savings

st.set_page_config(page_title="SubNexus", layout="wide", page_icon="📱")

st.markdown("""
<style>
    .main { padding: 0.5rem; }
    /* Карточка клиента */
    .client-card {
        background-color: white;
        border-radius: 24px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: 0.2s;
    }
    .client-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }
    /* Карточка подписки */
    .sub-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 0.5rem;
        margin-bottom: 0.6rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    /* Бейджи статусов */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 500;
        background-color: #e9ecef;
        color: #495057;
    }
    .status-active { background-color: #d4edda; color: #155724; }
    .status-upcoming { background-color: #fff3cd; color: #856404; }
    .status-price-rise { background-color: #f8d7da; color: #721c24; }
    .status-unused { background-color: #e2e3e5; color: #383d41; }
    .status-trial { background-color: #d1ecf1; color: #0c5460; }
    /* Метрики */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* Рекомендация внутри карточки */
    .recommend-inline {
        background-color: #f8f9fa;
        border-radius: 14px;
        padding: 0.6rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        border-left: 3px solid #667eea;
    }
    /* Кнопки в карточках */
    div.stButton > button {
        background-color: #667eea;
        color: white;
        border-radius: 40px;
        border: none;
        font-weight: 500;
        font-size: 0.85rem;
        width: 100%;
        transition: 0.1s;
    }
    div.stButton > button:hover {
        background-color: #5a67d8;
    }
    /* Кнопка внутри карточки клиента */
    .client-card div.stButton > button {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
        width: auto;
        padding: 0.25rem 1rem;
        font-size: 0.8rem;
    }
    .client-card div.stButton > button:hover {
        background-color: #667eea;
        color: white;
        border-color: #667eea;
    }
    .client-card div.stButton {
        text-align: center;
        margin: 0;
    }
    /* Кнопки в карточке подписки */
    .sub-card div.stButton > button {
        padding: 0.3rem;
        font-size: 1rem;
        min-width: 2rem;
    }
    .stRadio > div { flex-direction: row; gap: 0.5rem; }
    hr { margin: 0.5rem 0; }
    /* Горизонтальное расположение кнопок в карточке подписки */
    .sub-card .stButton {
        display: inline-block;
        width: auto;
        margin-right: 4px;
    }
    .sub-card div:has(> div.stButton) {
        display: flex;
        flex-wrap: nowrap;
        gap: 4px;
        justify-content: flex-start;
    }
    .sub-card div.stButton > button {
        white-space: nowrap;
        min-width: 2.5rem;
        padding: 0.3rem 0.5rem;
    }
    /* Принудительное горизонтальное расположение кнопок */
    .stHorizontalBlock {
        gap: 1 !important;
    }
    .stHorizontalBlock .stColumn {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        padding: 0 2px !important;
    }
</style>
""", unsafe_allow_html=True)

if 'users_data' not in st.session_state:
    st.session_state.users_data = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'num_users' not in st.session_state:
    st.session_state.num_users = 100
if 'user_important' not in st.session_state:
    st.session_state.user_important = {}
if 'user_hidden' not in st.session_state:
    st.session_state.user_hidden = {}
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'filter_status' not in st.session_state:
    st.session_state.filter_status = "Все"
if 'user_notify_off' not in st.session_state:
    st.session_state.user_notify_off = {}
if 'user_custom_subs' not in st.session_state:
    st.session_state.user_custom_subs = {}
if 'notifications_sent' not in st.session_state:
    st.session_state.notifications_sent = {}


def load_data(num_users):
    with st.spinner(f"Генерация данных для {num_users} пользователей..."):
        st.session_state.users_data = generate_all_users_transactions(
            num_users)
    keys_to_remove = [k for k in st.session_state.keys()
                      if k.startswith('subs_')]
    for k in keys_to_remove:
        del st.session_state[k]
    st.session_state.user_custom_subs = {}
    for uid in st.session_state.users_data.keys():
        if uid not in st.session_state.user_important:
            st.session_state.user_important[uid] = set()
        if uid not in st.session_state.user_hidden:
            st.session_state.user_hidden[uid] = set()
        if uid not in st.session_state.user_notify_off:
            st.session_state.user_notify_off[uid] = set()
        if uid not in st.session_state.user_custom_subs:
            st.session_state.user_custom_subs[uid] = []

    st.session_state.page = 0
    st.session_state.search_term = ""
    st.session_state.notifications_sent = {}


def get_subscriptions_for_user(user_id):
    # Возвращаем закэшированные подписки
    if f'subs_{user_id}' in st.session_state:
        return st.session_state[f'subs_{user_id}']
    # Иначе вычисляем из транзакций
    transactions = st.session_state.users_data[user_id]
    subs = detect_subscriptions(transactions)
    subs = assign_statuses(subs, transactions, date.today())
    st.session_state[f'subs_{user_id}'] = subs
    return subs


def show_user_detail(user_id):
    st.session_state.current_user = user_id


def back_to_list():
    st.session_state.current_user = None


def add_custom_subscription(user_id, merchant_name, amount, period_days, start_date):
    """Добавляет ручную подписку и обновляет данные пользователя."""
    # Добавляем транзакцию в историю
    new_tx = pd.DataFrame([{
        'date': pd.to_datetime(start_date),
        'merchant_name': merchant_name,
        'amount': amount,
        'transaction_id': f'custom_{user_id}_{len(st.session_state.users_data[user_id])}'
    }])
    st.session_state.users_data[user_id] = pd.concat(
        [st.session_state.users_data[user_id], new_tx], ignore_index=True)

    # Получаем текущий DataFrame подписок или создаём новый
    if f'subs_{user_id}' in st.session_state:
        subs_df = st.session_state[f'subs_{user_id}']
    else:
        subs_df = detect_subscriptions(st.session_state.users_data[user_id])
        subs_df = assign_statuses(
            subs_df, st.session_state.users_data[user_id], date.today())

    # Создаём запись подписки вручную
    last_date = pd.to_datetime(start_date)
    next_date = last_date + timedelta(days=period_days)
    custom_sub_row = {
        'merchant_name': merchant_name,
        'amount': amount,
        'period_days': period_days,
        'last_payment_date': last_date,
        'next_payment_date': next_date,
        'first_payment_date': last_date
    }

    # Добавляем новую строку и обновляем статусы
    new_row_df = pd.DataFrame([custom_sub_row])
    updated_subs = pd.concat([subs_df, new_row_df], ignore_index=True)
    updated_subs = assign_statuses(
        updated_subs, st.session_state.users_data[user_id], date.today())

    # Сохраняем в кэш
    st.session_state[f'subs_{user_id}'] = updated_subs

    # Сохраняем в user_custom_subs для информации
    if user_id not in st.session_state.user_custom_subs:
        st.session_state.user_custom_subs[user_id] = []
    st.session_state.user_custom_subs[user_id].append(custom_sub_row)


def show_auto_notifications(user_id, visible_df, notify_off_set, total_visible):
    """Показывает автоматические уведомления для текущего пользователя"""
    sent = st.session_state.notifications_sent.get(user_id, set())
    today = date.today()

    # Уведомления для каждой подписки
    for _, row in visible_df.iterrows():
        merchant = row['merchant_name']
        status = row['status']
        # Пропускаем, если уведомления отключены для этой подписки
        if merchant in notify_off_set:
            continue

        # Ключ для уникальности
        if status == "Скоро списание":
            days = (row['next_payment_date'].date() - today).days
            if 1 <= days <= 3:
                key = f"{user_id}_{merchant}_upcoming"
                if key not in sent:
                    st.toast(
                        f"⏰ Через {days} дня(ей) спишется {row['amount']} ₽ за {merchant}.", icon="🔔")
                    sent.add(key)
        elif status == "Цена выросла":
            key = f"{user_id}_{merchant}_price_rise"
            if key not in sent:
                st.toast(
                    f"📈 Стоимость {merchant} выросла. Текущая цена {row['amount']} ₽.", icon="📈")
                sent.add(key)
        elif status == "Пробный период":
            next_pay = row['next_payment_date'].date()
            days_left = (next_pay - today).days
            if days_left >= 0:
                key = f"{user_id}_{merchant}_trial"
                if key not in sent:
                    st.toast(
                        f"⚠️ Пробный период {merchant} заканчивается через {days_left} дней. Затем списание {row['amount']} ₽/мес.", icon="⏳")
                    sent.add(key)

    # Ежемесячное сводное уведомление
    summary_key = f"{user_id}_monthly_summary"
    if summary_key not in sent:
        num_subs = len(visible_df)
        if num_subs > 0:
            st.toast(
                f"📊 Вы платите за {num_subs} подписок, общая сумма — {total_visible} ₽ в месяц.", icon="💰")
            sent.add(summary_key)

    # Сохраняем отправленные уведомления
    st.session_state.notifications_sent[user_id] = sent


# Главная страница
if st.session_state.current_user is None:
    st.image(image='src/logo.png')
    st.title("SubNexus")
    st.caption("Разработано командой 418:I'm teapot, в рамках чемпионата: Технологии больших данных и искусственного интеллекта")
    st.markdown("### Управление подписками в вашем банке")

    with st.form("gen_form"):
        num_users = st.number_input(
            "Количество клиентов", min_value=10, max_value=500, value=st.session_state.num_users, step=50)
        submitted = st.form_submit_button(
            "Сгенерировать данные", use_container_width=True)
        if submitted:
            st.session_state.num_users = num_users
            load_data(num_users)
            st.rerun()

    if st.session_state.users_data is not None:
        search = st.text_input(
            "Поиск по ID клиента", value=st.session_state.search_term, key="search_input")
        if search != st.session_state.search_term:
            st.session_state.search_term = search
            st.session_state.page = 0

        # Фильтр по проблемам
        filter_options = ["Все", "Лишние", "Пробный период", "Рост цены"]
        current_filter = st.radio(
            "Фильтр по проблемам:",
            options=filter_options,
            index=filter_options.index(st.session_state.filter_status),
            horizontal=True,
            key="filter_radio",
            on_change=lambda: None
        )
        # Обновляем состояние, но не делаем rerun
        if current_filter != st.session_state.filter_status:
            st.session_state.filter_status = current_filter
            st.session_state.page = 0

        user_ids = sorted(st.session_state.users_data.keys())
        if st.session_state.search_term:
            try:
                search_int = int(st.session_state.search_term)
                user_ids = [uid for uid in user_ids if uid == search_int]
            except ValueError:
                pass

        filtered_ids = []
        for uid in user_ids:
            if f'subs_{uid}' not in st.session_state:
                st.session_state[f'subs_{uid}'] = get_subscriptions_for_user(
                    uid)
            subs_df = st.session_state[f'subs_{uid}']
            if st.session_state.filter_status == "Лишние":
                if any(subs_df['status'] == "Возможно не используется"):
                    filtered_ids.append(uid)
            elif st.session_state.filter_status == "Пробный период":
                if any(subs_df['status'] == "Пробный период"):
                    filtered_ids.append(uid)
            elif st.session_state.filter_status == "Рост цены":
                if any(subs_df['status'] == "Цена выросла"):
                    filtered_ids.append(uid)
            else:
                filtered_ids.append(uid)
        user_ids = filtered_ids

        page_size = 10
        total_pages = max(1, (len(user_ids) + page_size - 1) // page_size)
        start = st.session_state.page * page_size
        end = start + page_size
        paginated_ids = user_ids[start:end]

        for uid in paginated_ids:
            subs_df = st.session_state[f'subs_{uid}']
            transactions = st.session_state.users_data[uid]
            visible_subs = subs_df[~subs_df['merchant_name'].isin(
                st.session_state.user_hidden.get(uid, set()))]
            total_cost = total_monthly_cost(visible_subs)
            has_unused = any(visible_subs['status']
                             == "Возможно не используется")
            has_trial = any(visible_subs['status'] == "Пробный период")
            has_price_rise = any(visible_subs['status'] == "Цена выросла")

            with st.container():
                st.markdown(f"""
                <div class="client-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <strong style="font-size: 1.2rem;">👤 Клиент {uid}</strong>
                        </div>
                        <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                """, unsafe_allow_html=True)
                if has_unused:
                    st.markdown(
                        '<span class="status-badge status-unused">Лишние</span>', unsafe_allow_html=True)
                if has_trial:
                    st.markdown(
                        '<span class="status-badge status-trial">Пробный период</span>', unsafe_allow_html=True)
                if has_price_rise:
                    st.markdown(
                        '<span class="status-badge status-price-rise">Рост цены</span>', unsafe_allow_html=True)
                st.markdown(f"""
                        </div>
                    </div>
                    <div style="margin-top: 0.1rem;">
                        <div>Транзакций: {len(transactions)}</div>
                        <div>Подписок: {len(visible_subs)}</div>
                        <div><strong>{total_cost} ₽/мес</strong></div>
                    </div>
                """, unsafe_allow_html=True)
                col_left, col_right = st.columns([2, 1])
                with col_right:
                    if st.button("Подробнее", key=f"btn_{uid}", use_container_width=False):
                        show_user_detail(uid)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                col_left, col_right = st.columns(2)
                with col_left:
                    if st.button("← Предыдущая", disabled=(st.session_state.page == 0)):
                        st.session_state.page -= 1
                        st.rerun()
                with col_right:
                    if st.button("Следующая →", disabled=(st.session_state.page >= total_pages-1)):
                        st.session_state.page += 1
                        st.rerun()
            st.caption(f"Страница {st.session_state.page+1} из {total_pages}")
        st.caption(
            f"Показано {len(paginated_ids)} из {len(user_ids)} клиентов (всего {len(st.session_state.users_data)})")

# Страница клиента
else:
    user_id = st.session_state.current_user
    if st.button("← Назад к списку клиентов", use_container_width=False):
        back_to_list()
        st.rerun()

    st.header(f"👤 Клиент {user_id}")

    transactions = st.session_state.users_data[user_id]
    subs_df = get_subscriptions_for_user(user_id)
    important_set = st.session_state.user_important.get(user_id, set())
    hidden_set = st.session_state.user_hidden.get(user_id, set())
    notify_off_set = st.session_state.user_notify_off.get(user_id, set())

    # Видимые подписки
    visible_df = subs_df[~subs_df['merchant_name'].isin(hidden_set)]
    total_visible = total_monthly_cost(visible_df)
    # Автоматические уведомления
    show_auto_notifications(user_id, visible_df, notify_off_set, total_visible)

    # Метрики
    st.metric("Общая сумма", f"{total_visible} ₽/мес")
    st.metric("Подписок", len(visible_df))
    _, amt = potential_savings(visible_df, important_set)
    st.metric("Потенциальная экономия", f"{amt} ₽/мес")

    # Самые дорогие
    top = top_expensive(visible_df, 3)
    if top:
        st.markdown("#### Самые дорогие подписки")
        for t in top:
            st.info(f"**{t['merchant_name']}**: {t['monthly_cost']} ₽/мес")

    # Форма ручного добавления подписки
    with st.expander("➕ Добавить подписку вручную"):
        with st.form(key=f"add_sub_form_{user_id}"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input(
                    "Название сервиса", placeholder="например, Яндекс.Плюс")
                new_amount = st.number_input(
                    "Сумма (₽)", min_value=0.0, step=50.0)
            with col2:
                period_options = {"Ежемесячно": 30,
                                  "Еженедельно": 7, "Ежегодно": 365}
                period_choice = st.selectbox(
                    "Периодичность", list(period_options.keys()))
                period_days = period_options[period_choice]
                start_date = st.date_input(
                    "Дата первого платежа", value=date.today())
            submitted = st.form_submit_button("Добавить")
            if submitted and new_name:
                add_custom_subscription(
                    user_id, new_name, new_amount, period_days, start_date)
                st.success(f"Подписка {new_name} добавлена!")
                st.rerun()

    # Фильтры
    filter_option = st.radio(
        "Фильтр подписок:",
        ["Все", "Редко используемые", "Дорогие", "Скоро спишут"],
        horizontal=True,
        key="sub_filter"
    )
    display_df = visible_df.copy()
    if filter_option == "Редко используемые":
        display_df = display_df[display_df['status']
                                == "Возможно не используется"]
    elif filter_option == "Дорогие":
        monthly_cost = []
        for _, r in display_df.iterrows():
            p = r['period_days']
            a = r['amount']
            if p == 365:
                mon = a / 12
            elif p == 7:
                mon = a * (30/7)
            else:
                mon = a
            monthly_cost.append(mon)
        display_df = display_df.copy()
        display_df['monthly_cost'] = monthly_cost
        display_df = display_df.nlargest(3, 'monthly_cost')
    elif filter_option == "Скоро спишут":
        display_df = display_df[display_df['status'] == "Скоро списание"]

    st.subheader("Мои подписки")
    if display_df.empty:
        st.warning("Нет подписок по выбранному фильтру.")
    else:
        for _, row in display_df.iterrows():
            merchant = row['merchant_name']
            status = row['status']
            amount = row['amount']
            next_date = row['next_payment_date'].strftime('%d.%m.%Y')
            is_important = merchant in important_set

            status_class = "status-badge"
            if status == "Активна":
                status_class += " status-active"
            elif status == "Скоро списание":
                status_class += " status-upcoming"
            elif status == "Цена выросла":
                status_class += " status-price-rise"
            elif status == "Возможно не используется":
                status_class += " status-unused"
            elif status == "Пробный период":
                status_class += " status-trial"

            # Рекомендация
            recommendation = None
            if status in ["Возможно не используется", "Цена выросла", "Пробный период", "Скоро списание"]:
                if status == "Возможно не используется":
                    last_date = row['last_payment_date'].date()
                    days_ago = (date.today() - last_date).days
                    rec_text = f"Вы не пользовались сервисом более {days_ago} дней. Возможно, он вам больше не нужен."
                    savings = total_monthly_cost(pd.DataFrame([row]))
                elif status == "Цена выросла":
                    merchant_txs = transactions[transactions['merchant_name'] == merchant].sort_values(
                        'date')
                    amounts_list = merchant_txs['amount'].values
                    non_zero = [a for a in amounts_list if a > 0]
                    if len(non_zero) >= 2:
                        old_price = non_zero[0]
                        new_price = non_zero[-1]
                        if old_price == new_price and len(non_zero) > 2:
                            old_price = non_zero[-2]
                        if old_price != new_price:
                            inc = (new_price - old_price) / old_price * 100
                            rec_text = f"Стоимость выросла с {old_price:.2f} ₽ до {new_price:.2f} ₽ (+{inc:.0f}%)."
                        else:
                            rec_text = f"Стоимость выросла (текущая {amount} ₽). Рекомендуем проверить условия."
                    else:
                        rec_text = f"Стоимость выросла (текущая {amount} ₽)."
                    savings = 0
                elif status == "Пробный период":
                    next_pay = row['next_payment_date'].date()
                    days_left = (next_pay - date.today()).days
                    rec_text = f"Пробный период заканчивается через {days_left} дней. Затем начнётся списание {amount} ₽/мес."
                    savings = total_monthly_cost(pd.DataFrame([row]))
                elif status == "Скоро списание":
                    next_pay = row['next_payment_date'].date()
                    days_left = (next_pay - date.today()).days
                    rec_text = f"Через {days_left} дня(ей) спишется {amount} ₽."
                    savings = 0
                recommendation = (rec_text, savings)

            # Карточка подписки
            with st.container():
                st.markdown(f"""
                <div class="sub-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <strong>{merchant}</strong><br>
                            <span style="font-size: 0.9rem;">{amount} ₽ • {next_date}</span>
                        </div>
                        <div>
                            <span class="{status_class}">{status}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                is_notify_off = merchant in notify_off_set
                # Горизонтальный ряд кнопок
                col_imp, col_notify, col_hide, col_wrong = st.columns(
                    4, gap="small")
                with col_imp:
                    icon = "⭐" if not is_important else "⭐ ✓"
                    if st.button(icon, key=f"imp_{user_id}_{merchant}", help="Важная"):
                        if is_important:
                            st.session_state.user_important[user_id].discard(
                                merchant)
                        else:
                            st.session_state.user_important[user_id].add(
                                merchant)
                        st.rerun()
                with col_notify:
                    notify_icon = "🔕" if is_notify_off else "🔔"
                    if st.button(notify_icon, key=f"notify_{user_id}_{merchant}", help="Уведомления"):
                        if is_notify_off:
                            st.session_state.user_notify_off[user_id].discard(
                                merchant)
                        else:
                            st.session_state.user_notify_off[user_id].add(
                                merchant)
                        st.rerun()
                with col_hide:
                    if st.button("👁️‍🗨️", key=f"hide_{user_id}_{merchant}", help="Скрыть"):
                        st.session_state.user_hidden[user_id].add(merchant)
                        st.rerun()
                with col_wrong:
                    if st.button("⚠️", key=f"wrong_{user_id}_{merchant}", help="Ошибочна"):
                        st.session_state.user_hidden[user_id].add(merchant)
                        st.rerun()

                if recommendation:
                    rec_text, savings = recommendation
                    st.markdown(f"""
                    <div class="recommend-inline">
                        <strong>Рекомендация:</strong> {rec_text}
                    """, unsafe_allow_html=True)
                    if savings > 0:
                        st.caption(
                            f"Потенциальная экономия: **{savings:.2f} ₽/мес**, если отключить.")
                    else:
                        st.caption(
                            f"Рекомендуем проверить целесообразность.")
                    if status in ["Возможно не используется", "Пробный период"]:
                        if st.button(f"Смоделировать отключение", key=f"sim_{user_id}_{merchant}"):
                            new_total = simulate_savings(
                                visible_df, [merchant])
                            st.success(
                                f"Если отключить {merchant}, ежемесячные траты снизятся с {total_visible} ₽ до {new_total} ₽ (экономия {total_visible - new_total:.2f} ₽/мес).")
                    st.markdown("</div>", unsafe_allow_html=True)

    # Тестирование уведомлений
    st.subheader("Тестирование уведомлений")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Скоро списание"):
            upcoming = visible_df[visible_df['status'] == "Скоро списание"]
            if not upcoming.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} ({r['amount']} ₽)" for _, r in upcoming.iterrows()])
                st.toast(f"⏰ Через 1-3 дня спишется: {msg}", icon="🔔")
            else:
                st.toast("Нет подписок с ближайшим списанием", icon="ℹ️")
        if st.button("Рост цены"):
            price_rise = visible_df[visible_df['status'] == "Цена выросла"]
            if not price_rise.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} (теперь {r['amount']} ₽)" for _, r in price_rise.iterrows()])
                st.toast(f"💰 Цена выросла: {msg}", icon="📈")
            else:
                st.toast("Нет подписок с ростом цены", icon="ℹ️")
    with col2:
        if st.button("Пробный период"):
            trial = visible_df[visible_df['status'] == "Пробный период"]
            if not trial.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} (след. списание {r['amount']} ₽)" for _, r in trial.iterrows()])
                st.toast(f"⚠️ Пробный период заканчивается: {msg}", icon="⏳")
            else:
                st.toast("Нет подписок в пробном периоде", icon="ℹ️")
        if st.button("Лишняя подписка"):
            unused_names, amt = potential_savings(visible_df, important_set)
            if unused_names:
                st.toast(
                    f"💡 Обнаружены редко используемые подписки: {', '.join(unused_names)}. Экономия ~{amt} ₽/мес", icon="💡")
            else:
                st.toast("Лишних подписок не найдено", icon="✅")

    with st.expander("Все транзакции клиента"):
        st.dataframe(transactions, use_container_width=True, height=300)
