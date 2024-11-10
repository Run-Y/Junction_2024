# Climate Data Dashboard

This is a web application that visualizes global climate change data, including:

- Global Temperature Change
- CO₂ Emissions
- Sea Level Change
- Glacier Ice Mass Loss

The app provides interactive line charts for each dataset and offers recommendations on how individuals can contribute to addressing climate change.

### Key Features

- **Interactive Charts**: Users can interact with each chart, zooming in, selecting specific timeframes, and comparing different data series.
- **Real-time Data**: The dashboard is designed to pull in up-to-date information from reliable sources, ensuring that the data reflects current trends in climate change.
- **Actionable Insights**: The recommendations are not just informational—they are intended to guide users toward meaningful actions to reduce their impact on the planet.
- **User-Friendly Interface**: The design is intuitive, with easy navigation between different sections of the dashboard, making it accessible to both experts and the general public.

## Requirements

- Python 3.x
- Flask (for the web server)
- Matplotlib (for plotting data)

### Install Dependencies

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

Where `requirements.txt` should contain the following:

```
Flask
matplotlib
pandas
plotly
```

### Running the Application

1. In the terminal, navigate to the project directory and run the Flask app:

```bash
python app.py
```

2. Open a web browser and navigate to `http://127.0.0.1:5000` to view the dashboard.


### Accessing the Data

The dashboard will display the following data on interactive line charts:

- **Global Temperature Change**
- **CO₂ Emissionss**
- **Sea Level Change**
- **Glacier Ice Mass Loss**

Clicking on each item in the dashboard will open a chart with the relevant data.

### Recommendations

There is a button on the dashboard that displays public recommendations for climate action based on the United Nations Sustainable Development Goals (SDG 13: Climate Action).

### Why It Matters

By providing clear, accessible data on climate change and linking it to actionable recommendations, the dashboard aims to inform, educate, and inspire action. It empowers users to understand the urgency of addressing climate change and gives them concrete steps they can take to contribute to global sustainability efforts. Whether you’re a policymaker, a business leader, or an individual, this tool provides the information needed to make informed decisions and drive positive change in the fight against climate change.

