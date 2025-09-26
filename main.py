import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, no_update
from dash import dash_table
from graphfunc import print_tip_distribution, print_total_bill_distribution, print_time_boxplot, print_day_pie_chart, print_tip_vs_bill_scatter
from graphfunc import calculate_statistics, create_interactive_stats

# Загрузка данных
df = pd.read_csv('tips.csv')
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Опции для выбора типа графика
graph_options = [
    {'label': "💰 Tips by Gender", 'value': 'tips'},
    {'label': "📊 Total Bill", 'value': 'total_bill'},
    {'label': "⏰ Time Boxplot", 'value': 'time_boxplot'},
    {'label': "📅 Day Distribution", 'value': 'day_pie'},
    {'label': "📈 Tips vs Bill", 'value': 'bill_scatter'},
    {'label': "📋 Data Table", 'value': 'data_table'},
]

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Tips Analysis Dashboard", className="header-title"),
                html.P("Interactive analysis of restaurant tipping patterns",
                       className="header-subtitle"),
                html.Div([
                    html.Span("📊 5 Visualizations", className="badge-custom"),
                    html.Span("⚡ Real-time", className="badge-custom"),
                    html.Span("🎯 Smart Filters", className="badge-custom")
                ], className="text-center mt-3")
            ], className="dashboard-header text-center p-5")
        ], width=12)
    ], className="mb-4"),

    # Статистика
    html.Div(id='stats-container', children=create_interactive_stats(df), className="fade-in"),

    # Кнопка сброса
    dbc.Row([
        dbc.Col([
            dbc.Button("🔄 Reset All Filters",
                      id='reset-button',
                      n_clicks=0,
                      color="danger",
                      className="btn-custom-primary mb-4")
        ], width=12)
    ]),

    # Выбор типа отображения
    dbc.Card([
        dbc.CardHeader(html.H4("📈 Visualization Type", className="card-title"),
                      className="card-header-custom"),
        dbc.CardBody([
            dbc.RadioItems(
                id='graph-type',
                options=graph_options,
                value='tips',
                inline=True,
                className="radio-group-custom"
            )
        ])
    ], className="custom-card mb-4"),

    # Фильтры
    dbc.Card([
        dbc.CardHeader(html.H4("🔧 Data Filters", className="card-title"),
                      className="card-header-custom"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("📅 Day of Week", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='day-dropdown',
                        options=[
                            {'label': 'All Days', 'value': 'All'},
                            {'label': 'Thursday', 'value': 'Thur'},
                            {'label': 'Friday', 'value': 'Fri'},
                            {'label': 'Saturday', 'value': 'Sat'},
                            {'label': 'Sunday', 'value': 'Sun'}
                        ],
                        value='All',
                        clearable=False
                    )
                ], md=3, className="mb-3"),

                dbc.Col([
                    dbc.Label("⏰ Time of Day", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='time-dropdown',
                        options=[
                            {'label': 'All Times', 'value': 'All'},
                            {'label': 'Lunch', 'value': 'Lunch'},
                            {'label': 'Dinner', 'value': 'Dinner'}
                        ],
                        value='All',
                        clearable=False
                    )
                ], md=3, className="mb-3"),

                dbc.Col([
                    dbc.Label("👥 Gender", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='gender-dropdown',
                        options=[
                            {'label': 'All Genders', 'value': 'All'},
                            {'label': 'Male', 'value': 'Male'},
                            {'label': 'Female', 'value': 'Female'}
                        ],
                        value='All',
                        clearable=False
                    )
                ], md=3, className="mb-3"),

                dbc.Col([
                    dbc.Label("🚬 Smoker Status", className="fw-bold mb-2"),
                    dbc.RadioItems(
                        id='smoker-filter',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'Smokers', 'value': 'Yes'},
                            {'label': 'Non-smokers', 'value': 'No'}
                        ],
                        value='All',
                        inline=True
                    )
                ], md=3, className="mb-3")
            ]),

            # Слайдер счета
            dbc.Row([
                dbc.Col([
                    dbc.Label("💰 Bill Amount Range", className="fw-bold mb-3"),
                    dcc.RangeSlider(
                        id='bill-range',
                        min=df['total_bill'].min(),
                        max=df['total_bill'].max(),
                        step=5,
                        marks={i: f'${i}' for i in range(0, 55, 10)},
                        value=[df['total_bill'].min(), df['total_bill'].max()],
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], width=12)
            ], className="mt-4"),

            # Фильтр колонок таблицы
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id='column-filter-container',
                        children=[
                            dbc.Label("📋 Table Columns", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id='column-selector',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value=df.columns.tolist(),
                                multi=True,
                                clearable=False
                            )
                        ],
                        style={'display': 'none'}
                    )
                ], width=12)
            ], className="mt-4")
        ])
    ], className="custom-card mb-4"),

    # График/Таблица
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='graph-container', children=[
                        dcc.Graph(id='graph-output')
                    ]),
                    html.Div(id='table-container', children=[
                        dash_table.DataTable(
                            id='data-table',
                            columns=[],
                            data=[],
                            page_size=10,
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '12px'},
                            style_header={'backgroundColor': '#667eea', 'color': 'white'},
                            filter_action="native",
                            sort_action="native",
                            page_action="native"
                        )
                    ], style={'display': 'none'})
                ])
            ], className="custom-card")
        ], width=12)
    ]),

    # Футер
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src="/assets/images/otus_logo.png", height=40, className="me-3"),
                html.Span("© 2025 OTUS - Data Science Platform",
                         className="text-muted")
            ], className="footer-custom text-center p-4")
        ], width=12)
    ], className="mt-5")

], fluid=True)

