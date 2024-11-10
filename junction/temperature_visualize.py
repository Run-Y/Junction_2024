import base64

from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import io
import logging

app = Flask(__name__)

# 获取城市经纬度的函数
# 调用 Nominatim API 获取城市的经纬度
import requests
import logging


def get_lat_lng_from_city(city_name):
    try:
        # 使用你的 Google API 密钥
        Key = "AIzaSyBXO0ZpOUkaZgotj3UxCkK3E7xbBDZD9Hw"
        # 构建API请求的URL
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={Key}"

        # 发送请求
        response = requests.get(url)
        data = response.json()

        # 检查返回的数据是否正常
        if data['status'] == 'OK' and len(data['results']) > 0:
            # 获取第一个匹配结果中的经纬度
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            # 如果没有匹配结果，返回None
            return None, None

    except Exception as e:
        logging.error(f"Failed: {e}")
        return None, None


# 获取NASA Power数据的函数
def get_nasa_power_data(latitude, longitude, start_date, end_date):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start": start_date,
        "end": end_date,
        "community": "RE",
        "parameters": "ALLSKY_SFC_SW_DWN,WS10M,WS50M,T2M,PRECTOTCORR",
        "format": "JSON",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["properties"]["parameter"]
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {e}")
        return None

# 绘制天气数据的函数
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

            for year in years:
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
                avg_monthly_values[year] = [
                    np.mean(monthly_values[year][month]) if monthly_values[year][month] else 0
                    for month in range(1, 13)
                ]

            for year in years:
                plt.plot(range(1, 13), avg_monthly_values[year], label=str(year), color=colors[years.index(year)])

            plt.title(f"{param} Monthly Comparison")
            plt.xlabel("Month")
            plt.ylabel("Average Value")
            plt.xticks(range(1, 13))
            plt.legend()

        plt.tight_layout()

        # 将图像保存到内存并转为Base64编码
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return img_base64
    except Exception as e:
        logging.error(f"绘制图表时发生错误: {e}")
        return None

@app.route('/')
def home():
    return redirect(url_for('temperature_visualize_route'))

# 路由: 获取数据并显示图表
@app.route('/temperature_visualize', methods=['GET', 'POST'])
def temperature_visualize_route():
    if request.method == 'POST':
        city_name = request.form['city']  # 获取城市名称
        start_year = int(request.form['start_year'])
        end_year = int(request.form['end_year'])

        # 使用城市名称获取经纬度
        latitude, longitude = get_lat_lng_from_city(city_name)
        if latitude is None or longitude is None:
            return "<h1>Error: Could not find the city or its coordinates.</h1>"

        # 调用绘图功能并获取Base64编码图像
        img_base64 = plot_weather_data(start_year, end_year, latitude, longitude)
        if img_base64:
            # 将生成的图像嵌入HTML页面
            return render_template('temperature_visualize.html', img_url=img_base64)
        else:
            return "<h1>Error in generating plot</h1>"

    return render_template('temperature_visualize.html')  # 显示表单页面


if __name__ == '__main__':
    app.run(debug=True)
