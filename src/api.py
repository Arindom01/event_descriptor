from flask import Flask, request, g
from flask import jsonify
import json
import os
from datetime import datetime, timezone, timedelta
from dbutil import dbutil
import requests
from loadconfig import App_Conf
from pathlib import Path
import logging

app = Flask(__name__)

class BadRequest(Exception):
    """Custom exception class to be thrown when local error occurs."""
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.before_first_request
def initialize():
    logging.basicConfig(
        datefmt = '%Y-%m-%d %H:%M:%S ',
        format = '%(asctime)s %(message)s',
        level=logging.INFO)


@app.before_request
def before_request():
    db  = dbutil()
    
    # derive local db path
    path=os.path.join(Path(__file__).parent.parent , App_Conf().config()['db_relative_path'] )
    g.db = db.create_connection(r"{path}".format(path=path))

@app.route("/listevents", methods=['GET'])
def listevents():
    # Initiate DB connection
    db  = dbutil()
    # request.method
    # Validate query params
    try:
	    req_validation = [
            request.args['fromDate'],
            request.args['toDate']
        ]
    except Exception as ex:
        logging.error(str(ex))
        raise BadRequest('Bad Request: Either fromDate or toDate is not provided', 40001, { 'ext': str(ex) })
    

    try:
        # retrieve the sql statement from config
        cmd = App_Conf().config()['q_bydate'] 
        cmd = cmd.format(toDate=request.args['toDate'], fromDate=request.args['fromDate'])

        # Invoke DB command
        logging.info('Initiating DB connection')
        conn = getattr(g, 'db', None)
        if conn is not None:
            rows = db.exec(conn, cmd)

    except Exception as ex:
        logging.error(str(ex))
        return make_error(400,  str(ex))

    return jsonify(rows)


@app.route("/listevents/<engineer>")
def listeventsbyengineer(engineer):
    # Initiate DB connection
    db  = dbutil()

    try:
        # retrieve the sql statement from config
        cmd = App_Conf().config()['q_byeng'] 
        cmd = cmd.format(engineer=engineer)

        # Invoke DB command
        logging.info('Initiating DB connection')
        conn = getattr(g, 'db', None)
        if conn is not None:
            rows = db.exec(conn, cmd)

    except Exception as ex:
        logging.error(str(ex))
        return make_error(400,  str(ex))

    return jsonify(rows)


@app.route('/summaryevents', defaults={'date': None})
@app.route("/summaryevents/<date>")
def summaryevents(date):
    # Initiate DB connection
    db  = dbutil()

    try:
        # retrieve the sql statement from config
        cmd = App_Conf().config()['q_sumary_daily'] 
        if date is not None:
            cmd = cmd + "WHERE f.fmdate = '{Date}'".format(Date=date)

        # Invoke DB command
        logging.info('Initiating DB connection')
        conn = getattr(g, 'db', None)
        if conn is not None:
            rows = db.exec(conn, cmd)

    except Exception as ex:
        logging.error(str(ex))
        return make_error(400,  str(ex))

    return jsonify(rows)


@app.route("/listevents/getengineers")
def listallengineer():
    # Initiate DB connection
    db  = dbutil()

    try:
        # retrieve the sql statement from config
        cmd = App_Conf().config()['q_listalleng'] 
        logging.info(cmd)
        # Invoke DB command
        logging.info('Initiating DB connection')
        conn = getattr(g, 'db', None)
        if conn is not None:
            rows = db.exec(conn, cmd)

    except Exception as ex:
        logging.error(str(ex))
        return make_error(400,  str(ex))

    return jsonify(rows)


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400


# To add some structured error handling
def make_error(status_code, message):
    resp = jsonify({
        'status': status_code,
        'message': message
    })
    resp.status_code = status_code
    return resp

