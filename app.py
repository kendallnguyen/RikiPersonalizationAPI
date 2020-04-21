from flask import request, jsonify, Response, redirect, flash, render_template
from UserChoicesDb import User
from settings import app

app.config['SECRET_KEY'] = 'meow'


@app.route('/')  # works
def helloWorld():
    return "Hello, world. Go to this webpage /personalize/"


def getDefaultUser():
    name = "default"
    return User.get_user(name)


@app.route('/personalize/allusers')  # works
def getAllUsers():
    print({'users': User.get_all_users()})
    return jsonify({'users': User.get_all_users()})


@app.route('/personalize/')
def home():
    # getAllUsersNames()
    return personalize("default")


@app.route('/personalize/<string:name>')
def get_users(name):  # get users choices
    return_value = User.get_user(name)
    print(return_value)
    return personalize(return_value)


@app.route('/personalize/create')
def load_create_page():
    return personalize("create")


@app.route('/personalize/create', methods=['POST'])
def create_user():  # make new user
    request_data = request.get_json()
    print(request_data)
    User.add_user(request_data['name'], request_data['backgroundColor'],
                  request_data['textColor'], request_data['buttonColor'],
                  request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(request_data['name'])
    flash('saved')
    return response, personalize(request_data),  # redirect(
    # "/personalize/" + str(request_data['name']))  # , personalize(getDefaultUser())


@app.route('/personalize/<string:name>', methods=['PUT'])
def replace_user(name):  # replace user choices
    request_data = request.get_json()
    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
    return response, personalize(request_data)


@app.route('/personalize/<string:name>', methods=['PATCH'])
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
    return response, personalize("patch")


@app.route('/personalize/<string:name>', methods=['DELETE'])
def delete_user(name):
    if User.delete_user(name):
        response = Response("", 201, mimetype='application/json')
        response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
        return response, personalize("default")
    else:
        errormessage = {
            "error": "error, could not delete choices"
        }
        response = Response(errormessage, status=400, mimetype='application/json')
        return response, personalize("default")


def personalize(data):
    if data == "create":  # create user
        _name = "Default"
        _backgroundColor = "white"
        _textColor = "black"
        _buttonColor = "white"
        _font = "italic"
        _theme = "none"
        return render_template('personalizeCreate.html',
                               name=_name,
                               backgroundColor=_backgroundColor,
                               textColor=_textColor,
                               buttonColor=_buttonColor,
                               font=_font,
                               theme=_theme)
    elif data == "default" or "delete":  # no user chosen yet, delete user
        _name = "Default"
        _backgroundColor = "white"
        _textColor = "black"
        _buttonColor = "white"
        _font = "italic"
        _theme = "none"
        return render_template('personalize.html',
                               name=_name,
                               backgroundColor=_backgroundColor,
                               textColor=_textColor,
                               buttonColor=_buttonColor,
                               font=_font,
                               theme=_theme)
    elif data == "patch":  # update user, replace user
        return render_template('personalizeCreate.html')

    # the rest of the options. put, post, patch
    else:
        print(data)
        print(data['name'])
        _name = data['name']
        _backgroundColor = data['backgroundColor']
        _textColor = data['textColor']
        _buttonColor = data['buttonColor']
        _font = data['font']
        _theme = data['theme']
        return render_template('personalize.html',
                               name=_name,
                               backgroundColor=_backgroundColor,
                               textColor=_textColor,
                               buttonColor=_buttonColor,
                               font=_font,
                               theme=_theme)


def getAllUsersNames():
    print(getAllUsers)

    # print(jsonify(User.get_all_users_names()))
    # allNames = jsonify(User.get_all_users_names())
    # listOfNames = []
    # for name in allNames:
    #     oneName = allNames[name]
    #     print(oneName)
    #     listOfNames.append(oneName)
    # print(listOfNames)

    # return jsonify(User.get_all_users_names())


""" Error Handling 
    ~~~~~~~~~~~~~~
"""


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=80, debug=True)
