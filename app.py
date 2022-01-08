# -*- coding: utf-8 -*-
import gzip

from flask import Flask, render_template, json, request
from flask_cors import CORS
from library.functions import pathDB, Settings, work_with_backup, get_fun
from multiprocessing import process
import os
import re
import time

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

pdb = pathDB(r"D:\backup")


@app.route("/getTables/<string:name_backup>/<string:item>/")
def getTables(name_backup, item):
    print(name_backup, item)

    tablr = []
    selected_backup = pdb.path + "\\" + name_backup

    if item == 'tables':
        pattern = r"-- Table structure for table\ \`([\w\d_-]*)\`"
    elif item == 'views':
        pattern = r"-- Temporary table structure for view\ \`([\w\d_-]*)\`"
    else:
        return app.response_class(
            response=json.dumps({'text': "Не правильнный параметр"}),
            status=200,
            mimetype='application/json'
        )

    with gzip.open(selected_backup, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if len(re.findall(pattern, line)) != 0:
                tablr.append(re.findall(pattern, line)[0])

    if len(tablr) == 0:
        return app.response_class(
            response=json.dumps({'text': "Пусто"}),
            status=200,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response=json.dumps(tablr),
            status=200,
            mimetype='application/json'
        )


@app.route("/get_date_exists_backup")
def get_data_exists_backup():
    response = app.response_class(
        response=json.dumps(pdb.get_json_by_date()),
        status=200,
        mimetype='application/json'
    )
    return response


# main
if __name__ == "__main__":
    # f = pathDB(r"D:\backup")
    # print(f.getFileInDirectory())
    app.run(debug=True)
