import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

# Server setup for Flask and Dash
server = Flask(__name__)
server.secret_key = 'secret'
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,  title='Expense Tracker App')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(server)

# In-memory user data with hashed password
users = {"admin": {"password": generate_password_hash("1234")}}

# User class for login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

# User-specific transaction data
user_transactions = {"admin": []}

# Layout for login page
login_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H3("Login", className="card-title text-center mb-4"),
                    dbc.Row([
                        dbc.Label("Username", html_for="username", width=12),
                        dbc.Col(dbc.Input(id="username", placeholder="Enter username", type="text", className="mb-3"), width=12)
                    ]),
                    dbc.Row([
                        dbc.Label("Password", html_for="password", width=12),
                        dbc.Col(dbc.Input(id="password", placeholder="Enter password", type="password", className="mb-3"), width=12)
                    ]),
                    dbc.Button("Login", id="login-button", color="primary", className="btn-block my-2", n_clicks=0),
                    html.Div(id="login-output", className="text-danger text-center mt-3")
                ])
            ], className="shadow p-4 bg-light"),
            width=25,
        ),
        justify="center", className="vh-100 d-flex align-items-center"
    )
], fluid=True)

# Layout for the main app after login
app_layout = dbc.Container([
    html.H2("Expense Tracker", className="text-center my-4"),
    html.Div(id="balance-div", className="text-center"),

    dbc.Row([
        dbc.Col([
            html.H4("Income"),
            html.P(id="income-display", className="money plus")
        ]),
        dbc.Col([
            html.H4("Expense"),
            html.P(id="expense-display", className="money minus")
        ])
    ], className="inc-exp-container my-4"),

    # Bar chart for income and expense comparison
    html.H3("Income vs Expense Comparison"),
    dcc.Graph(id="income-expense-chart"),

    html.H3("History"),
    dash_table.DataTable(
        id='transaction-table',
        columns=[
            {"name": "Text", "id": "text"},
            {"name": "Category", "id": "category"},
            {"name": "Amount", "id": "amount", "type": "numeric"},
            {"name": "Date", "id": "date", "type": "datetime"}
        ],
        data=[],
        row_deletable=True,
        filter_action="native",  # Enable filtering
        sort_action="native",    # Enable sorting
        style_cell={'textAlign': 'center'},
        style_table={'margin-bottom': '20px'},
    ),

    dbc.Row([
        dbc.Col([
            html.Button("Download History", id="download-button", className="btn btn-primary my-2"),
            dcc.Download(id="download-csv")
        ])
    ]),

    html.H3("Add new transaction"),
    dbc.Form([
        dbc.Row([
            dbc.Label("Text", html_for="transaction-text", width=12),
            dbc.Col(dbc.Input(id="transaction-text", type="text", placeholder="Enter text..."), width=12)
        ]),
        dbc.Row([
            dbc.Label("Category", html_for="category-dropdown", width=12),
            dbc.Col(
                dcc.Dropdown(
                    id="category-dropdown",
                    options=[
                        {'label': 'Groceries', 'value': 'Groceries'},
                        {'label': 'Rent', 'value': 'Rent'},
                        {'label': 'Salary', 'value': 'Salary'},
                        {'label': 'Misc', 'value': 'Misc'},
                        {'label': 'Dress', 'value': 'Dress'},
                        {'label': 'Others', 'value': 'Others'},
                    ],
                    placeholder="Select a category"
                ), width=12
            )
        ]),
        dbc.Row([
            dbc.Label("Amount (negative - expense, positive - income)", html_for="transaction-amount", width=12),
            dbc.Col(dbc.Input(id="transaction-amount", type="number", placeholder="Enter amount..."), width=12)
        ]),
        dbc.Row([
            dbc.Label("Date", html_for="transaction-date", width=12),
            dbc.Col(dcc.DatePickerSingle(id='transaction-date', date=date.today()), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Add transaction", id="add-transaction", className="btn btn-primary my-2"), width=12)
        ])
    ]),

    dbc.Button("Logout", id="logout-button", color="danger", className="mt-4")
])

# Switch between layouts based on login status
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if current_user.is_authenticated:
        return app_layout
    else:
        return login_layout

# Authentication callback
@app.callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value")
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        if username in users and check_password_hash(users[username]["password"], password):
            user = User(username)
            login_user(user)
            return dcc.Location(id='url', pathname="/", refresh=True)
        else:
            return "Invalid username or password."

# Add transaction callback
@app.callback(
    Output('transaction-table', 'data'),
    Output('income-display', 'children'),
    Output('expense-display', 'children'),
    Output('income-expense-chart', 'figure'),
    Input('add-transaction', 'n_clicks'),
    State('transaction-text', 'value'),
    State('category-dropdown', 'value'),
    State('transaction-amount', 'value'),
    State('transaction-date', 'date'),
    prevent_initial_call=True
)
def add_transaction(n_clicks, text, category, amount, date):
    if text and amount and category and date:
        user_transactions[current_user.id].append({"text": text, "category": category, "amount": amount, "date": date})

        # Calculate income and expense
        income = sum([t['amount'] for t in user_transactions[current_user.id] if t['amount'] > 0])
        expense = sum([t['amount'] for t in user_transactions[current_user.id] if t['amount'] < 0])

        # Create bar chart
        fig = go.Figure([go.Bar(x=['Income', 'Expense'], y=[income, abs(expense)], marker_color=['green', 'red'])])

        return user_transactions[current_user.id], f"${income:.2f}", f"${abs(expense):.2f}", fig
    return dash.no_update

# Download transactions callback
@app.callback(
    Output("download-csv", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    if n_clicks:
        df = pd.DataFrame(user_transactions[current_user.id])
        return dcc.send_data_frame(df.to_csv, "transactions.csv")

# Logout callback
@app.callback(
    Output("url", "pathname"),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    if n_clicks:
        logout_user()
        return "/login"

# Define initial layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id="page-content")
])

if __name__ == '__main__':
    app.run_server(debug=True)
