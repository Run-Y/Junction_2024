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

    # 创建 Plotly 图表
    trace = go.Scatter(
        x=filtered_data['year_fraction'],
        y=filtered_data['GMSL_GIA_applied'],
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
    return redirect(url_for('sea_level_visualize_route'))

@app.route('/sea_level_visualize_route', methods=['GET'])
def sea_level_visualize_route():
    # 获取表单输入的年份
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    # 创建图表
    figure = create_plot(start_year, end_year)
    # 将图表转换为 HTML 格式嵌入到页面中
    graph_html = figure.to_html(full_html=False)
    return render_template('sea_level_visualize.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
