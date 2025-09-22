import plotly.express as px
import pandas as pd
from dash import html
import numpy as np
import dash_bootstrap_components as dbc
def print_tip_distribution(dataFrame, day_filter='All'):
    """
    Создает график распределения чаевых по полу с возможностью фильтрации по дню недели

    """
    # Фильтрация данных по дню недели
    if day_filter != 'All':
       dataFrame = dataFrame[dataFrame['day'] == day_filter]

    # Группировка и расчет средних чаевых
    filtered_data = dataFrame.groupby(['sex']).agg({'tip': 'mean'}).reset_index()
    filtered_data['tip'] = filtered_data['tip'].round(2)
    filtered_data.sort_values(by='tip', ascending=False, inplace=True)

    # Определение заголовка
    title = (f"Average Tips by Gender ({day_filter})" if day_filter != 'All'
             else "Average Tips by Gender (All Days)")

    # Создание графика
    fig = px.bar(filtered_data,
                 x="sex",
                 y="tip",
                 title=title,
                 color="sex",
                 labels={'sex': 'Gender', 'tip': 'Average Tip ($)'})

    # Настройка макета для компактного отображения
    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Average Tip Amount ($)",
        showlegend=False,
        bargap=0.7,
        bargroupgap=0.3,
        margin=dict(l=50, r=50, t=60, b=50),
        autosize=True,
        width=None
    )


    fig.update_traces(width=0.3)

    return fig


def print_total_bill_distribution(dataFrame, day_filter='All'):
    """
    Создает гистограмму распределения сумм счетов (total_bill)
    """
    # Фильтрация данных по дню недели
    if day_filter != 'All':
      dataFrame = dataFrame[dataFrame['day'] == day_filter]

    # Определение заголовка
    title = (f"Total Bill Distribution ({day_filter})" if day_filter != 'All'
             else "Total Bill Distribution (All Days)")

    # Создание гистограммы
    fig = px.histogram(dataFrame,
                       x="total_bill",
                       title=title,
                       nbins=20,
                       color_discrete_sequence=['indianred'],
                       labels={'total_bill': 'Total Bill Amount ($)'})

    # Настройка макета
    fig.update_layout(
        xaxis_title="Total Bill Amount ($)",
        yaxis_title="Count",
        showlegend=False
    )

    return fig


def print_time_boxplot(dataFrame, gender_filter='All'):
    """
    Создает Box plot распределения чаевых по времени дня с фильтром по полу

    """
    # Фильтрация по полу
    if gender_filter != 'All':
        dataFrame = dataFrame[dataFrame['sex'] == gender_filter]

    title = f"Tip Distribution by Time ({gender_filter})" if gender_filter != 'All' \
        else "Tip Distribution by Time (All Genders)"

    fig = px.box(dataFrame,
                 x='time',
                 y='tip',
                 color='sex' if gender_filter == 'All' else None,
                 title=title,
                 labels={'time': 'Time of Day', 'tip': 'Tip Amount ($)'})

    fig.update_layout(
        legend_title_text='Gender',
        xaxis_title="Time of Day",
        yaxis_title="Tip Amount ($)"
    )

    if gender_filter != 'All':
        fig.update_traces(fillcolor='lightblue', line_color='darkblue')

    return fig


# Круговая диаграмма распределения по дням недели
def print_day_pie_chart(dataFrame):
    day_counts = dataFrame['day'].value_counts().reset_index()
    day_counts.columns = ['day', 'count']

    fig = px.pie(day_counts,
                 values='count',
                 names='day',
                 title='Distribution by Day of Week',
                 color='day',
                 category_orders={'day': ['Thur', 'Fri', 'Sat', 'Sun']})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Scatter plot зависимости чаевых от суммы счета
