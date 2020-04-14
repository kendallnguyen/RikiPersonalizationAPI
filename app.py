from flask import Flask, request, jsonify, Response, redirect, flash, render_template
from settings import *
from UserChoicesDb import User
import json
# from Riki import *
users = User.get_all_users()


@app.route('/')  # works
def helloWorld():
    return "Hello world"


@app.route('/personalize/')   # works
def getAllUsers():
#    render_template('personalize.html', users=users)
    return jsonify({'users': User.get_all_users()})


@app.route('/personalize/<string:name>')  # works
def get_users(name):  # get users choices
    return_value = User.get_user(name)
#    render_template('personalize.html')
    return jsonify(return_value)


@app.route('/personalize/', methods=['POST'])   # works
def create_user():  # make new user
    request_data = request.get_json()
    User.add_user(request_data['name'], request_data['backgroundColor'],
                  request_data['textColor'], request_data['buttonColor'],
                  request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(request_data['name'])
    flash('saved')
#    render_template('personalize.html')
    return response, redirect("/personalize/" + str(request_data['name']))


@app.route('/personalize/<string:name>', methods=['PUT'])   # works
def replace_user(name):  # replace user choices
    request_data = request.get_json()
    User.replace_user(name, request_data['backgroundColor'],
                      request_data['textColor'], request_data['buttonColor'],
                      request_data['font'], request_data['theme'])
    response = Response("", 201, mimetype='application/json')
    response.headers['location'] = "/personalize/" + str(name)
    flash('saved')
#    render_template('personalize.html')
    return response


@app.route('/personalize/<string:name>', methods=['PATCH'])    # works
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
#    render_template('personalize.html')
    return response


@app.route('/personalize/<string:name>', methods=['DELETE'])   # works
def delete_user(name):
    if User.delete_user(name):
        response = Response("", 201, mimetype='application/json')
        response.headers['location'] = "/personalize/" + str(name)
        flash('deleted')
#        render_template('personalize.html')
        return response
    else:
        errormessage = {
            "error": "error, could not delete choices"
        }
        response = Response(errormessage, status=400, mimetype='application/json')
        return response



if __name__ == '__main__':
    app.run(port=80)
