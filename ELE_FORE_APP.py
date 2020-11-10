#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Drawon
# Time:2020/11/6 17:08
# Version:python 3.7.6


import logging
from flask import Flask, request, abort, make_response
from flasgger import Swagger,swag_from
from EleForeApp.ele_forecast import valueForecast


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
@app.route('/api/valueFore/', methods=['POST','GET'])
@swag_from('valueFore.yml')
def forecastValue():
    try:
        if "file" not in request.files:
            return "No FILE"
        filebytes = request.files["file"]
        print('执行前',filebytes)
        value =  valueForecast(filebytes).to_dict()
    except Exception as e:
        logging.exception('出现错误',exc_info=e)
        return make_response('异常')
    else:
        return value

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5100,debug=True)