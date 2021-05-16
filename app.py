from flask import Flask as flask, jsonify, request as req
import Connection as con
import Route as route
from passlib.hash import pbkdf2_sha256 as sha256
import SqlQuery as query
import random
import string

conn = None;

app = flask(__name__)

@app.route('/')
def index():
    conn = con.Connection()
    return "Server started"

@app.route(route.register, methods=['POST'])
def RegisterTourTracker():
    conn = con.Connection()

    first_name = req.form.get('first_name')
    last_name = req.form.get('last_name')
    email_id = req.form.get('email_id')
    mobile_no = req.form.get('mobile_no')
    gender = req.form.get('gender')
    address = req.form.get('address')
    trusted_person_t_code = 'T-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    created_trips = req.form.get('created_trips')
    joined_trips = req.form.get('joined_trips')
    trusted_person = req.form.get('trusted_person')
    birth_date = req.form.get('birth_date')
    blood_group = req.form.get('blood_group')
    health_problems = req.form.get('health_problems')


    password = req.form.get('password')
    encrypt_password = ""
    if password != None:
        encrypt_password = str(sha256.using(salt_size = 16, rounds =200).hash(password))

    if check_Validation(first_name, last_name, email_id, gender, address, encrypt_password):
        return jsonify({
            'data':[],
            'status': 'failer',
            'message': 'Invalid Data'
        })
    
    data = conn.Insert_tour_people_register(conn.get_Cursor(), first_name, last_name, email_id, mobile_no, gender, address, encrypt_password, trusted_person_t_code, created_trips, joined_trips, trusted_person, birth_date, blood_group, health_problems)
    return jsonify({
        'data':data,
        'status':'Success',
        'message': 'Email id already register' if len(data) ==0 else 'Register successfully'})
    #return jsonify({'record':conn.get_Data(conn.get_Cursor(), query.TOUR_PEOPLE_REGISTER)})
    #return f"Register successfully {first_name} {last_name} {encrypt_password} {email_id}"

@app.route(route.UpdateUserData, methods=['POST'])
def updateUserData():
    conn = con.Connection()
    userid = req.form.get('userid')
    first_name = req.form.get('first_name')
    last_name = req.form.get('last_name')
    mobile_no = req.form.get('mobile_no')
    gender = req.form.get('gender')
    address = req.form.get('address')
    birth_date = req.form.get('birth_date')
    blood_group = req.form.get('blood_group')
    health_problems = req.form.get('health_problems')

    if check_Validation(first_name, last_name, mobile_no, gender, address, birth_date, blood_group, health_problems):
        return jsonify({
            'data':[],
            'status': 'failer',
            'message': 'Invalid Data'
        })
    data = conn.Update_User_Data(conn.get_Cursor(), userid, first_name, last_name, mobile_no, gender, address, birth_date, blood_group, health_problems)
    return jsonify({
        'data':[] if data == 'NOT_FOUND' else data,
        'status': 'failer' if data == 'NOT_FOUND' else 'success',
        'message': 'User Not found' if data == 'NOT_FOUND' else 'Update Successfully'
    })
    #return f"update successfully {userid}"


@app.route(route.login, methods=['POST'])
def login():
    conn = con.Connection()
    email_id = req.form.get('email_id')
    password = req.form.get('password')

    if check_Validation(email_id, password):
        return jsonify({
            'data':[],
            'status': 'failer',
            'message': 'Invalid Data'
        })

    data = conn.login(conn.get_Cursor(), email_id, password)
    return jsonify({
        'data': [] if data == "NOT_FOUND" else [] if data == "WRONG_PASSWORD" else data,
        'status': 'failer' if data == "NOT_FOUND" else 'failer' if data == 'WRONG_PASSWORD' else 'success',
        'message': 'User not found' if data == "NOT_FOUND" else 'password is wrong' if data == 'WRONG_PASSWORD' else 'login successfully'
    })


def check_Validation(*args):
    isValid = False
    for arg in args:
        if arg == "":
            isValid = True
    return isValid

if __name__ == '__main__':
    app.run(debug=True)

#host='192.168.43.4', port=5000,
