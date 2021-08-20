# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request
import model
import json

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cost')
def cost_page():
    uid = request.args.get("uid","")
    result = model.sum_unblendedcost(uid)
    return render_template('cost.html', data = result)

if __name__ == '__main__':
    app.run()