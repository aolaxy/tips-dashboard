import plotly.express as px


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
        bargap=0.7,  # Больше пространства между группами столбцов
        bargroupgap=0.3,  # Пространство между столбцами внутри группы
        margin=dict(l=50, r=50, t=60, b=50),
        autosize=True,
        width=None  # Автоматическая ширина
    )

    # Настройка ширины отдельных столбцов
    fig.update_traces(width=0.3)  # Значительно уменьшаем ширину столбцов

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
                     trendline='ols',
                     labels={'total_bill': 'Total Bill ($)', 'tip': 'Tip Amount ($)'})

    fig.update_layout(legend_title_text='Time of Day')
    return fig