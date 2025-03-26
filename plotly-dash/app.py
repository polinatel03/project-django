import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests

# Создаём Dash-приложение
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Заявки"),
    dcc.Dropdown(id='workorder-dropdown', placeholder="Выберите заявку"),
    html.Div(id='approval-data')
])

# Функция для получения данных о заявках (кэшируется)
def fetch_workorders():
    try:
        response = requests.get('http://localhost:8000/workorder/')
        response.raise_for_status()  # Проверяем статус ответа
        workorders = response.json()
        return [{'value': wo['workorderid'], 'label': wo['description']} for wo in workorders]
    except requests.RequestException as e:
        print(f"Ошибка при получении данных о заявках: {e}")
        return []

# Callback для загрузки списка заявок
@app.callback(
    Output('workorder-dropdown', 'options'),
    [Input('workorder-dropdown', 'id')]
)
def update_workorder_dropdown(_):
    return fetch_workorders()

# Функция для получения данных о согласованиях и пользователях (кэшируется)
def fetch_users_and_approvals(workorderid):
    try:
        # Получаем данные о пользователях
        response = requests.get('http://localhost:8000/user/')
        response.raise_for_status()
        user_list = response.json()

        if not user_list:
            return {}, []
        
        # Создаем словарь для поиска и дальнейшего вывода имён пользователей
        user_dict = {user['userid']: user['displayname'] for user in user_list}

        # Получаем данные о согласованиях
        response = requests.get(f'http://localhost:8000/approval/?workorderid={workorderid}')
        response.raise_for_status()
        approval_list = response.json()

        if not approval_list:
            return user_list, []
        
        return user_dict, approval_list
    
    except requests.RequestException as e:
        print(f"Ошибка при получении данных о согласовании/пользователях: {e}")
        return {}, [] 

# Callback для отображения данных о согласовании заявки
@app.callback(
    Output('approval-data', 'children'),
    [Input('workorder-dropdown', 'value')]
)
def display_approval(workorderid):
    if not workorderid:
        return None # Если заявка не выбрана, никакие данные выводиться не будут

    user_dict, approval_list = fetch_users_and_approvals(workorderid)

    if not user_dict:
        return "В системе нет данных о пользователях."

    if not approval_list:
        return "В системе нет данных о согласовании."

    # Формируем список согласований по выбранной заявке
    approval_items = [
        html.Li(f"Согласующий: {user_dict[approval['userid']]}, статус согласования: {approval['status']}")
        for approval in approval_list if approval['workorderid'] == workorderid
    ]

    # Выводим непронумерованный список данных о согласовании заявки либо сообщение о его отсутствии
    return html.Ul(approval_items) if approval_items else "Нет данных о согласовании для данной заявки."

if __name__ == '__main__':
    app.run_server(debug=True)