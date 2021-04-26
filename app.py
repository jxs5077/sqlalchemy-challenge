from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, and_
import numpy as np
import pandas as pd
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"
    


@app.route("/precipitation")
def prcp():
    session=Session(engine)
    prior_year=dt.date(2017,8,23) - dt.timedelta(days=365)
  
    query_last=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > prior_year).order_by(Measurement.date).all()
    session.close()
    return jsonify(query_last)


@app.route("/stations")
def stations():
    session=Session(engine)
    stations=session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    session.close()
    return jsonify(stations)


@app.route("/tobs")
def tobs():
    session=Session(engine)
    prior_year=dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs52=session.query(Measurement.tobs, Measurement.date).filter(Measurement.station=="USC00519281").filter(Measurement.date >= prior_year).all()
    session.close()
    return jsonify (tobs52)


@app.route("/start/<startdate>")
def start(startdate):
    session=Session(engine)
    startdate_results=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=startdate).all()
    session.close()
    return jsonify (startdate_results)

@app.route("/range/<daterangestart>/<daterangeend>")
def range(daterangestart, daterangeend):
    session=Session(engine)
    startend=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= daterangestart).\
    filter(Measurement.date <= daterangeend).all()
    
    session.close()
    return jsonify (startend)

if __name__ == '__main__':
    app.run(debug=True)
