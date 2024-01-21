# Import the dependencies.
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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




#################################################
# Flask Routes
#################################################
