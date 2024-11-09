import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import io
import logging

app = Flask(__name__)

# 图片保存的目录
app.config['UPLOAD_FOLDER'] = 'static/images'

# 获取NASA Power数据的函数
def get_nasa_power_data(latitude, longitude, start_date, end_date):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start": start_date,
        "end": end_date,
        "community": "RE",
        "parameters": "ALLSKY_SFC_SW_DWN,WS10M,WS50M,T2M,PRECTOTCORR",  # 要获取的参数
        "format": "JSON",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败，将抛出异常
        data = response.json()
        return data["properties"]["parameter"]
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {e}")
        return None


# 绘制天气数据的函数
def plot_weather_data(start_year, end_year, latitude, longitude):
    try:
        parameters = ["ALLSKY_SFC_SW_DWN", "WS10M", "WS50M", "T2M", "PRECTOTCORR"]
        colors = plt.cm.viridis(np.linspace(0, 1, end_year - start_year + 1))
        years = list(range(start_year, end_year + 1))

        plt.figure(figsize=(14, 12))

        for i, param in enumerate(parameters):
            plt.subplot(2, 3, i + 1)
            monthly_values = {year: {month: [] for month in range(1, 13)} for year in years}

            for j, year in enumerate(years):
                start_date = f"{year}0101"
                end_date = f"{year}1231"
                data = get_nasa_power_data(latitude, longitude, start_date, end_date)

                if data:
                    dates = [datetime.strptime(date, "%Y%m%d") for date in data[param].keys()]
                    values = list(data[param].values())

                    for date, value in zip(dates, values):
                        month = date.month
                        monthly_values[year][month].append(value)

            avg_monthly_values = {}
            for year in years:
                avg_monthly_values[year] = [np.mean(monthly_values[year][month]) if monthly_values[year][month] else 0 for
                                            month in range(1, 13)]

            for j, year in enumerate(years):
                plt.plot(range(1, 13), avg_monthly_values[year], label=str(year), color=colors[j])

            plt.title(f"{param} Monthly Comparison")
            plt.xlabel("Month")
            plt.ylabel("Average Value")
            plt.xticks(range(1, 13))
            plt.legend()

        plt.tight_layout()

        # 将图像保存在静态文件夹中并返回文件名
        img_filename = f"plot_{latitude}_{longitude}_{start_year}_{end_year}.png"
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        with open(img_path, 'wb') as f:
            f.write(img.read())

        return img_filename
    except Exception as e:
        logging.error(f"绘制图表时发生错误: {e}")
        return None


# 根路由
@app.route('/')
def home():
    return "<h1>Welcome to the Temperature Visualization App</h1>"  # 或者渲染一个HTML模板


# 路由: 获取数据并显示图表
@app.route('/temperature_visualize', methods=['GET', 'POST'])
def temperature_visualize():
    if request.method == 'POST':
        start_year = int(request.form['start_year'])
        end_year = int(request.form['end_year'])
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        # 调用绘图功能
        img = plot_weather_data(start_year, end_year, latitude, longitude)
        return send_file(img, mimetype='image/png')  # 将图片返回给浏览器

    return render_template('temperature_visualize.html')  # 显示表单页面


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
