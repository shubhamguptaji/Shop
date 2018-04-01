from flask import Flask, render_template, request, redirect,  url_for, flash, jsonify

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, User, Items

from flask import session as login_session

import random, string

from oauth2client.client import flow_from_clientsecrets

from oauth2client.client import FlowExchangeError

import httplib2

import json

from flask import make_response

import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open(
 	'client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///shopdata.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def login():
	if 'username' not in login_session:
		state = ''.join(random.choice(string.ascii_uppercase + string.digits)
						for x in xrange(32))
		login_session['state'] = state
		print state
		return render_template('login.html', STATE=state)
	else:
		flash("Already logged In!")
		return redirect(url_for('categories'))

# google id connection
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '''
    <div class="content">
    <div class="row">
        <div class="col-md-12">
            <h1>Welcome '''
    output += login_session['username']
    output += '''
    !!</h1>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <img style = "width: 200px; height: \
200px;border-radius: 100px;-webkit-border-radius: \
100px;-moz-border-radius: 100px;" src="'''
    output += login_session['picture']
    output += '''">
        </div>
    </div>
</div>
    '''
    flash("You are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
# This method is to add a new user to the database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# This method is to get the information of a registered user from the database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# This method returns user_id
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# logging out handler
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in.")
    return redirect(url_for('categories'))



@app.route('/categories/<int:categories_id>/items/JSON')
def categoriesItemJson(categories_id):
	category = session.query(Categories).filter_by(id=categories_id).one()
	items = session.query(Items).filter_by(categories_id=categories_id).all()
	return jsonify(Items=[i.serialize for i in items])

@app.route('/categories/<int:categories_id>/items/<int:items_id>/JSON')
def ItemsJSON(categories_id,items_id):
	item = session.query(Items).filter_by(id=categories_id).one()
	return jsonify(item=item.serialize)

@app.route('/categories/JSON')
def categoriesJSON():
	categories = session.query(Categories).all()
	return jsonify(categories=[c.serialize for c in categories])




@app.route('/')
@app.route('/categories')
def categories():
	categories = session.query(Categories).all()
	return render_template('Categories.html', categories=categories)




@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
	if 'email' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCategory = Categories(name=request.form['name'], image=request.form['image'])
		session.add(newCategory)
		flash('New Category %s Successfully Created' % newCategory.name)
		session.commit()
		return redirect(url_for('categories'))
	else:
		return render_template('newCategory.html')


@app.route('/categories/<int:categories_id>/edit', methods=['GET', 'POST'])
def editCategory(categories_id):
    if 'email' not in login_session:
        return redirect('/login')
    editedcategory = session.query(Categories).filter_by(id = categories_id).one()
    if request.method == 'POST':
        editedcategory.name = request.form['name']
        editedcategory.image = request.form['image']
        session.add(editedcategory)
        flash('%s Successfully Updated' % editedcategory.name)
        session.commit()
        return redirect('categories')
    else:
        return render_template('editCategory.html',categories_id=categories_id, category=editedcategory)


@app.route('/categories/<int:categories_id>/delete', methods=['GET', 'POST'])
def deleteCategory(categories_id):
	if 'email' not in login_session:
		return redirect('/login')
	category = session.query(Categories).filter_by(id = categories_id).one()
	if request.method == 'POST':
		session.delete(category)
		flash('%s Successfully Deleted' % category.name)
		session.commit()
		return redirect(url_for('categories', categories_id=categories_id))
	else:
		return render_template('deleteCategory.html', category=category)


@app.route("/categories/<int:categories_id>/")
@app.route("/categories/<int:categories_id>/items/")
def showItem(categories_id):
    if 'email' not in login_session:
        return redirect('login')
    else:
        category = session.query(Categories).filter_by(id = categories_id).one()
        items = session.query(Items).filter_by(categories_id = categories_id).all()
        return render_template('showItem.html', items=items, category=category, username=login_session['username'])


@app.route('/categories/<int:categories_id>/items/<int:items_id>/edit', methods=['GET', 'POST'])
def editItem(categories_id, items_id):
    if 'email' not in login_session:
        return redirect('/login')
    category = session.query(Categories).filter_by(id=categories_id).one()
    editeditem = session.query(Items).filter_by(id=items_id).one()
    if request.method == 'POST':
        editeditem.name = request.form['name']
        editeditem.price = request.form['price']
        editeditem.description = request.form['description']
        editeditem.image = request.form['image']
        editeditem.seller_name = request.form['seller_name']
        editeditem.seller_address = request.form['seller_address']
        editeditem.seller_phoneno = request.form['seller_phoneno']
        session.add(editeditem)
        flash("Item successfully Updated!")
        session.commit()
        return redirect(url_for('showItem', categories_id=category.id))
    else:
        return render_template('editItem.html', categories_id=category.id, items_id=items_id, item=editeditem)
'''@app.route("/categories/<int:categories_id>/items/<int:items_id>/edit", methods=['GET', 'POST'])
def editItem(categories_id, items_id):
	category = session.query(Categories).filter_by(id = categories_id).one()
	editeditem = session.query(Items).filter_by(id = items_id).one()
	if 'email' not in login_session:
		return redirect("/login")
	if request.method == 'POST':
        editeditem.name = request.form['name']
		editeditem.price = request.form['price']
		editeditem.description = request.form['description']
		editeditem.image = request.form['image']
		editeditem.seller_name = request.form['seller_name']
		editeditem.seller_address = request.form['seller_address']
		editeditem.seller_phoneno = request.form['seller_phoneno']
		session.add(editeditem)
		flash('Item Successfully Edited!')
        session.commit()
		return redirect(url_for('showItem', categories_id=category.id))
	else:
		return render_template('editItem.html', categories_id=category.id, items_id=items_id, item=editeditem)'''


@app.route("/categories/<int:categories_id>/items/<int:items_id>/delete", methods=['GET', 'POST'])
def deleteItem(categories_id, items_id):
	if 'email' not in login_session:
		return redirect('/login')
	category = session.query(Categories).filter_by(id = categories_id).one()
	item = session.query(Items).filter_by(id = items_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('Item Successfully Deleted!')
		return redirect(url_for('showItem', categories_id=categories_id))
	else:
		return render_template('deleteItem.html', item=item)





@app.route("/categories/<int:categories_id>/items/new", methods=['GET', 'POST'])
def newItem(categories_id):
	if 'email' not in login_session:
		return redirect('login')
	category = session.query(Categories).filter_by(id = categories_id).one()
	if request.method == 'POST':
		newitem = Items(name=request.form['name'], description=request.form['description'], price=request.form['price'], seller_name=request.form['seller_name'], seller_address=request.form['seller_address'], seller_phoneno=request.form['seller_phoneno'], image=request.form['image'], categories_id=categories_id)
		session.add(newitem)
		session.commit()
		flash('New Item %s Successfully Added' % (newitem.name))
		return redirect(url_for('showItem', categories_id=categories_id))
	else:
		return render_template('newItem.html', categories_id=categories_id)




if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
