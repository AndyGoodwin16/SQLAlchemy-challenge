#Import dependencies.
import numpy as np
import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, Response

#Created engine to hawaii.sqlite.
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflected an existing database into a new model.
Base = automap_base()

#Reflected the tables.
Base.prepare(engine, reflect=True)

#Saved references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

#Setup Flask app.
app = Flask(__name__)

#Setup Flask routes.
@app.route("/")
def homepage():
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
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    #Looped through the results to create a dictionary of "Date":"Prcp" key:value pairs.
    prcp_data = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["Date"] = date
        date_prcp_dict["Prcp"] = prcp
        date_prcp_dict.append(date_prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = [z.station for z in session.query(Station.station)]
    
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    #Found the most active station.
    a = session.query(Station.station)
    b = a.filter(Station.station == Measurement.station)
    c = b.group_by(Station.station)
    d = c.order_by(func.count(Measurement.station).desc())
    e = d.all()
    most_active_station = e[0][0]
    
    #Found the most recent date of measurement at the most active station.
    f = session.query(Measurement.date)
    g = f.filter(Measurement.station == most_active_station)
    h = g.order_by(Measurement.date.desc())
    most_recent_date = h.first().date
    
    #Found the date one year prior to most recent date of measurement at the most active station.
    year = most_recent_date[0:4]
    month = most_recent_date[5:7]
    day = most_recent_date[8:10]
    most_recent_date = dt.date(int(year), int(month), int(day))
    one_year_past_date = most_recent_date - dt.timedelta(days=365)
    
    #Created a list of temperature measurements spanning one year before the most recent date of measurement at the most active station.
    i = session.query(Measurement.tobs)
    j = i.filter(Measurement.date >= one_year_past_date)
    k = j.filter(Measurement.station == most_active_station)
    l = k.order_by(Measurement.date)
    m = l.all()
    temp_list = [z.tobs for z in m]
    
    session.close()
    
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    
    #Uncomment the line below and insert desired start date in the below format.
    #start_date = dt.date(int(INSERT YEAR HERE), int(INSERT MONTH HERE), int(INSERT DAY HERE))
    
    #Found the min temp from start date to present.
    n = session.query(func.min(Measurement.tobs))
    o = n.filter(Measurement.date >= start_date)
    min_temp = o.scalar()
    
    #Found the max temp from start date to present.
    p = session.query(func.max(Measurement.tobs))
    q = p.filter(Measurement.date >= start_date)
    max_temp = q.scalar()
    
    #Found the average temp from start date to present.
    r = session.query(func.avg(Measurement.tobs))
    s = r.filter(Measurement.date >= start_date)
    avg_temp = s.scalar()
    
    start_list = [min_temp, avg_temp, max_temp]
    
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    session = Session(engine)
    
    #Uncomment the line below and insert desired start and end dates in the below format.
    #start_date2 = dt.date(int(INSERT YEAR HERE), int(INSERT MONTH HERE), int(INSERT DAY HERE))
    #end_date = dt.date(int(INSERT YEAR HERE), int(INSERT MONTH HERE), int(INSERT DAY HERE))
    
    #Found the min temp from start date to end date.
    t = session.query(func.min(Measurement.tobs))
    u = t.filter(Measurement.date >= start_date2).filter(Measurement.date <= end_date)
    min_temp2 = o.scalar()
    
    #Found the max temp from start date to end date.
    v = session.query(func.max(Measurement.tobs))
    w = v.filter(Measurement.date >= start_date2).filter(Measurement.date <= end_date)
    max_temp2 = q.scalar()
    
    #Found the avg temp from start date to end date.
    x = session.query(func.avg(Measurement.tobs))
    y = x.filter(Measurement.date >= start_date2).filter(Measurement.date <= end_date)
    avg_temp2 = y.scalar()
    
    start_end_list = [min_temp2, avg_temp2, max_temp2]
    
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)