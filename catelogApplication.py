#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']  # noqa
APPLICATION_NAME = 'Item catelog'

engine = create_engine('sqlite:///itemCatelog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token

@app.route('/login')
def showLogin():
    if 'username' in login_session:
        return redirect('/')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))  # noqa
    login_session['state'] = state

    # return "The current session state is %s" % login_session['state']

    return render_template('loginpage.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)  # noqa
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    print 'done!'
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))   # noqa
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/categories/<int:category_id>/item/JSON')
def itemCatelogJSON(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE

@app.route('/categories/<int:category_id>/item/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Items).filter_by(id=menu_id).one()
    return jsonify(Items=Items.serialize)


# Show all categories

@app.route('/')
@app.route('/categories/')
def showCategories():
    if 'username' in login_session:
        flash('Hi %s !' % login_session['username'])
    categories = session.query(Categories).order_by(Categories.name)
    return render_template('categories.html', categories=categories)


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/item')
def itemCatelog(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=category_id).all()
    if 'username' in login_session:
        flash('Hi %s !' % login_session['username'])
        return render_template('item.html', category=category,
                               items=items, category_id=category_id)
    else:
        return render_template('showitem.html', category=category,
                               items=items, category_id=category_id)

# Task 1: Create route for newItem function here


@app.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        flash("Hi %s !" % login_session['username'])
    category = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


# Task 2: Create route for editItem function here

@app.route('/categories/<int:category_id>/item/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        flash('Hi %s !' % login_session['username'])
    editItem = session.query(Items).filter_by(id=item_id).one()
    category = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        session.add(editItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))
    else:
        return render_template('editItem.html',
                               category_id=category_id,
                               item_id=item_id, item=editItem)


# Task 3: Create a route for deleteItem function here

@app.route('/categories/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        flash('Hi %s !' % login_session['username'])
    deleteItem = session.query(Items).filter_by(id=item_id).one()
    category = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('itemCatelog', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=deleteItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
