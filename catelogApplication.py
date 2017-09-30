#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

app = Flask(__name__)


engine = create_engine('sqlite:///itemCatelog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/categories/<int:category_id>/item/JSON')
def itemCatelogJSON(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE
@app.route('/categories/<int:category_id>/item/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Items).filter_by(id=menu_id).one()
    return jsonify(Items=Items.serialize)


#@app.route('/')
@app.route('/categories/<int:category_id>/item')
def itemCatelog(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=category_id)
    return render_template('item.html', category=category, items=items, category_id=category_id)

# Task 1: Create route for newItem function here

@app.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Items(name=request.form['name'], description=request.form['description'], category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))  
    else:
        return render_template('newItem.html', category_id=category_id)

# Task 2: Create route for editItem function here


@app.route('/categories/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editItem = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.name = request.form['description']
        session.add(editItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))
    else:
        return render_template(
            'editItem.html', category_id=category_id, item_id=item_id, item=editItem)

# Task 3: Create a route for deleteItem function here


@app.route('/categories/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    deleteItem = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=deleteItem)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
