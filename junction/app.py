from flask import Flask, render_template, jsonify, send_file, request
import requests
import matplotlib.pyplot as plt
import io
import numpy as np
from datetime import datetime
import temperature_visualize  # 导入 Temperature_Visualize.py 中的功能

app = Flask(__name__)


# 主页面路由
@app.route('/')
def index():
    return render_template('index.html')


# 路由: 温度可视化
@app.route('/temperature_visualize', methods=['GET', 'POST'])
def temperature_visualize():
    try:
        if request.method == 'POST':
            # 获取表单数据
            start_year = int(request.form['start_year'])
            end_year = int(request.form['end_year'])
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])

            # 调用 Temperature_Visualize 中的绘图功能
            temperature_visualize.plot_weather_data(start_year, end_year, latitude, longitude)
            return render_template('index.html', message="Data visualization complete")

        return render_template('temperature_visualize.html')  # 显示表单
    except Exception as e:
        return f"Error occurred: {e}"



if __name__ == '__main__':
    app.run(debug=True)
