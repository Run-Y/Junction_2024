from flask import Flask, render_template, send_file, request

import sea_level_visulize as slv_module
import temperature_visualize as tv_module  # 导入 Temperature_Visualize.py 中的功能
import ice_sheets_visualize as isv_module
import carbon_dioxide_visualize as cdv_module
import global_temperature_visualize as gtv_module

app = Flask(__name__)


# 主页面路由
@app.route('/')
def index():
    return render_template('index.html')


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
            figure = gtv_module.create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('global_temperature_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求时显示表单页面
    return render_template('global_temperature_visualize.html')


# 路由: 温度可视化
@app.route('/temperature_visualize', methods=['GET', 'POST'])
def temperature_visualize():
    if request.method == 'POST':
        city_name = request.form['city']  # 获取城市名称
        start_year = int(request.form['start_year'])
        end_year = int(request.form['end_year'])

        # 使用城市名称获取经纬度
        latitude, longitude = tv_module.get_lat_lng_from_city(city_name)
        if latitude is None or longitude is None:
            return "<h1>Error: Could not find the city or its coordinates.</h1>"

        # 调用绘图功能并获取Base64编码图像
        img_base64 = tv_module.plot_weather_data(start_year, end_year, latitude, longitude)
        if img_base64:
            # 将生成的图像嵌入HTML页面
            return render_template('temperature_visualize.html', img_url=img_base64)
        else:
            return "<h1>Error in generating plot</h1>"

    return render_template('temperature_visualize.html')  # 显示表单页面


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
            figure = slv_module.create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('sea_level_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('sea_level_visualize.html')

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
            figure = isv_module.create_plot(start_year, end_year, data_file)
            if figure:
                graph_html = figure.to_html(full_html=False)
                return render_template('ice_sheets_visualize.html', graph_html=graph_html)
            else:
                return "<h1>File not found or data format error.</h1>"
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('ice_sheets_visualize.html')

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
            figure = cdv_module.create_plot(start_year, end_year)
            graph_html = figure.to_html(full_html=False)
            return render_template('carbon_dioxide_visualize.html', graph_html=graph_html)
        else:
            return "<h1>Please enter a valid year.</h1>"

    # GET 请求显示表单页面
    return render_template('carbon_dioxide_visualize.html')


if __name__ == '__main__':
    app.run(debug=True)