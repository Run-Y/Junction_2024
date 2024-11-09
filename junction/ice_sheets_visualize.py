import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def create_plot(start_year, end_year, file_name):
    # 根据选择的文件加载不同的数据
    file_path = f'./data/{file_name}'
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        return None

    # 根据年份范围筛选数据
    filtered_data = data[(data['TIME (year.decimal)'] >= start_year) & (data['TIME (year.decimal)'] <= end_year)]

    # 根据选择的数据集设置纵坐标
    if file_name == "antarctica_mass_data.csv":
        mass_column = 'Antarctic mass (Gigatonnes)'
        uncertainty_column = 'Antarctic mass 1 - sigma uncertainty (Gigatonnes)'
        title = "Antarctic Mass"
    else:
        mass_column = 'Greenland mass (Gigatonnes)'  # 假设你有 Greenland 数据列
        uncertainty_column = 'Greenland mass 1-sigma uncertainty (Gigatonnes)'  # 假设你有 Greenland 的 uncertainty 列
        title = "Greenland Mass"

    # 创建 Plotly 图表
    trace = go.Scatter(
        x=filtered_data['TIME (year.decimal)'],  # 横坐标为 Time
        y=filtered_data[mass_column],  # 纵坐标为对应的 Mass
        mode='lines+markers',
        name='',
        hovertemplate='Time: %{x}<br>' +
                      f'{title}' + '%{y}(Gigatonnes)' + f' (±{filtered_data[uncertainty_column].iloc[0]})' # 显示不确定性
    )

    layout = go.Layout(
        title=f'{title} Mass Loss ({start_year} - {end_year})',
        xaxis=dict(title='Time'),
        yaxis=dict(title=f'{title} Mass (Gigatonnes)'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        template='plotly_white'
    )

    figure = go.Figure(data=[trace], layout=layout)
    return figure


@app.route('/')
def home():
    # Your handling code here
    return redirect(url_for('ice_sheets_visualize'))


@app.route('/ice_sheets_visualize', methods=['GET', 'POST'])
def ice_sheets_visualize():
    if request.method == 'POST':
        # 获取表单输入的年份和数据文件
        start_year = request.form.get('start_year', type=int)
        end_year = request.form.get('end_year', type=int)
        data_file = request.form.get('data_file', type=str)

        # 额外的年份范围检查
        if start_year < 2002 or end_year > 2024:
            return "<h1>Please enter a valid year between 2002 and 2024.</h1>"

        if start_year and end_year:
            # 生成图表
            figure = create_plot(start_year, end_year, data_file)
            if figure:
                graph_html = figure.to_html(full_html=False)
                return render_template('ice_sheets_visualize.html', graph_html=graph_html)
            else:
                return "<h1>File not found or data format error.</h1>"
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('ice_sheets_visualize.html')



if __name__ == '__main__':
    app.run(debug=True)
