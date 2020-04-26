from flask import request, jsonify, Response, redirect, flash, render_template, Blueprint
from flask_wtf import FlaskForm
from logging.config import dictConfig
from UserChoicesDb import User
from forms import preferences
from settings import app

bp = Blueprint(__name__, 'bp')

app.config['SECRET_KEY'] = 'meow'

"""
These are the default values for the following pages: 
'/personalize/'
'/personalize/create'
'/personalize/delete' 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

_name = "Default"
_backgroundColor = "white"
_textColor = "black"
_buttonColor = "white"
_font = "italic"

""" 
Home. Redirects to Personalize home
"""


@bp.route('/')
def helloWorld():
    return "hello world"


"""
A json page showing all users in the database. 
Not linked on page.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/allusers')
def getAllUsers():
    print({'users': User.get_all_users()})
    return jsonify({'users': User.get_all_users()})


"""
Personalize Home
~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/')
def home():
    nameslist = User.get_all_users_names()
    length = len(nameslist)
    return render_template('base.html',
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           namelist=nameslist,
                           length=length,
                           navnames=nameslist)


"""
Users page with their preferences loaded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>')
def get_users(name):  # get users choices and page
    nameslist = User.get_all_users_names()
    if name not in nameslist:
        return page_not_found('user not year created')
    return_value = User.get_user(name)
    form = preferences()
    return render_template('usersPage.html',
                           form=form,
                           name=name,
                           backgroundColor=return_value['backgroundColor'],
                           textColor=return_value['textColor'],
                           buttonColor=return_value['buttonColor'],
                           font=return_value['font'])


"""
Create user page
~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/create', methods=['GET', 'POST'])
def create_user():  # make new user
    form = preferences(request.form)
    request_data = request.form.to_dict()
    if request.method == 'POST':
        request_headers = request.headers
        print(request_headers)
        request_data = request.form.to_dict()
        # print(request_data)

        User.add_user(request_data['name'],
                      request_data['backgroundColor'],
                      request_data['textColor'],
                      request_data['buttonColor'],
                      request_data['font'])
        # response = Response("", 201, mimetype='application/json')
        # response.headers['location'] = "/personalize/" + str(request_data['name'])
        flash('saved')
        return redirect("/personalize/" + str(request_data['name']))
    return render_template('usersPage.html',
                           form=form,
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font)


"""
Users page, put request. Replaces all fields. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>', methods=['POST'])
def methods(name):
    form = preferences(request.form)
    request_data = request.form.to_dict()
    delete = request_data['delete']
    if delete == 'Yes, Delete Me':
        print(request)
        return delete_user(name)
    else:
        method = request_data['method']
        if method == 'put':
            return replace_user(name)
        elif method == 'patch':
            return update_user(name)
        elif method == 'post':
            return create_user()
        else:
            flash('try again')
            return redirect('/personalize/' + str(name))


# @bp.route('/personalize/<string:name>', methods=['PUT'])
@bp.route('/personalize/<string:name>', methods=['POST'])
def replace_user(name):  # replace user choices
    form = preferences(request.form)
    request_data = request.form.to_dict()

    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'])
    # response = Response("", 201, mimetype='application/json')
    # response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
    # return redirect("/personalize/" + str(request_data['name']))
    return render_template('usersPage.html',
                           form=form,
                           name=name,
                           backgroundColor=request_data['backgroundColor'],
                           textColor=request_data['textColor'],
                           buttonColor=request_data['buttonColor'],
                           font=request_data['font'])


@bp.route('/personalize/<string:user>/<string:url>', methods=['GET'])
def geturl(name, url):
    pass




"""
Users page, patch request. Updates user choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# @bp.route('/personalize/<string:name>', methods=['PATCH'])
@bp.route('/personalize/<string:name>', methods=['POST'])
def update_user(name):  # update user choices
    form = preferences(request.form)
    request_data = request.form.to_dict()
    # request_data = request.get_json()
    uinput = request_data['name']
    if uinput != '':
        User.update_user_name(name, request_data['name'])

    uinput = request_data['backgroundColor']
    if uinput != '':
        User.update_user_backgroundColor(name, request_data['backgroundColor'])

    uinput = request_data['textColor']
    if uinput != '':
        User.update_user_textColor(name, request_data['textColor'])

    uinput = request_data['buttonColor']
    if uinput != '':
        User.update_user_buttonColor(name, request_data['buttonColor'])

    uinput = request_data['font']
    if uinput != '':
        User.update_user_font(name, request_data['font'])


    flash('saved')
    return render_template('usersPage.html',
                           form=form,
                           name=request_data['name'],
                           backgroundColor=request_data['backgroundColor'],
                           textColor=request_data['textColor'],
                           buttonColor=request_data['buttonColor'],
                           font=request_data['font'])


"""
Users page, delete request. Removes user from database.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# @bp.route('/personalize/<string:name>', methods=['DELETE'])
@bp.route('/personalize/<string:name>', methods=['POST'])
def delete_user(name):
    if User.delete_user(name):
        # response = Response("", 201, mimetype='application/json')
        # response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
        return render_template('base.html',
                                         name=_name,
                                         backgroundColor=_backgroundColor,
                                         textColor=_textColor,
                                         buttonColor=_buttonColor,
                                         font=_font)
    else:
        errormessage = {
            "error": "error, could not delete choices"
        }
        response = Response(errormessage, status=400, mimetype='application/json')
        return response, render_template('base.html',
                                         name=_name,
                                         backgroundColor=_backgroundColor,
                                         textColor=_textColor,
                                         buttonColor=_buttonColor,
                                         font=_font)


"""
Gets all users, gets all names from those users, 
and returns a list of the names.
For use in the nav bar item 'Find Me' 
which shows a link to every user in the database's page.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def getAllUsersNames():
    namelist = User.get_all_users_names()
    print(namelist)
    return namelist


# print(jsonify(User.get_all_users_names()))
# allNames = jsonify(User.get_all_users_names())
# listOfNames = []
# for name in allNames:
#     oneName = allNames[name]
#     print(oneName)
#     listOfNames.append(oneName)
# print(listOfNames)

# return jsonify(User.get_all_users_names())


"""
Error Handling 
~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    flash(error)
    return render_template('404.html'), 404


app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(port=80, debug=True)
