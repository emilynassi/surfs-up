import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query dates and precipiation observations"""
    # Query temps and dates from the last year
    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= "2016-08-23").all()
    
    # Convert list into dictionary
    for item in results:
        results_dict = {}
        results_dict["date"]=Measurements.date
        results_dict["prcp"]=Measurements.prcp
    return jsonify(results)


@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations"""
    # Query all passengers
    results = session.query(Stations.station).all()

    # Convert list of tuples into normal list using np.ravel
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query station and temp data"""
    # Query temps and dates from the last year
    results = session.query(Measurements.station, Measurements.tobs).all()
    
    # Convert list into dictionary
    for item in results:
        results_dict = {}
        results_dict["date"]=Measurements.station
        results_dict["tobs"]=Measurements.tobs
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start):
    #Define start date
    start_date = datetime.strptime(start,'%Y-%m-%d')
    #Query temperature data
    max_temp = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    min_temp = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    avg_temp = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    
    temp={}
    temp["Maximum Temperature"] = max_temp[0]
    temp["Minimum Temperature"] = min_temp[0]
    temp["Average Temperature"] = avg_temp[0]

    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    #Define start date and end date
    start_date = datetime.strptime(start,'%Y-%m-%d')
    end_date = datetime.strptime(end,'%Y-%m-%d')
    #Query temperature data
    max_temp = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    min_temp = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    avg_temp = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    
    temp={}
    temp["Maximum Temperature"] = max_temp[0]
    temp["Minimum Temperature"] = min_temp[0]
    temp["Average Temperature"] = avg_temp[0]

    return jsonify(temp)

if __name__ == '__main__':
    app.run(debug=True)