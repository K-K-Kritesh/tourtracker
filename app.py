from flask import Flask as flask, jsonify, request as req
import Connection
import Route as route
from passlib.hash import pbkdf2_sha256 as sha256

app = flask(__name__)

@app.route('/')
def index():
    Connection.Connection()
    return "Server started"

@app.route(route.register, methods=['POST'])
def RegisterTourTracker():
    first_name = req.form.get('first_name')
    last_name = req.form.get('last_name')
    email_id = req.form.get('email_id')
    mobile_no = req.form.get('mobile_no')
    gender = req.form.get('gender')
    address = req.form.get('address')
    trusted_person_t_code = req.form.get('trusted_person_code')
    created_trips = req.form.get('created_trips')
    joined_trips = req.form.get('joined_trips')
    trusted_person = req.form.get('trusted_person')
    birth_date = req.form.get('birth_date')
    blood_group = req.form.get('blood_group')
    health_problems = req.form.get('health_problems')


    password = req.form.get('password')
    encrypt_password = ""
    if password != None:
        encrypt_password = sha256.using(salt_size = 16, rounds =200).hash(password)

    return f"Register successfully {first_name} {last_name} {encrypt_password}"



if __name__ == '__main__':
    app.run(debug=True)

#host='192.168.43.4', port=5000,
