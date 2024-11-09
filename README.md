# Climate Data Dashboard

This is a web application designed to visualize global climate change data, including the following:

- **Global Temperature Change**
- **CO2 Emissions**
- **Sea Level Rise**
- **Glacier Ice Mass Loss**

The app provides interactive line charts for each dataset and offers actionable recommendations for individuals on how to contribute to combating climate change.

## Requirements

- **Python 3.x**
- **Flask** (for the web server)
- **Matplotlib** (for plotting data)

### Install Dependencies

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install the required Python libraries by running the following command:

   ```bash
   pip install -r requirements.txt

Certainly! Here is the complete README.md in English, formatted for direct use on GitHub:

# Climate Data Dashboard

This is a web application designed to visualize global climate change data, including the following:

- **Global Temperature Change**
- **CO2 Emissions**
- **Sea Level Rise**
- **Glacier Ice Mass Loss**

The app provides interactive line charts for each dataset and offers actionable recommendations for individuals on how to contribute to combating climate change.

## Requirements

- **Python 3.x**
- **Flask** (for the web server)
- **Matplotlib** (for plotting data)

### Install Dependencies

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install the required Python libraries by running the following command:

   ```bash
   pip install -r requirements.txt
The requirements.txt file should contain the following dependencies:

Flask
matplotlib
Setting Up the Background Image (Optional)
To enhance the visual appearance of the dashboard, you can add a background image:

Download your preferred background image.
Place the image in the same directory as the index.html file, or place it in a folder named static (Flask will serve static files from this directory).
Update the CSS in index.html to point to the image. You can use the following code:
If the image is in the same directory:

css
复制代码
background-image: url('back.jpg');
If the image is inside the static folder:

css
复制代码
background-image: url('/static/back.jpg');
Running the Application
To run the Flask application, follow these steps:

In your terminal, navigate to the project directory.

Run the Flask app:

python app.py
Open a web browser and visit http://127.0.0.1:5000 to view the dashboard.

Directory Structure
Here is a suggested directory structure for your project:

/climate-dashboard
    ├── /static
        └── back.jpg      # Background image (optional)
    ├── /templates
        └── index.html    # Main HTML file
    ├── app.py            # Flask application
    ├── requirements.txt  # List of dependencies
    └── README.md         # This file
Accessing the Data
The dashboard will display interactive line charts for the following datasets:

Global Temperature Change
CO2 Emissions
Sea Level Rise
Glacier Ice Mass Loss
Clicking on each dataset will open a corresponding line chart with relevant data, enabling users to explore trends and insights.

Climate Action Recommendations
The dashboard includes a feature where users can click a button to view recommendations on how to take climate action, in alignment with the United Nations Sustainable Development Goal 13: Climate Action.



