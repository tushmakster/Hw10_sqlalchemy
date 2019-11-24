# Libraries
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




# Create an app, being sure to pass __name__
app = Flask(__name__)


# list of all available routes
@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )



@app.route("/api/v1.0/precipitation")
def q1_precip():
    max_date = session.query(func.max(Measurement.date)).all()
    max_date = dt.datetime.strptime(max_date[0][0],'%Y-%m-%d')

# Calculate the date 1 year ago from the last data point in the database
    min_date = dt.date(max_date.year - 1, max_date.month, max_date.day + 1)

# Perform a query to retrieve the data and precipitation scores
    query1 = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= min_date).all()
    query1_dict = {date: prcp for date, prcp in query1}
    return jsonify(query1_dict)



@app.route("/api/v1.0/stations")
def q2_stations():
    list_q2 = []
    query2 = session.query(Measurement.station, 
    func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    for i in query2:
        list_q2.append(i[0])

    return jsonify(list_q2)

@app.route("/api/v1.0/tobs")
def q3_temp():

    max_date = session.query(func.max(Measurement.date)).all()
    max_date = dt.datetime.strptime(max_date[0][0],'%Y-%m-%d')
    min_date = dt.date(max_date.year - 1, max_date.month, max_date.day + 1)

    query2 = session.query(Measurement.station, 
    func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    query3 = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= dt.date(2016, 8, 24)).all()
    clean = list(np.ravel(query3))
    return jsonify(clean)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def q4_avg(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        q4_1 = session.query(*sel).filter(Measurement.date >= start).all()
        clean = list(np.ravel(q4_1))
        return jsonify(clean)
    q4_2 = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    clean = list(np.ravel(q4_2))
    return jsonify(clean)


    
        


if __name__ == "__main__":
    app.run(debug=True)