# Callback функции (остаются без изменений)
@app.callback(
    [Output('day-dropdown', 'value'),
     Output('gender-dropdown', 'value'),
     Output('time-dropdown', 'value'),
     Output('smoker-filter', 'value'),
     Output('graph-type', 'value'),
     Output('column-selector', 'value'),
     Output('bill-range','value')],
    Input('reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    if n_clicks > 0:
        return 'All', 'All', 'All', 'All', 'tips', df.columns.tolist(), [df['total_bill'].min(), df['total_bill'].max()]
    return no_update

@app.callback(
    [Output('graph-container', 'style'),
     Output('table-container', 'style'),
     Output('column-filter-container', 'style')],
    Input('graph-type', 'value')
)
def toggle_display_type(graph_type):
    if graph_type == 'data_table':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

@app.callback(
    Output('graph-output', 'figure'),
    Input('day-dropdown', 'value'),
    Input('graph-type', 'value'),
    Input('gender-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('smoker-filter', 'value'),
    Input('bill-range', 'value'),
)
def update_graph(selected_day, graph_type, selected_gender, selected_time, smoker_status, bill_range):
    if graph_type == 'data_table':
        return no_update

    filtered_df = apply_filters(df, selected_day, selected_gender, selected_time, smoker_status, bill_range)

    if graph_type == 'tips':
        return print_tip_distribution(filtered_df, selected_day)
    elif graph_type == 'total_bill':
        return print_total_bill_distribution(filtered_df, selected_day)
    elif graph_type == 'time_boxplot':
        return print_time_boxplot(filtered_df)
    elif graph_type == 'day_pie':
        return print_day_pie_chart(filtered_df)
    elif graph_type == 'bill_scatter':
        return print_tip_vs_bill_scatter(filtered_df)

@app.callback(
    [Output('data-table', 'columns'),
     Output('data-table', 'data')],
    [Input('day-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('time-dropdown', 'value'),
     Input('smoker-filter', 'value'),
     Input('bill-range', 'value'),
     Input('column-selector', 'value')]
)
def update_table(selected_day, selected_gender, selected_time, smoker_status, bill_range, selected_columns):
    filtered_df = apply_filters(df, selected_day, selected_gender, selected_time, smoker_status, bill_range)
    filtered_df = filtered_df[selected_columns]
    columns = [{"name": col, "id": col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    return columns, data

@app.callback(
    Output('stats-container', 'children'),
    Input('day-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('smoker-filter', 'value'),
    Input('bill-range', 'value')
)
def update_stats(selected_day, selected_gender, selected_time, smoker_status, bill_range):
    filtered_df = apply_filters(df, selected_day, selected_gender, selected_time, smoker_status, bill_range)
    return create_interactive_stats(filtered_df)

def apply_filters(dataframe, day, gender, time, smoker, bill_range):
    filtered_df = dataframe.copy()
    if day != 'All': filtered_df = filtered_df[filtered_df['day'] == day]
    if gender != 'All': filtered_df = filtered_df[filtered_df['sex'] == gender]
    if time != 'All': filtered_df = filtered_df[filtered_df['time'] == time]
    if smoker != 'All': filtered_df = filtered_df[filtered_df['smoker'] == smoker]
    filtered_df = filtered_df[(filtered_df['total_bill'] >= bill_range[0]) & (filtered_df['total_bill'] <= bill_range[1])]
    return filtered_df

if __name__ == '__main__':
    app.run(debug=True)