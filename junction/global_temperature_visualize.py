import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def create_plot(start_year, end_year):

    # 读取数据
    file_path = './data/global_temperature_data.csv'
    data = pd.read_csv(file_path)

    # 根据年份范围筛选数据
    filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

    # 创建图表
    trace_1 = go.Scatter(
        x=filtered_data['Year'],
        y=filtered_data['No_Smoothing'],
        mode='lines+markers',
        name='Annual Mean',
        hovertemplate='Year: %{x}<br>Temperature Anomaly: %{y}°C<br>',
    )

    trace_2 = go.Scatter(
        x=filtered_data['Year'],
        y=filtered_data['Lowess'],
        mode='lines',
        name='Lowess Smoothing',
        hovertemplate='Year: %{x}<br>Temperature Anomaly: %{y}°C<br>',
    )

    layout = go.Layout(
        title=f'Global Temperature Anomalies ({start_year} - {end_year})',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Temperature Anomaly (°C)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        template='plotly_white'
    )

    # 创建图表对象
    figure = go.Figure(data=[trace_1, trace_2], layout=layout)
    return figure


@app.route('/')
def home():
    return redirect(url_for('global_temperature_visualize'))


@app.route('/global_temperature_visualize', methods=['GET', 'POST'])
def global_temperature_visualize():
    if request.method == 'POST':
        # 获取用户输入的年份范围
        start_year = request.form.get('start_year', type=int)
        end_year = request.form.get('end_year', type=int)

        # 校验年份范围
        if start_year < 1880 or end_year > 2023:
            return "<h1>Please enter a valid year between 1880 and 2023.</h1>"

        if start_year and end_year:
            # 生成图表
            figure = create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('global_temperature_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求时显示表单页面
    return render_template('global_temperature_visualize.html')


if __name__ == '__main__':
    app.run(debug=True)
