import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def create_plot(start_year, end_year):
    # 读取数据
    file_path = './data/carbon_dioxide_data.csv'
    data = pd.read_csv(file_path)

    # 根据年份范围筛选数据
    filtered_data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]


    # 创建 Plotly 图表
    trace = go.Scatter(
        x=filtered_data['year'],
        y=filtered_data['de-seasonalized'],
        mode='lines+markers',
        name='',
        hovertemplate='Year: %{x}<br>Monthly average(de-seasonalized): %{y} parts per million<br>',
    )

    layout = go.Layout(
        title=f'Carbon Dioxide Emission ({start_year} - {end_year})',
        xaxis=dict(title='Year'),
        yaxis=dict(title='CO₂ (parts per million)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        template='plotly_white'
    )

    figure = go.Figure(data=[trace], layout=layout)
    return figure


@app.route('/')
def home():
    return redirect(url_for('carbon_dioxide_visualize'))

@app.route('/carbon_dioxide_visualize', methods=['GET', 'POST'])
def carbon_dioxide_visualize():
    if request.method == 'POST':
        # 获取表单输入的年份
        start_year = request.form.get('start_year', type=int)
        end_year = request.form.get('end_year', type=int)

        # 额外的年份范围检查
        if start_year < 1958 or end_year > 2024:
            return "<h1>Please enter a valid year between 1958 and 2024。</h1>"

        if start_year and end_year:
            # 生成图表
            figure = create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('carbon_dioxide_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('carbon_dioxide_visualize.html')


if __name__ == '__main__':
    app.run(debug=True)
