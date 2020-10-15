import os
import peeweedbevolve # new; must be imported before models
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Store # new line

app = Flask(__name__)
app.secret_key= os.urandom(16)

@app.before_request # new line
def before_request():
   db.connect()

@app.after_request # new line
def after_request(response):
    db.close()
    return response

@app.cli.command() # new
def migrate(): # new 
    db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/store", methods=['GET'])
def store_new():
    return render_template('store.html')

@app.route("/store/", methods=['POST'])
def store_create():
    store_name = request.form.get('store_name')
    store = Store(name=store_name)
    if store.save(): 
        flash("Store created!", "success")
        return redirect(url_for('store_new'))

if __name__ == '__main__':
   app.run()