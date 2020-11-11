#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Drawon
# Time:2020/11/6 17:08
# Version:python 3.7.6
import json
import logging
from flask import Flask, request, make_response
from flasgger import Swagger,swag_from
from ELE_FORE import valueForecast


app = Flask(__name__)
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
Swagger(app,config=swagger_config)
@app.route('/api/valueFore/', methods=['POST'])
@swag_from('valueFore.yml')
def forecastValue():
    try:
        if "file" not in request.files:
            return "No FILE"
        filebytes = request.files["file"]
        value =  valueForecast(filebytes).to_json()
    except Exception as e:
        logging.exception('出现错误',exc_info=e)
        return status('',str(e),500)
    else:
        return status(value)


def status(data, exc='', status=200):
    try:
        return json.dumps({"code": status, "data": data, "message": exc}, ensure_ascii=False)
    except Exception :
        return json.dumps({"code": 500, "data": {}, "message": exc}, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5100,debug=True)