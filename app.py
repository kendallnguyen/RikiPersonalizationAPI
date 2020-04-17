from flask import request, jsonify, Response, redirect, flash, render_template
from UserChoicesDb import User
from settings import app


@app.route('/')  # works
def helloWorld():
    return "Hello, world"


@app.route('/personalize/')  # works
def getAllUsers():
    return jsonify({'users': User.get_all_users()})


@app.route('/personalize/<string:name>')  # works
def get_users(name):  # get users choices
    return_value = User.get_user(name)
    personalize(return_value)
    return jsonify(return_value)


@app.route('/personalize/', methods=['POST'])  # works
def create_user():  # make new user
    request_data = request.get_json()
    User.add_user(request_data['name'], request_data['backgroundColor'],
                  request_data['textColor'], request_data['buttonColor'],
                  request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(request_data['name'])
    flash('saved')
    return response, redirect("/personalize/" + str(request_data['name']))


@app.route('/personalize/<string:name>', methods=['PUT'])  # works
def replace_user(name):  # replace user choices
    request_data = request.get_json()
    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
    return response


@app.route('/personalize/<string:name>', methods=['PATCH'])  # works
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
    response.headers['Location'] = "/personalization/" + str(name)
    flash('saved')
    return response


@app.route('/personalize/<string:name>', methods=['DELETE'])  # works
def delete_user(name):
    if User.delete_user(name):
        response = Response("", 201, mimetype='application/json')
        response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
        return response
    else:
        errormessage = {
            "error": "error, could not delete choices"
        }
        response = Response(errormessage, status=400, mimetype='application/json')
        return response


@app.route('/personalize/')
def personalize(data):
    print(data)
    _name = data['name']
    _backgroundColor = data['backgroundColor']
    _textColor = data['textColor']
    _buttonColor = data['buttonColor']
    _font = data['font']
    _theme = data['theme']
    # FIX_ME
    return render_template('personalize.html',
                           name=_name,
                           backgroundColor=_backgroundColor,
                           textColor=_textColor,
                           buttonColor=_buttonColor,
                           font=_font,
                           theme=_theme)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=80, debug=True)
