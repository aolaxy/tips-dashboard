import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, no_update
from dash import dash_table
from graphfunc import print_tip_distribution, print_total_bill_distribution, print_time_boxplot, print_day_pie_chart, \
    print_tip_vs_bill_scatter

df = pd.read_csv('tips.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Добавляем опцию для таблицы в выбор типа отображения
graph_options = [
    {'label': html.Span([html.Img(src="/assets/images/person.svg", height=20), " Tips by Gender"]), 'value': 'tips'},
    {'label': html.Span([html.Img(src="/assets/images/bar-chart-line-fill.svg", height=20), " Total bill"]),
     'value': 'total_bill'},
    {'label': html.Span([html.Img(src="/assets/images/archive-fill.svg", height=20), "Time Boxplot"]),
     'value': 'time_boxplot'},
    {'label': html.Span([html.Img(src="/assets/images/calendar-day.svg", height=20), "Day Distribution"]),
     'value': 'day_pie'},
    {'label': html.Span([html.Img(src="/assets/images/graph-up.svg", height=20), "Tips vs Bill Scatter"]),
     'value': 'bill_scatter'},
    {'label': html.Span([html.Img(src="/assets/images/table-cells-solid-full.svg", height=20), "Data Table"]),
     'value': 'data_table'},
]

app.layout = dbc.Container([
    # Header с фоновым изображением
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("Tips Analysis Dashboard",
                            className="text-white display-4 fw-bold",
                            style={'textShadow': '2px 2px 4px rgba(0,0,0,0.5)'}),
                    html.P("Interactive analysis of restaurant tipping patterns",
                           className="text-white lead",
                           style={'textShadow': '1px 1px 2px rgba(0,0,0,0.5)'})
                ], className="text-center")
            ], style={
            'backgroundImage': 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("/assets/images/tips.png")',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'height': '250px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'borderRadius': '10px',
            'marginBottom': '20px'
        })
    ], width=12)
], className="mb-4"),

    # Кнопка сброса фильтров
    dbc.Row([
        dbc.Col([
            dbc.Button('Reset All Filters',
                       id='reset-button',
                       n_clicks=0,
                       color="danger",
                       className="mb-3")
        ], width=12)
    ]),

    # Карточка с выбором типа отображения
    dbc.Card([
        dbc.CardHeader(
            html.H5("📊 Display Type Selection", className="mb-0"),
            className="bg-light"
        ),
        dbc.CardBody([
            dbc.RadioItems(
                id='graph-type',
                options=graph_options,
                value='tips',
                inline=True,
                className="gap-2"
            )
        ])
    ], className="mb-4"),

    # Карточка с фильтрами
    dbc.Card([
        dbc.CardHeader("Filters"),
        dbc.CardBody([
            dbc.Row([
                # День недели
                dbc.Col([
                    dbc.Label("Day of Week:"),
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

                # Время дня
                dbc.Col([
                    dbc.Label("Time of Day:"),
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

                # Пол
                dbc.Col([
                    dbc.Label("Gender:"),
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

                # Курящие/некурящие
                dbc.Col([
                    dbc.Label("Smoker Status:"),
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

            # Слайдер суммы счета
            dbc.Row([
                dbc.Col([
                    dbc.Label("Bill Amount Range:"),
                    dcc.RangeSlider(
                        id='bill-range',
                        min=df['total_bill'].min(),
                        max=df['total_bill'].max(),
                        step=5,
                        marks={i: f'${i}' for i in range(0, 55, 5)},
                        value=[df['total_bill'].min(), df['total_bill'].max()],
                        className="mt-3"
                    )
                ], width=12)
            ]),

            # Фильтр колонок для таблицы
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id='column-filter-container',
                        children=[
                            dbc.Label("Select Columns to Display:"),
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
            ], className="mt-3")
        ])
    ], className="mb-4"),

    # Контейнер для графика или таблицы
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # График
                    html.Div(id='graph-container', children=[
                        dcc.Graph(id='graph-output')
                    ]),
                    # Таблица
                    html.Div(id='table-container', children=[
                        dash_table.DataTable(
                            id='data-table',
                            columns=[],
                            data=[],
                            page_size=10,
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'
                            },
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                        )
                    ], style={'display': 'none'})
                ])
            ])
        ], width=12)
    ]),

    # Footer с логотипом OTUS
    dbc.Row([
        dbc.Col([
            html.Hr(className="my-4"),
            html.Div([
                html.Div([
                    html.Img(
                        src="/assets/images/otus_logo.png",
                        height="40px",
                        className="me-3"
                    ),
                    html.Span("© 2025 OTUS - Educational Platform",
                              className="text-muted",
                              style={'verticalAlign': 'middle'})
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'padding': '20px 0'
                })
            ], className="text-center")
        ], width=12)
    ])

], fluid=True, style={'minHeight': '100vh', 'position': 'relative', 'paddingBottom': '80px'})


# Callback для сброса всех фильтров
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


# Callback для переключения между графиком и таблицей
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


# Callback для обновления графика
@app.callback(
    Output('graph-output', 'figure'),
    Input('day-dropdown', 'value'),
    Input('graph-type', 'value'),
    Input('gender-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('smoker-filter', 'value'),
    Input('bill-range', 'value'),
)
def update_graph(selected_day, graph_type, selected_gender,
                 selected_time, smoker_status, bill_range):
    if graph_type == 'data_table':
        return no_update

    filtered_df = apply_filters(df, selected_day, selected_gender, selected_time, smoker_status, bill_range)

    if graph_type == 'tips':
        return print_tip_distribution(filtered_df,selected_day)
    elif graph_type == 'total_bill':
        return print_total_bill_distribution(filtered_df,selected_day)
    elif graph_type == 'time_boxplot':
        return print_time_boxplot(filtered_df)
    elif graph_type == 'day_pie':
        return print_day_pie_chart(filtered_df)
    elif graph_type == 'bill_scatter':
        return print_tip_vs_bill_scatter(filtered_df)


# Callback для обновления таблиции
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

    # Фильтруем колонки
    filtered_df = filtered_df[selected_columns]

    # Создаем колонки для таблицы
    columns = [{"name": col, "id": col} for col in filtered_df.columns]

    # Конвертируем данные
    data = filtered_df.to_dict('records')

    return columns, data


# Вспомогательная функция для применения фильтров
def apply_filters(dataframe, day, gender, time, smoker, bill_range):
    filtered_df = dataframe.copy()

    if day != 'All':
        filtered_df = filtered_df[filtered_df['day'] == day]

    if gender != 'All':
        filtered_df = filtered_df[filtered_df['sex'] == gender]

    if time != 'All':
        filtered_df = filtered_df[filtered_df['time'] == time]

    if smoker != 'All':
        filtered_df = filtered_df[filtered_df['smoker'] == smoker]

    filtered_df = filtered_df[
        (filtered_df['total_bill'] >= bill_range[0]) &
        (filtered_df['total_bill'] <= bill_range[1])
        ]

    return filtered_df


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)