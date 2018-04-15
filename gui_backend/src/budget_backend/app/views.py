import datetime
import os
import logging
import time
from app import app
from flask import render_template, request, send_file
from excel_budget import budgetsheet


BUDGET_SHEET_PATH = os.path.join(os.getcwd(), 'data', 'test.xlsx')


def is_date_time(element):
    """return boolean for whether or not element is of type
    datetime.datetime
    """
    return isinstance(element, datetime.datetime)


def update_budget(path):
    """return a new instance of BudgetSheet at the given path"""
    file_path = os.path.join(os.getcwd(), path)
    logging.info("reading budget data from {}".format(file_path))
    return budgetsheet.BudgetSheet(file_path)


@app.route('/')
@app.route('/index')
def index():
    budget = update_budget(BUDGET_SHEET_PATH)
    return render_template('index.html',
                           budget=budget,
                           is_date_time=is_date_time,
                           strftime=time.strftime)


@app.route('/result', methods=['POST', 'GET'])
def result():
    budget = update_budget(BUDGET_SHEET_PATH)
    if request.method == 'POST':
        date = str(request.form.get('date'))
        budget.write_budget_cell(date,
                                 request.form.get('category'),
                                 request.form.get('data'))
    return render_template('index.html',
                           budget=budget,
                           is_date_time=is_date_time,
                           strftime=time.strftime)


@app.route('/category', methods=['POST', 'GET'])
def category():
    budget = update_budget(BUDGET_SHEET_PATH)
    if request.method == 'POST':
        budget.add_category(request.form.get('category'))
    return render_template('index.html',
                           budget=budget,
                           is_date_time=is_date_time,
                           strftime=time.strftime)


@app.route('/api/data/<string:file_name>', methods=['GET'])
def getFile(file_name):
    return send_file(os.path.join(os.getcwd(), 'data', file_name))
