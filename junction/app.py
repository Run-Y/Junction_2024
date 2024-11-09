from flask import Flask, render_template, send_file, request

import sea_level_visulize as slv_module
import temperature_visualize as tv_module  # 导入 Temperature_Visualize.py 中的功能

app = Flask(__name__)


# 主页面路由
@app.route('/')
def index():
    return render_template('index.html')


# 路由: 温度可视化
@app.route('/temperature_visualize', methods=['GET', 'POST'])
def temperature_visualize():
    if request.method == 'POST':
        start_year = int(request.form['start_year'])
        end_year = int(request.form['end_year'])
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        # 调用绘图功能
        img = tv_module.plot_weather_data(start_year, end_year, latitude, longitude)
        if img:
            # 将生成的图像直接发送到浏览器
            return send_file(img, mimetype='image/png')
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





if __name__ == '__main__':
    app.run(debug=True)
