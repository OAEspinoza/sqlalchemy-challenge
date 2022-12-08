import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float 
from sqlalchemy import inspect
from flask import Flask, json, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()

Base.prepare(engine)

Measurement=Base.classes.measurement
Station=Base.classes.station

app=Flask(__name__)

@app.route("/")
def welcome():
    return(f"Welcome to Omar's Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format YYYY-MM-DD.</p>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_from_latest_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    precipitation_scores=session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=year_from_latest_date).\
        order_by(Measurement.date).all()
    data=[]
    for date,prcp in precipitation_scores:
        precip_dict={}
        precip_dict["date"]=date
        precip_dict["prcp"]=prcp
        data.append(precip_dict)
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results=session.query(Station.station).all()
    stations=list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_temp_readings=session.query(Measurement.tobs).\
    filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').\
    order_by(Measurement.date).all()
    most_active_temp_readings=list(np.ravel(most_active_temp_readings))
    return jsonify(most_active_temp_readings)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temps(start=None,end=None):
    session = Session(engine)
    sel=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    if not end:
        results=session.query(*sel).filter(Measurement.date>=start).all()
        temps=list(np.ravel(results))
        return jsonify(temps) 
    results=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    # session.close()
    temps=list(np.ravel(results))
    return jsonify(temps)

if __name__=="__main__":
    app.run(debug=True)

