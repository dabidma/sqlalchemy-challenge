from flask import Flask, jsonify
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#create engine for database
engine = create_engine('sqlite:///hawaii.sqlite')

#automap and reflect
base = automap_base()
base.prepare(engine,reflect=True)
#print(base.classes.keys()) ['measurement', 'station']
base.classes.keys()

#save references to each table
measurement = base.classes.measurement
station = base.classes.station

#create session
session = Session(engine)

#start flask
app = Flask(__name__)


#home page and list all available routes with /
@app.route('/')
def home():
    print('live')
    return ('<html>'
        '<h1>Surfs Up Flask API</h1>'
        '<hr>'
        '<a href="/api/v1.0/precipitation">Precipitation Analysis</a><br/>'
        '<a href="/api/v1.0/stations">Stations Analysis</a><br/>'
        '<a href="/api/v1.0/tobs">TOBS</a><br/>'
        '<a href="/api/v1.0/<start>">Start day</a><br/>'
        '<a href="/api/v1.0/<start>/<end>">End Day</a><br/>'
    )
#precipitation analysis
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date one year from the last date in data set.
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    prec_scores = session.query(measurement.date, measurement.prcp).order_by(measurement.date.desc()).all()

    #convert to dictionary
    prec_scores_list = dict(prec_scores)
    #return as json
    return jsonify(prec_scores_list)

@app.route('/api/v1.0/stations')
def stations():
    #Return a JSON list of stations from the dataset.
    stations = session.query(station.station, station.name).all()
    #convert to lsit
    stations_list = dict(stations)
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    #Query the dates and temperature observations of the most active station for the previous year of data.
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_last_twelve = session.query(measurement.date,measurement.tobs).filter(measurement.date >= one_year).filter(measurement.station == 'USC00519281').order_by(measurement.date).all()
    tobs_data = dict(tobs_last_twelve)
    return jsonify(tobs_data)

# @app.route('/api/v1.0/<start>')
# #user inputs a start day
# def start_day(start):
#     #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
#     start_day = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()
#     start_day_list = dict(start_day)
#     return jsonify(start_day_list)

#added debugger to constantly use
if __name__ == '__main__':
    app.run(debug=True)