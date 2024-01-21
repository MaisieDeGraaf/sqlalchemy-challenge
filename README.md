# Weather App - SurfsUp

Welcome to the Weather App! This application provides weather-related data through a Flask API and includes interactive visualizations.

## Project Structure

The project is organized as follows:

- `SurfsUp/`: Contains the main Flask application and other related files.
  
  - `app.py`: The main Flask application that serves the API endpoints.
    
  - `climate_starter.ipynb`: Jupyter Notebook containing starter code for data analysis and visualization.
  
- `Resources/`: Contains the SQLite database and data files.
  
  - `hawaii.sqlite`: SQLite database file containing weather-related data.
    
  - Other data files such as `hawaii_measurements.csv` and `hawaii_stations.csv` that the SQLite database references.

## Running the Application

1. Ensure you have Python installed.
   
2. Install the required dependencies using the following command:
   
   ```bash
  
   pip install flask matplotlib sqlalchemy
   
3. Open VSCode and run the application, clicking on the link generated

## API Endpoints

/: Welcome page providing a directory of available API endpoints.

/api/v1.0/precipitation: Returns JSON of the last 12 months of precipitation data from the latest date.

/api/v1.0/stations: Returns a JSON list of stations.

/api/v1.0/tobs: Returns JSON list of temperature observations from the most active station.

/api/v1.0/YYYY-MM-DD: Returns a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start date.

/api/v1.0/YYYY-MM-DD/YYYY-MM-DD: Returns a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start and end date.

## Data Analysis and Visualization

The Jupyter Notebook climate_starter.ipynb provides starter code for data analysis and visualization. It uses Matplotlib for plotting and SQLAlchemy for database interactions.

Data Analysis Completed:

- Most recent date in database
  
- Previous 12 months of precipitation data from most recent date
  
- Bar graph of the previous 12 months of precipitation data from most recent date
  
- Total number of stations in the dataset
  
- Identification of the most active station and list of activity of all stations
  
- Lists the lowest, highest, and average temperatures that filters on the most-active station id
  
- Histogram of the previous 12 months of data for the most active station based on the temperature observations and frequency of occurance

## Dependencies

Flask: A micro web framework for building web applications.

Matplotlib: A 2D plotting library for creating static, animated, and interactive visualizations in Python.

SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
