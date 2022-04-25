import ast
import pymysql
from flask import *
import re
import numpy as np
import datetime
from datetime import date
import asyncio


#////////// config
SECRET_KEY = 'dsvrsgkvergwerfercdgrwhjhrgregtwrhkokokojwfoeowg'
host = "maxonbtc.beget.tech"
user = "maxonbtc_test"
password = "cagnN%9n"
db_name = "maxonbtc_test"


app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(__name__)


@app.route('/')
def main():
    return render_template('index.html')
     

@app.route('/table',methods=["POST", "GET"])
def table():
    if request.method == 'POST':
        timeStart = datetime.datetime.now()
        prime = deapazonCheck(int(request.form['startD']), int(request.form['endD']))
        processTime = str(datetime.datetime.now() - timeStart)
        makeNote(date.today(), 'Python Flask', request.form['startD'], request.form['endD'], prime, processTime)
        return render_template('table.html', data = getNote())
    return render_template('table.html', data = getNote())

@app.route('/clean')
def clean():
    cleanData()
    return render_template('table.html', data = getNote())

def getNote():
    try:
        connection = pymysql.connect(host=host, port=3306, user=user, password=password, database=db_name,cursorclass=pymysql.cursors.DictCursor)
        print('Succses!')
        try:
            with connection.cursor() as cursor:
                create_table_query = "select * from bakalavratest"
                cursor.execute(create_table_query)
                rows = cursor.fetchall()
        finally:
            connection.close()
    except Exception as ex:
        print('Ereror')
        print(ex)
    return rows

def isPrime(num):
    for x in range(2, num):
        if num % x == 0:
            return False
    return num > 1

def deapazonCheck(startNum, endNum):
    primeNumCol = 0
    for x in range(startNum, endNum + 1):
        if isPrime(x): 
            primeNumCol = primeNumCol + 1
    return primeNumCol

def makeNote(date, stack, start, end, num, time):
    try:
        connection = pymysql.connect(host=host, port=3306, user=user, password=password, database=db_name,cursorclass=pymysql.cursors.DictCursor)
        print('Succses!')
        try:
            with connection.cursor() as cursor:
                create_table_query = f"INSERT INTO `bakalavratest` (`data`, `stack`, `start`, `end`, `num`, `time`) VALUES ('{str(date)}', '{str(stack)}', '{str(start)}', '{str(end)}', '{str(num)}', '{str(time)}');"
                cursor.execute(create_table_query)
                connection.commit() 
        finally:
            connection.close()
    except Exception as ex:
        print('Ereror')
        print(ex)

def cleanData():
    try:
        connection = pymysql.connect(host=host, port=3306, user=user, password=password, database=db_name,cursorclass=pymysql.cursors.DictCursor)
        print('Succses!')
        try:
            with connection.cursor() as cursor:
                create_table_query = f"DELETE FROM `bakalavratest`"
                cursor.execute(create_table_query)
                connection.commit() 
        finally:
            connection.close()
    except Exception as ex:
        print('Ereror')
        print(ex)


if __name__ == '__main__':
    app.run(debug=True)

