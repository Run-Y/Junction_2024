from flask import Flask, render_template, jsonify, send_file
import requests
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# NASA API密钥
API_KEY = "sx6sHUxfk6jhjcFtaKM2Su39LbqvVqPZ6fNoDdc5"
base_url = "https://api.nasa.gov/"

# 数据端点，需根据NASA API的文档进行具体替换
endpoints = {
    "temperature": "temperature_anomaly_endpoint",      # 需要确认具体端点路径
    "co2": "co2_emissions_endpoint",                    # 需要确认具体端点路径
    "sea_level": "sea_level_rise_endpoint",             # 需要确认具体端点路径
    "ice_mass_loss": "ice_mass_loss_endpoint"           # 需要确认具体端点路径
}

# 获取NASA数据的通用函数
def fetch_nasa_data(endpoint):
    params = {"api_key": API_KEY}
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 绘制折线图的函数
def plot_data(dates, values, title, ylabel):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存到内存
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

# 主页面路由
@app.route('/')
def index():
    return render_template('index.html')

# 数据图表路由
@app.route('/plot/<data_type>')
def plot(data_type):
    endpoint = endpoints.get(data_type)
    if endpoint:
        data = fetch_nasa_data(endpoint)
        if data:
            dates = [entry["year"] for entry in data]
            values = [entry["value"] for entry in data]  # 适配返回的具体字段名称
            ylabel_map = {
                "temperature": "Temperature Anomaly (°C)",
                "co2": "CO2 Emissions (MtCO2)",
                "sea_level": "Sea Level Rise (mm)",
                "ice_mass_loss": "Mass Loss (Gt)"
            }
            img = plot_data(dates, values, data_type.capitalize(), ylabel_map[data_type])
            return send_file(img, mimetype='image/png')
    return "Data not available", 404

if __name__ == '__main__':
    app.run(debug=True)
