from flask import Flask, render_template, jsonify, send_file, request
import requests
import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime
import temperature_visualize as tv_module # 导入 Temperature_Visualize.py 中的功能

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



if __name__ == '__main__':
    app.run(debug=True)
