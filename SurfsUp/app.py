import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float 
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()

Base.prepare(engine)

Measurement=Base.classes.measurement
Station=Base.classes.station

session = Session(engine)

app=Flask(__name__)

@app.route("/")
def welcome():
    return(f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
        )

# @app.route("/api/v1.0/precipitation")
# def 
#     return()

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station.station).all()
    stations=list(np.ravel(results))
    return jsonify(stations)

# @app.route("/api/v1.0/tobs")
# def 
#     return()

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temps(start=None,end=None):
    sel=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    if not end:
        # start=dt.datetime.strptime(start,"%m%d%Y")
        results=session.query(*sel).filter(Measurement.date>=start).all()
        temps=list(np.ravel(results))
        return jsonify(temps)
    
    # start=dt.datetime.strptime(start,"%m%d%Y")
    # end=dt.datetime.strptime(end,"%m%d%Y")
    results=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    temps=list(np.ravel(results))
    return jsonify(temps)


    return()


if __name__=="__main__":
    app.run()

