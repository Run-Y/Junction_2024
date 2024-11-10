# Climate Data Dashboard

This is a web application that visualizes global climate change data, including:

- Global temperature change
- CO2 emissions
- Sea level rise
- Glacier ice mass loss

The app provides interactive line charts for each dataset and offers recommendations on how individuals can contribute to addressing climate change.

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
```

### Running the Application

1. In the terminal, navigate to the project directory and run the Flask app:

```bash
python app.py
```

2. Open a web browser and navigate to `http://127.0.0.1:5000` to view the dashboard.

### Directory Structure

```
/climate-dashboard
    ├── /static
        └── back.jpg      # Background image (optional)
    ├── /templates
        └── index.html    # Main HTML file
    ├── app.py            # Flask application
    ├── requirements.txt  # List of dependencies
    └── README.md         # This file
```

### Accessing the Data

The dashboard will display the following data on interactive line charts:

- **Global Temperature Change**
- **CO2 Emissions**
- **Sea Level Rise**
- **Glacier Ice Mass Loss**

Clicking on each item in the dashboard will open a chart with the relevant data.

### Recommendations

There is a button on the dashboard that displays public recommendations for climate action based on the United Nations Sustainable Development Goals (SDG 13: Climate Action).

