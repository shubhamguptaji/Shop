from flask import Flask, render_template, request, redirect,  url_for, flash, jsonify

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Users, Item

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

engine = create_engine('postgresql://guptaji:shop@localhost/shopdata')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# LOGIN
@app.route('/login')
def login():
    if 'username' not in login_session:
        state = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    else:
        flash("Already Logged In")
        return redirect(url_for('categories'))


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


# facebook oauth
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
   

    app_id = "173697696588493"
    app_secret = "74b5c20437cc0f066303c859b43cfecc"
    url = '''https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s''' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.11/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.11/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.11/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "You have been logged out"


# logging out handler
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        elif login_session['provider'] == 'facebook':
            fbdisconnect()
        del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in.")
    return redirect(url_for('categories'))



@app.route('/categories/<int:categories_id>/items/JSON')
def categoriesItemJson(categories_id):
    category = session.query(Category).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(categories_id=categories_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/categories/<int:categories_id>/items/<int:items_id>/JSON')
def ItemsJSON(categories_id,items_id):
    item = session.query(Item).filter_by(id=categories_id).one()
    return jsonify(item=item.serialize)

@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])




@app.route('/')
@app.route('/categories')
def categories():
    categories = session.query(Category).all()
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
    editedcategory = session.query(Category).filter_by(id = categories_id).one()
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
    category = session.query(Category).filter_by(id = categories_id).one()
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
        category = session.query(Category).filter_by(id = categories_id).one()
        items = session.query(Item).filter_by(categories_id = categories_id).all()
        return render_template('showItem.html', items=items, category=category, username=login_session['username'])


@app.route('/categories/<int:categories_id>/items/<int:items_id>/edit', methods=['GET', 'POST'])
def editItem(categories_id, items_id):
    if 'email' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=categories_id).one()
    editeditem = session.query(Item).filter_by(id=items_id).one()
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
    category = session.query(Category).filter_by(id = categories_id).one()
    item = session.query(Item).filter_by(id = items_id).one()
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
    category = session.query(Category).filter_by(id = categories_id).one()
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
