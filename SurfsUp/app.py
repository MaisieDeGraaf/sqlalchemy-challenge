# Import the dependencies.
from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy.ext.automap import automap_base
import os

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
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
    return ("Welcome to the Weather App!<br>"
    "Directory:<br>"
    "- /api/v1.0/precipitation: Return JSON of the last 12 months of precipitation data from the latest date<br>"
    "- /api/v1.0/stations: Return JSON list of stations<br>"
    "- /api/v1.0/tobs: Return JSON list of temperature observations from the most active station<br>"
    "- /api/v1.0/YYYY-MM-DD: Return a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start date in the address bar in place of YYYY-MM-DD<br>"
    "- /api/v1.0/YYYY-MM-DD/YYYY-MM-DD: Return a JSON list of the minimum temperature, average temperature, and the maximum temperature from a specified start and end date in the address bar in place of YYYY-MM-DD<br>")

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
def start(start):  

    stats = session.query(
        func.min(measurement_table.tobs),
        func.max(measurement_table.tobs),
        func.avg(measurement_table.tobs)
    )

    if start:
        stats = stats.filter(measurement_table.date >= start)

    result = stats.first()
    
    temperature_data = {
        'min_temperature': result[0],  
        'max_temperature': result[1],
        'avg_temperature': round(result[2])
    }

    return jsonify(temperature_data)
    
@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def start_end(start, end):  

    stats = session.query(
        func.min(measurement_table.tobs),
        func.max(measurement_table.tobs),
        func.avg(measurement_table.tobs)
    )

    if start:
        stats = stats.filter(measurement_table.date >= start)
    if end:
        stats = stats.filter(measurement_table.date <= end)

    result = stats.first()
    
    temperature_data = {
        'min_temperature': result[0],  
        'max_temperature': result[1],
        'avg_temperature': round(result[2])
    }


    return jsonify(temperature_data)

if __name__ == '__main__':
    app.run(debug=True)

