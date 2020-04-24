from flask import request, jsonify, Response, redirect, flash, render_template, Blueprint
from flask_wtf import FlaskForm

from UserChoicesDb import User
from forms import preferences
from settings import app

bp = Blueprint(__name__, 'bp')

app.config['SECRET_KEY'] = 'meow'

"""
Default values for the following pages: 
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
_theme = "none"

""" 
Home. Redirects to Personalize home
"""


@bp.route('/')
def helloWorld():
    return redirect('/personalize/')


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
    # for n in range(length):
    #     print(nameslist[n])
    return render_template('base.html',
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           theme=_theme,
                           namelist=nameslist,
                           length=length)


"""
Users page with their preferences loaded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>')
def get_users(name):  # get users choices and page
    return_value = User.get_user(name)
    form = preferences()
    print(return_value)
    return render_template('usersPage.html',
                           form=form,
                           name=name,
                           backgroundColor=return_value['backgroundColor'],
                           textColor=return_value['textColor'],
                           buttonColor=return_value['buttonColor'],
                           font=return_value['font'],
                           theme=return_value['theme'])


"""
Create user page
~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/create', methods=['GET'])
def load_create_user():
    form = preferences()
    return render_template('create.html',
                           form=form,
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           theme=_theme)


@bp.route('/personalize/create', methods=['POST'])
def create_user():  # make new user
    form = preferences(request.form)
    if request.method == 'POST' and form.validate():
        print(request)
        request_headers = request.headers
        print(request_headers)
        request_data = request.get_json()
        # jsonify(request_data)
        print(request_data)
        User.add_user(request_data['name'], request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'], request_data['theme'])
        response = Response("", 201, mimetype='application/json')
        response.headers['location'] = "/personalize/" + str(request_data['name'])
        flash('saved')
        return response, redirect("/personalize/" + str(request_data['name']))
    else:
        return render_template('usersPage.html',
                               form=form,
                               name=_name,
                               backgroundColor=_backgroundColor,
                               textColor=_textColor,
                               buttonColor=_buttonColor,
                               font=_font,
                               theme=_theme)


"""
Users page, put request. Replaces all fields. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>', methods=['PUT'])
def replace_user(name):  # replace user choices
    request_data = request.get_json()
    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
    return response, render_template('usersPage.html',
                                     name=_name,
                                     backgroundColor=_backgroundColor,
                                     textColor=_textColor,
                                     buttonColor=_buttonColor,
                                     font=_font,
                                     theme=_theme)


"""
Users page, patch request. Updates user choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>', methods=['PATCH'])
def update_user(name):  # update user choices
    request_data = request.get_json()
    if 'name' in request_data:
        User.update_user_name(name, request_data['name'])
    if 'backgroundColor' in request_data:
        User.update_user_backgroundColor(name, request_data['backgroundColor'])
    if 'textColor' in request_data:
        User.update_user_textColor(name, request_data['textColor'])
    if 'buttonColor' in request_data:
        User.update_user_buttonColor(name, request_data['buttonColor'])
    if 'font' in request_data:
        User.update_user_font(name, request_data['font'])
    if 'theme' in request_data:
        User.update_user_theme(name, request_data['theme'])

    response = Response("", status=204)
    response.headers['Location'] = "/personalize/" + str(name)
    flash('saved')
    return response, render_template('usersPage.html',
                                     name=_name,
                                     backgroundColor=_backgroundColor,
                                     textColor=_textColor,
                                     buttonColor=_buttonColor,
                                     font=_font,
                                     theme=_theme)


"""
Users page, delete request. Removes user from database.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@bp.route('/personalize/<string:name>', methods=['DELETE'])
def delete_user(name):
    if User.delete_user(name):
        response = Response("", 201, mimetype='application/json')
        response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
        return response, render_template('base.html',
                                         name=_name,
                                         backgroundColor=_backgroundColor,
                                         textColor=_textColor,
                                         buttonColor=_buttonColor,
                                         font=_font,
                                         theme=_theme)
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
                                         font=_font,
                                         theme=_theme)


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
    return render_template('404.html'), 404


app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(port=80, debug=True)
