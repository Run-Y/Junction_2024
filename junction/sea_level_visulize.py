import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def create_plot(start_year, end_year):
    # 读取数据
    file_path = './data/gmsl_data.csv'
    data = pd.read_csv(file_path)

    # 根据年份范围筛选数据
    filtered_data = data[(data['year_fraction'] >= start_year) & (data['year_fraction'] <= end_year)]

    # 对 GMSL_GIA_applied 列的值加上 37.9
    filtered_data['GMSL_GIA_applied'] = filtered_data['GMSL_GIA_applied'] + 37.9

    # 创建 Plotly 图表
    trace = go.Scatter(
        x=filtered_data['year_fraction'],
        y=filtered_data['GMSL_GIA_applied'],  # 使用加上 37.9 后的值
        mode='lines+markers',
        name='GMSL (GIA applied)',
        hovertemplate='Year: %{x}<br>GMSL: %{y} mm<br>',
    )

    layout = go.Layout(
        title=f'Global Mean Sea Level Variations ({start_year} - {end_year})',
        xaxis=dict(title='Year (Fraction)'),
        yaxis=dict(title='Global Mean Sea Level (mm)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        template='plotly_white'
    )

    figure = go.Figure(data=[trace], layout=layout)
    return figure


@app.route('/')
def home():
    return redirect(url_for('sea_level_visualize'))

@app.route('/sea_level_visualize', methods=['GET', 'POST'])
def sea_level_visualize():
    if request.method == 'POST':
        # 获取表单输入的年份
        start_year = request.form.get('start_year', type=int)
        end_year = request.form.get('end_year', type=int)

        # 额外的年份范围检查
        if start_year < 1993 or end_year > 2024:
            return "<h1>Please enter a valid year between 1993 and 2024。</h1>"

        if start_year and end_year:
            # 生成图表
            figure = create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('sea_level_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('sea_level_visualize.html')


if __name__ == '__main__':
    app.run(debug=True)
