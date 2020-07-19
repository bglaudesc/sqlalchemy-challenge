from flask import Flask, jsonify
import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


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
    return (
        f"Home page<br/>"
        f"List all routes that are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/START DATE GOES HERE (YYYY-MM-DD)<br/>"
        f"/api/v1.0/START DATE GOES HERE (YYYY-MM-DD) / END DATE GOES HERE (YYYY-MM-DD)<br/>"
        
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    Previous_year ='2016-08-23'
    Data_Precipitation_12_months = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= Previous_year).\
    order_by(Measurement.date).all()

    date_prec_dict = {}
    for tuple_ in Data_Precipitation_12_months:
        date_prec_dict[tuple_[0]]=tuple_[1]
    session.close()
    return jsonify(date_prec_dict)


@app.route("/api/v1.0/stations")
def stations():
    list_of_stations = session.query(Station.station).\
    order_by(Station.station).all()

    stations_loop=[]
    for tuple_ in list_of_stations:
        stations_loop.append(tuple_[0])

    return jsonify(stations_loop)


@app.route("/api/v1.0/tobs")
def tobs_temp():
    observation_last_year = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >='2016-08-23').\
    filter('USC00519281'==Measurement.station).all()

    tempature_obeservation=[]
    for tuple_ in observation_last_year:
        tempature_obeservation.append(tuple_[1])

    session.close()
    return jsonify(tempature_obeservation)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def given_start(start,end=None):
    if end==None:
        start_route = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()[0]
    else:
        start_route = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]
    start_dictionary = {
        "min":start_route[0],
        "avg":start_route[1],
        "max":start_route[2],
    }

  
    session.close()
    return jsonify(start_dictionary)






if __name__ == "__main__":
    app.run(debug=True)
