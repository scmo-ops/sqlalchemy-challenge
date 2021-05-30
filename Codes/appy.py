# Dependencies

from flask.templating import render_template
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
import numpy as np

# Engine setup

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect = True)

# The references that have already been colected

measurement = base.classes.measurement
station = base.classes.station

# Flask setup

app = Flask(__name__)
@app.route("/")
def Home():
    return render_template('Index.html')
def temps1():
    return (
        f'Available data:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
    )


@app.route('/api/v1.0/precipitation')

def precipitation():
    '''A json where the date controls the value of the precipitation data'''
    session = Session(engine)

    '''query to retrieve data'''

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').all()
    session.close()
    precipt = []
    for date,precipt1  in results:
        prcipt_dict = {}
        prcipt_dict['date'] = date
        prcipt_dict['prcp'] = precipt1
        precipt.append(prcipt_dict)

    return jsonify(precipt)

@app.route('/api/v1.0/stations')

def stations():
    session = Session(engine)
    '''This part will return a list of all Stations'''

    stations = session.query(station.station).order_by(station.station).all()
    session.close()
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    '''This part will return a list of all TOBs'''
    # Query all tobs

    results = session.query(measurement.date, measurement.tobs, measurement.prcp).filter(measurement.date >= '2016-08-24').filter(measurement.station=='USC00519281').order_by(measurement.date).all()

    session.close()

    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict['prcp'] = prcp
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

    
@app.route('/api/v1.0/<start_date>')
def start(start):
    '''This is a json that return to the user a list of the minimum, average and the maximum temperatures for a given date'''

    temps = Session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(Measurement.date >= start_date).all()

    temp_list = []
    for min, max, avg in temps:
        start_tobs = {}
        start_tobs['min_temp'] = min
        start_tobs['avg_temp'] = avg
        start_tobs['max_temp'] = max
        temp_list.append(start_tobs) 
    return jsonify(temp_list)

@app.route('/api/v1.0/<start_date>/<end_date>')
def Start_end_date(start_date, end_date):

    session = Session(engine)

    query1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()
    tobs_date = []
    for min, avg, max in query1:
        tobs_date_dict = {}
        tobs_date_dict['min_temp'] = min
        tobs_date_dict ['avg_temp'] = avg
        tobs_date_dict ['max_temp'] = max
        tobs_date.append(tobs_date) 
    
    return jsonify(tobs_date)

if __name__ == '__main__':
    app.run(debug=True)
