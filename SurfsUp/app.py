# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with= engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"  
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago).all()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precipitation=precip)
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.station=='USC00519281').filter(measurement.date >= year_ago).all()


    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(stations=all_names)

@app.route("/api/v1.0/<start>")
def math(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    results = session.query(func.avg(measurement.tobs), 
                            func.min(measurement.tobs), 
                            func.max(measurement.tobs)).\
        filter(measurement.date >= year_ago).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)