def print_tip_vs_bill_scatter(dataFrame):
    fig = px.scatter(dataFrame,
                     x='total_bill',
                     y='tip',
                     color='time',
                     title='Tip Amount vs Total Bill',
                     trendline='ewm', trendline_options=dict(span=10),
                     labels={'total_bill': 'Total Bill ($)', 'tip': 'Tip Amount ($)'})

    fig.update_layout(legend_title_text='Time of Day')
    return fig


def calculate_statistics(dataFrame):
    """
    Рассчитывает основные статистические показатели данных о чаевых
    """
    stats = {}

    # Основные показатели
    stats['total_records'] = len(dataFrame)
    stats['avg_bill'] = dataFrame['total_bill'].mean()
    stats['avg_tip'] = dataFrame['tip'].mean()
    stats['avg_tip_percentage'] = (dataFrame['tip'] / dataFrame['total_bill'] * 100).mean()
    stats['avg_size'] = dataFrame['size'].mean()

    # По полу
    gender_stats = dataFrame.groupby('sex').agg({
        'tip': 'mean',
        'total_bill': 'mean',
        'size': 'mean'
    }).round(2)
    stats['gender_stats'] = gender_stats

    # По дням недели
    day_stats = dataFrame.groupby('day').agg({
        'tip': 'mean',
        'total_bill': 'mean',
        'size': 'count'
    }).round(2)
    stats['day_stats'] = day_stats

    # По времени дня
    time_stats = dataFrame.groupby('time').agg({
        'tip': 'mean',
        'total_bill': 'mean'
    }).round(2)
    stats['time_stats'] = time_stats

    # По курящим/некурящим
    smoker_stats = dataFrame.groupby('smoker').agg({
        'tip': 'mean',
        'total_bill': 'mean'
    }).round(2)
    stats['smoker_stats'] = smoker_stats

    # Корреляция
    stats['correlation'] = dataFrame['total_bill'].corr(dataFrame['tip'])

    # Экстремальные значения
    stats['max_tip'] = dataFrame['tip'].max()
    stats['min_tip'] = dataFrame['tip'].min()
    stats['max_bill'] = dataFrame['total_bill'].max()
    stats['min_bill'] = dataFrame['total_bill'].min()

    return stats


def create_interactive_stats(dataFrame):
    """
    Создает интерактивные статистические карточки
    """
    stats = calculate_statistics(dataFrame)

    return html.Div([
        dbc.Row([
            # Основные показатели
            dbc.Col(dbc.Card([
                dbc.CardHeader("📊 Основные показатели"),
                dbc.CardBody([
                    html.H4(f"{stats['total_records']}", className="text-primary"),
                    html.P("Всего записей", className="text-muted")
                ])
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("💰 Средний счет"),
                dbc.CardBody([
                    html.H4(f"${stats['avg_bill']:.2f}", className="text-success"),
                    html.P("Средняя сумма", className="text-muted")
                ])
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("💵 Средние чаевые"),
                dbc.CardBody([
                    html.H4(f"${stats['avg_tip']:.2f}", className="text-info"),
                    html.P(f"{stats['avg_tip_percentage']:.1f}% от счета", className="text-muted")
                ])
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("👥 Размер компании"),
                dbc.CardBody([
                    html.H4(f"{stats['avg_size']:.1f}", className="text-warning"),
                    html.P("Среднее количество", className="text-muted")
                ])
            ]), md=3),
        ], className="mb-4"),

        # Детальная статистика
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("👨‍👩 По полу"),
                dbc.CardBody([
                    *[html.P(f"{row.Index}: ${row.tip:.2f} чаевых")
                      for row in stats['gender_stats'].itertuples()]
                ])
            ]), md=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("📅 По дням недели"),
                dbc.CardBody([
                    *[html.P(f"{row.Index}: ${row.tip:.2f} чаевых")
                      for row in stats['day_stats'].itertuples()]
                ])
            ]), md=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("⏰ По времени дня"),
                dbc.CardBody([
                    *[html.P(f"{row.Index}: ${row.tip:.2f} чаевых")
                      for row in stats['time_stats'].itertuples()]
                ])
            ]), md=4),
        ])
    ])