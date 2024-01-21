# Import the dependencies.
from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine(r"sqlite:///C:\Users\qwert\Documents\GitHub\sqlalchemy-challenge\Resources\hawaii.sqlite")
hawaii_cxn = engine.connect()
# Save references to each table

Base = automap_base()
Base.prepare(engine, reflect=True)
classes = Base.classes.keys()
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

recent_date = session.query(func.max(measurement_table.date)).scalar()
recent_date_convert = dt.datetime(*map(int, recent_date.split('-')))
one_year_previous = (recent_date_convert - dt.timedelta(days=365))
precipitation_data = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= one_year_previous).order_by(measurement_table.date).all()
precipitation_dict = {date: prcp for date, prcp in precipitation_data}

stations_data = session.query(station_table.name, station_table.station).all()
stations_dict = [{'name': name, 'station': station} for name, station in stations_data]

active_stations = session.query(measurement_table.station, func.count(measurement_table.station))\
.group_by(measurement_table.station)\
.order_by(func.count(measurement_table.station).desc()).all()
most_active_station = active_stations[0][0]

most_active_station_stats = session.query(measurement_table.station, measurement_table.tobs, measurement_table.date).filter(measurement_table.station == most_active_station).all()



#################################################
# Flask Routes
#################################################
app = Flask(__name__)

@app.route("/")
def index(): 
        return """
    Welcome to the Weather App!
    Directory:
    - /api/v1.0/precipitation: Return JSON of the last 12 months of precipitation data from the latest date
    - /api/v1.0/stations: Return JSON list of stations
    - /api/v1.0/tobs: Return JSON list of temperature observations from the most active station
    - /api/v1.0/<start>: Return a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start date
    - /api/v1.0/<start>/<end>: Return a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start and end date
    """

@app.route("/api/v1.0/precipitation")
def precp(): 
    return(jsonify(precipitation_dict))
@app.route("/api/v1.0/stations")
def station(): 
    return(jsonify(stations_dict))
@app.route("/api/v1.0/tobs")
def active(): 
    return(jsonify(most_active_station_stats))
@app.route("/api/v1.0/<start>", methods=['GET'])
def start(): 
    start_date = request.arg.get('start_date')

    stats = session.query(
        func.min(measurement_table.tobs),
        func.max(measurement_table.tobs),
        func.avg(measurement_table.tobs)
    )

    if start_date:
        stats= query.filter(measurement.date >= start_date)

    result = stats.first()
    
    temperature_data = {
        'start_date': start_date,
        'min_temperature': result.min_temp,
        'max_temperature': result.max_temp,
        'avg_temperature': result.avg_temp
    }

    return jsonify(temperature_data)
    
@app.route("/api/v1.0/<start>/<end>")
def startend(): 
    start_date = request.arg.get('start_date')
    end_date = request.arg.get('end_date')

    stats = session.query(
        func.min(measurement_table.tobs),
        func.max(measurement_table.tobs),
        func.avg(measurement_table.tobs)
    )

    if start_date:
        stats= stats.filter(measurement.date >= start_date)
    if end_date:
        stats = stats.filter(measurement.date <= end_date)
    
    result = stats.first()
    
    temperature_data = {
        'start_date': start_date,
        'end_date': end_date,
        'min_temperature': result.min_temp,
        'max_temperature': result.max_temp,
        'avg_temperature': result.avg_temp
    }

    return jsonify(temperature_data)

if __name__ == '__main__':
    app.run(debug=True)