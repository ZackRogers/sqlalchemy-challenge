import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
station = Base.classes.station

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
        f'<h3>To get data add path to url:</h3>'
        f"<ul><li>/api/v1.0/precipitation</li>"
        f"<li>/api/v1.0/stations</li>"
        f"<li>/api/v1.0/tobs</li>" +
        "<li>/api/v1.0/<{start}></li>" +
        "<li>/api/v1.0/<{start}>/<{end}></li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurements names"""
    # Query all measurementss
    return { date: prcp for date, prcp in session.query(measurements.date, measurements.prcp).all() }
    # results = session.query(measurements.date, measurements.prcp).all()
    # respond = {}
    # for date, prcp in results:
    #     respond[date]: prcp 
    # print(respond)

@app.route("/api/v1.0/stations")
def get_stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return { station: name for station, name in session.query(station.station, station.name).all() }

@app.route("/api/v1.0/tobs")
def get_tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return { date: tobs for date, tobs in session.query(measurements.date, measurements.tobs).all() }


#@app.route('/api/v1.0/<start>')
#@app.route('/api/v1.0/<start>/<end>')
#def tobs_result(start, end = '2017-08-23'): 
    #session = Session(engine)
   # if(end = False)
# create start route


# create start route
@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    """TMIN, TAVG, and TMAX per date starting from a starting date.
    Args:
        start (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create session link from Python to the DB
    session = Session(engine)
    return_list = []
    #String format as desired
    format_str = '%Y-%m-%d'
    start_dt = dt.datetime.strptime(start, format_str)
    results =   session.query(  measurements.date,\
                                func.min(measurements.tobs), \
                                func.avg(measurements.tobs), \
                                func.max(measurements.tobs)).\
                        filter(measurements.date >= start_dt).\
                        group_by(measurements.date).all()
    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)
    session.close()    
    return jsonify(return_list)
@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):
    """TMIN, TAVG, and TMAX per date for a date range.
    Args:
        start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create session link from Python to the DB
    session = Session(engine)
    return_list = []
    #String format as desired
    format_str = '%Y-%m-%d'
    start_dt = dt.datetime.strptime(start, format_str)
    end_dt = dt.datetime.strptime(end, format_str)
    results =   session.query(measurements.date,\
                                func.min(measurements.tobs), \
                                func.avg(measurements.tobs), \
                                func.max(measurements.tobs)).\
                        filter((measurements.date >= start_dt) , (measurements.date <= end_dt)).\
                        group_by(measurements.date).all()
    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)
    session.close()    
    return jsonify(return_list)

if __name__ == '__main__':
    app.run(debug=True)