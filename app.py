import streamlit as st
import pandas as pd
from datetime import date
from modules.data_generator import generate_all_users_transactions
from modules.subscription_detector import detect_subscriptions
from modules.status_tracker import assign_statuses
from modules.analytics import total_monthly_cost, top_expensive, simulate_savings, potential_savings


st.set_page_config(page_title="SubNexus", layout="centered", page_icon="📱")

st.markdown("""
<style>
    .main > div { max-width: 1100px; margin: 0 auto; }
    .badge-warning { background-color: #f8d7da; color: #721c24; border-radius: 40px; padding: 2px 8px; font-size: 12px; white-space: nowrap; }
    .badge-ok { background-color: #d4edda; color: #155724; border-radius: 40px; padding: 2px 8px; font-size: 12px; white-space: nowrap; }
    .status-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; background-color: #e9ecef; color: #495057; }
    .status-active { background-color: #d4edda; color: #155724; }
    .status-upcoming { background-color: #fff3cd; color: #856404; }
    .status-price-rise { background-color: #f8d7da; color: #721c24; }
    .status-unused { background-color: #e2e3e5; color: #383d41; }
    .status-trial { background-color: #d1ecf1; color: #0c5460; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 24px; padding: 1.5rem; color: white; text-align: center; margin-bottom: 1.5rem; }
    .savings-card { background: #d1e7dd; border-left: 6px solid #198754; border-radius: 16px; padding: 1rem; margin: 1rem 0; }
    div.stButton > button { background-color: #667eea; color: white; border-radius: 40px; padding: 0.5rem 1rem; border: none; width: 100%; font-weight: 500; }
    div.stButton > button:hover { background-color: #5a67d8; }
    hr { margin: 0.5rem 0; }
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
if 'filter_unused' not in st.session_state:
    st.session_state.filter_unused = False
if 'filter_trial' not in st.session_state:
    st.session_state.filter_trial = False
if 'filter_price_rise' not in st.session_state:
    st.session_state.filter_price_rise = False


def load_data(num_users):
    with st.spinner(f"Генерация данных для {num_users} пользователей..."):
        st.session_state.users_data = generate_all_users_transactions(
            num_users)
    keys_to_remove = [k for k in st.session_state.keys()
                      if k.startswith('subs_')]
    for k in keys_to_remove:
        del st.session_state[k]
    for uid in st.session_state.users_data.keys():
        if uid not in st.session_state.user_important:
            st.session_state.user_important[uid] = set()
        if uid not in st.session_state.user_hidden:
            st.session_state.user_hidden[uid] = set()
    st.session_state.page = 0
    st.session_state.search_term = ""


def get_subscriptions_for_user(user_id):
    transactions = st.session_state.users_data[user_id]
    subs = detect_subscriptions(transactions)
    subs = assign_statuses(subs, transactions, date.today())
    return subs


def show_user_detail(user_id):
    st.session_state.current_user = user_id


def back_to_list():
    st.session_state.current_user = None


if st.session_state.current_user is None:
    st.title("SubNexus")
    st.markdown("### Управление подписками в вашем банке")

    with st.form("gen_form"):
        num_users = st.number_input(
            "Количество клиентов", min_value=10, max_value=500, value=st.session_state.num_users, step=10)
        submitted = st.form_submit_button(
            "Сгенерировать данные", use_container_width=True)
        if submitted:
            st.session_state.num_users = num_users
            load_data(num_users)
            st.rerun()

    if st.session_state.users_data is not None:
        st.markdown("---")
        col_search, col_filter1, col_filter2, col_filter3 = st.columns([
                                                                       2, 1, 1, 1])
        with col_search:
            search = st.text_input(
                "Поиск по ID клиента", value=st.session_state.search_term)
        with col_filter1:
            st.session_state.filter_unused = st.checkbox(
                "Лишние", value=st.session_state.filter_unused)
        with col_filter2:
            st.session_state.filter_trial = st.checkbox(
                "Пробный период", value=st.session_state.filter_trial)
        with col_filter3:
            st.session_state.filter_price_rise = st.checkbox(
                "Рост цены", value=st.session_state.filter_price_rise)

        if search != st.session_state.search_term:
            st.session_state.search_term = search
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
            cond_unused = (not st.session_state.filter_unused) or any(
                subs_df['status'] == "Возможно не используется")
            cond_trial = (not st.session_state.filter_trial) or any(
                subs_df['status'] == "Пробный период")
            cond_price = (not st.session_state.filter_price_rise) or any(
                subs_df['status'] == "Цена выросла")
            if cond_unused and cond_trial and cond_price:
                filtered_ids.append(uid)
        user_ids = filtered_ids

        page_size = 20
        total_pages = max(1, (len(user_ids) + page_size - 1) // page_size)
        start = st.session_state.page * page_size
        end = start + page_size
        paginated_ids = user_ids[start:end]

        cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
        with cols[0]:
            st.markdown("**👤**")
        with cols[1]:
            st.markdown("**📊**")
        with cols[2]:
            st.markdown("**📦**")
        with cols[3]:
            st.markdown("**💰**")
        with cols[4]:
            st.markdown("**🧹**")
        with cols[5]:
            st.markdown("**🎁**")
        with cols[6]:
            st.markdown("**📈**")

        for uid in paginated_ids:
            subs_df = st.session_state[f'subs_{uid}']
            transactions = st.session_state.users_data[uid]
            total_cost = total_monthly_cost(subs_df)
            has_unused = any(subs_df['status'] == "Возможно не используется")
            has_trial = any(subs_df['status'] == "Пробный период")
            has_price_rise = any(subs_df['status'] == "Цена выросла")

            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
                [1, 1, 1, 1, 1, 1, 1, 1])
            with col1:
                st.write(f"{uid}")
            with col2:
                st.write(f"{len(transactions)}")
            with col3:
                st.write(f"**{len(subs_df)}**")
            with col4:
                st.write(f"**{total_cost} ₽**")
            with col5:
                st.markdown(
                    '<span class="badge-warning">Найдено</span>' if has_unused else '<span class="badge-ok">Не найдено</span>', unsafe_allow_html=True)
            with col6:
                st.markdown(
                    '<span class="badge-warning">Найдено</span>' if has_trial else '<span class="badge-ok">Не найдено</span>', unsafe_allow_html=True)
            with col7:
                st.markdown(
                    '<span class="badge-warning">Найдено</span>' if has_price_rise else '<span class="badge-ok">Не найдено</span>', unsafe_allow_html=True)
            with col8:
                if st.button("→", key=f"btn_{uid}"):
                    show_user_detail(uid)
                    st.rerun()
            st.divider()

        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                left, right = st.columns(2)
                with left:
                    if st.button("← Предыдущая", disabled=(st.session_state.page == 0)):
                        st.session_state.page -= 1
                        st.rerun()
                with right:
                    if st.button("Следующая →", disabled=(st.session_state.page >= total_pages-1)):
                        st.session_state.page += 1
                        st.rerun()
            st.caption(f"Страница {st.session_state.page+1} из {total_pages}")
        st.caption(
            f"Показано {len(paginated_ids)} из {len(user_ids)} клиентов (всего {len(st.session_state.users_data)})")

else:
    user_id = st.session_state.current_user
    if st.button("← Назад к списку клиентов"):
        back_to_list()
        st.rerun()

    st.header(f"Клиент {user_id}")

    transactions = st.session_state.users_data[user_id]
    subs_df = get_subscriptions_for_user(user_id)
    important_set = st.session_state.user_important.get(user_id, set())
    hidden_set = st.session_state.user_hidden.get(user_id, set())

    total = total_monthly_cost(subs_df)
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0">Общая сумма оплаты в месяц</h3>
        <h1 style="margin:0">{total} ₽</h1>
    </div>
    """, unsafe_allow_html=True)

    top = top_expensive(subs_df, 3)
    if top:
        st.markdown("#### Самые дорогие подписки:")
        for t in top:
            st.info(
                f"**{t['merchant_name']}**: {t['monthly_cost']} ₽/мес")

    st.subheader("Персональные рекомендации")
    st.caption(
        "На основе анализа ваших транзакций мы подготовили несколько наблюдений. Решение остаётся за вами.")

    problem_subs = subs_df[subs_df['status'].isin(
        ["Возможно не используется", "Цена выросла", "Пробный период", "Скоро списание"])]
    problem_subs = problem_subs[~problem_subs['merchant_name'].isin(
        hidden_set)]

    if not problem_subs.empty:
        total_savings = 0.0
        for _, row in problem_subs.iterrows():
            merchant = row['merchant_name']
            status = row['status']
            amount = row['amount']
            period = row['period_days']
            if period == 365:
                monthly_cost = amount / 12
            elif period == 7:
                monthly_cost = amount * (30/7)
            else:
                monthly_cost = amount

            if status == "Возможно не используется":
                last_date = row['last_payment_date'].date()
                days_ago = (date.today() - last_date).days
                reason = f"Вы не пользовались сервисом {merchant} более {days_ago} дней. Возможно, он вам больше не нужен."
                savings = monthly_cost
                action = "отключить"
            elif status == "Цена выросла":
                merchant_txs = transactions[transactions['merchant_name'] == merchant].sort_values(
                    'date')
                amounts = merchant_txs['amount'].values
                non_zero = [a for a in amounts if a > 0]
                if len(non_zero) >= 2:
                    old_price = non_zero[0]
                    new_price = non_zero[-1]
                    if old_price == new_price and len(non_zero) > 2:
                        old_price = non_zero[-2]
                    if old_price != new_price:
                        increase_pct = (new_price - old_price) / \
                            old_price * 100
                        reason = f"Стоимость {merchant} выросла с {old_price:.2f} ₽ до {new_price:.2f} ₽ (+{increase_pct:.0f}%). Вы продолжаете платить по новой цене."
                    else:
                        reason = f"Стоимость {merchant} выросла (текущая цена {amount} ₽). Рекомендуем проверить условия подписки."
                    savings = 0
                    action = "пересмотреть"
                else:
                    reason = f"Стоимость {merchant} выросла (текущая цена {amount} ₽)."
                    savings = 0
                    action = "проверить"
            elif status == "Пробный период":
                next_payment = row['next_payment_date'].date()
                days_left = (next_payment - date.today()).days
                reason = f"Пробный период {merchant} заканчивается через {days_left} дней. Затем начнётся списание {amount} ₽/мес."
                savings = monthly_cost
                action = "отключить до списания"
            elif status == "Скоро списание":
                next_payment = row['next_payment_date'].date()
                days_left = (next_payment - date.today()).days
                reason = f"Через {days_left} дня(ей) спишется {amount} ₽ за {merchant}. Напомним, что это регулярный платёж."
                savings = 0
                action = "проверить необходимость"
            else:
                continue

            with st.container():
                st.markdown(f"""
                <div style="background-color: #f8f9fa; border-radius: 16px; padding: 12px; margin-bottom: 12px;">
                    <strong>{reason}</strong>
                </div>
                """, unsafe_allow_html=True)
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    if savings > 0:
                        st.caption(
                            f"Потенциальная экономия: **{savings:.2f} ₽/мес**, если {action} подписку.")
                    else:
                        st.caption(
                            f"Рекомендуем {action} целесообразность этой подписки.")
                with col_b:
                    if status in ["Возможно не используется", "Пробный период"]:
                        if st.button(f"Смоделировать отключение", key=f"rec_sim_{user_id}_{merchant}"):
                            new_total = simulate_savings(subs_df, [merchant])
                            st.success(
                                f"Если отключить {merchant}, ежемесячные траты снизятся с {total} ₽ до {new_total} ₽ (экономия {total - new_total:.2f} ₽/мес).")
            total_savings += savings

        if total_savings > 0:
            st.info(
                f"**Общая потенциальная экономия в месяц: {total_savings:.2f} ₽**, если отключить все указанные подписки.")
    else:
        st.success(
            "Отлично! Все ваши подписки выглядят актуально. Нет явно лишних или проблемных.")

    filter_option = st.radio("Фильтр:", [
                             "Все", "Редко используемые", "Дорогие", "Скоро спишут"], horizontal=True)
    display_df = subs_df[~subs_df['merchant_name'].isin(hidden_set)]
    if filter_option == "Редко используемые":
        display_df = display_df[display_df['status']
                                == "Возможно не используется"]
    elif filter_option == "Дорогие":
        display_df = display_df.copy()
        monthly = []
        for _, row in display_df.iterrows():
            p = row['period_days']
            am = row['amount']
            if p == 365:
                mon = am / 12
            elif p == 7:
                mon = am * (30/7)
            else:
                mon = am
            monthly.append(mon)
        display_df['monthly_cost'] = monthly
        display_df = display_df.nlargest(3, 'monthly_cost')
    elif filter_option == "Скоро спишут":
        display_df = display_df[display_df['status'] == "Скоро списание"]

    st.subheader("Мои подписки")
    if display_df.empty:
        st.warning("Нет подписок по выбранному фильтру.")
    else:
        for _, row in display_df.iterrows():
            status = row['status']
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

            next_date = row['next_payment_date'].strftime('%d.%m.%Y')
            is_important = row['merchant_name'] in important_set

            cols = st.columns([4, 0.5, 0.5])
            with cols[0]:
                st.markdown(f"**{row['merchant_name']}**")
                st.caption(f"{row['amount']} ₽ • {next_date}")
                st.markdown(
                    f'<span class="{status_class}">{status}</span>', unsafe_allow_html=True)
            with cols[1]:
                if st.button("⭐" if is_important else "☆", key=f"imp_{user_id}_{row['merchant_name']}"):
                    if is_important:
                        st.session_state.user_important[user_id].discard(
                            row['merchant_name'])
                    else:
                        st.session_state.user_important[user_id].add(
                            row['merchant_name'])
                    st.rerun()
            with cols[2]:
                if st.button("❌", key=f"hide_{user_id}_{row['merchant_name']}"):
                    st.session_state.user_hidden[user_id].add(
                        row['merchant_name'])
                    st.rerun()
            st.divider()

    st.subheader("Тестирование уведомлений")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Скоро списание"):
            upcoming = subs_df[subs_df['status'] == "Скоро списание"]
            if not upcoming.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} ({r['amount']} ₽)" for _, r in upcoming.iterrows()])
                st.toast(f"⏰ Через 1-3 дня спишется: {msg}", icon="🔔")
            else:
                st.toast("Нет подписок с ближайшим списанием", icon="ℹ️")
        if st.button("Рост цены"):
            price_rise = subs_df[subs_df['status'] == "Цена выросла"]
            if not price_rise.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} (теперь {r['amount']} ₽)" for _, r in price_rise.iterrows()])
                st.toast(f"💰 Цена выросла: {msg}", icon="📈")
            else:
                st.toast("Нет подписок с ростом цены", icon="ℹ️")
    with col2:
        if st.button("Пробный период"):
            trial = subs_df[subs_df['status'] == "Пробный период"]
            if not trial.empty:
                msg = ", ".join(
                    [f"{r['merchant_name']} (след. списание {r['amount']} ₽)" for _, r in trial.iterrows()])
                st.toast(f"⚠️ Пробный период заканчивается: {msg}", icon="⏳")
            else:
                st.toast("Нет подписок в пробном периоде", icon="ℹ️")
        if st.button("Лишняя подписка"):
            unused_names, amt = potential_savings(subs_df, important_set)
            if unused_names:
                st.toast(
                    f"💡 Обнаружены редко используемые подписки: {', '.join(unused_names)}. Экономия ~{amt} ₽/мес", icon="💡")
            else:
                st.toast("Лишних подписок не найдено", icon="✅")

    with st.expander("Все транзакции клиента"):
        st.dataframe(transactions, use_container_width=True, height=300)
