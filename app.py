from flask import Flask as flask, jsonify, request as req
import Connection as con
import Route as route
from passlib.hash import pbkdf2_sha256 as sha256
import SqlQuery as query
import random
import string
import BusinessMailUtils as BMU
import urllib.request as urlopen
import os, time
from datetime import datetime

conn = None;

app = flask(__name__)    

# API Defination

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

    trusted_person_t_code = check_Code_Exists(conn, trusted_person_t_code, query.Check_Code_Is_Exists)
    

    password = req.form.get('password')
    encrypt_password = ""
    if password != None:
        encrypt_password = str(sha256.using(salt_size = 16, rounds =200).hash(password))

    if check_Validation(first_name, last_name, email_id, gender, address, encrypt_password):
        return invalid_Data()
    
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
        return invalid_Data()

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
        return invalid_Data()

    data = conn.login(conn.get_Cursor(), email_id, password)
    return jsonify({
        'data': [] if data == "NOT_FOUND" else [] if data == "WRONG_PASSWORD" else data,
        'status': 'failer' if data == "NOT_FOUND" else 'failer' if data == 'WRONG_PASSWORD' else 'success',
        'message': 'User not found' if data == "NOT_FOUND" else 'password is wrong' if data == 'WRONG_PASSWORD' else 'login successfully'
    })

@app.route(route.changePassword, methods=['POST'])
def changePassword():
    conn = con.Connection()

    email_id = req.form.get('email_id')
    new_password = req.form.get('new_Password')
    old_password = req.form.get('old_Password')

    encrypt_password = ""
    if new_password != None and old_password != None:
        encrypt_password = str(sha256.using(salt_size = 16, rounds =200).hash(new_password))

    if check_Validation(email_id, new_password, old_password):
        return invalid_Data()

    message = conn.Change_Password(conn.get_Cursor(), email_id, encrypt_password, old_password)
    return jsonify({
        'status':'Success',
        'message':message
    })

@app.route(route.forgetPassword, methods=['POST'])
def forgotPassword():
    try:
        conn = con.Connection()
        email_id = req.form.get('email_id')
        if check_Validation(email_id):
            return invalid_Data()

        mail = BMU.BusinessMailUtils()
        dir = os.path.dirname(os.path.realpath('__file__'))
        path = os.path.join(dir, 'html/forgotpasswordmail.html')
        html = urlopen.urlopen('file://'+path).read()
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))+(str(time.time()).replace(".",""))
        url = f"http://127.0.0.1:5000/tourtracker/resetpassword/{key}"
        timestamp = str(time.time())
        conn.Insert_reset_password_link_key(conn.get_Cursor(), email_id, key, timestamp)
        status = mail.forgot_password_send_mail(html, email_id, "Forgot Password", "html", url)
        return jsonify({
            'status':'success' if status == "SEND_MSG" else 'failer',
            'message':'Send Password Reset Link To Your Mail' if status == "SEND_MSG" else 'something went wrong! please try again',
            })
    except Exception as e:
        return str(e)


@app.route(route.resetPasswordLink+"/<string:key>")
def resetpassword(key):
    conn = con.Connection()
    data = conn.get_reset_password_emailid(conn.get_Cursor(), key)
    #E8DHMBJGQK2F
    if data == 'NOT_FOUND':
        return "<html><body style='text-align:center'><h1>Sorry...! User Not Found</h1></body></html>"
    elif data == 'URL_NOT_FOUND':
        return "<html><body style='text-align:center'><h1>Url not Found</h1></body></html>"
    else:
        timestamp1 = float(data[0]['date'])
        timestamp2 = time.time()
        differences = datetime.fromtimestamp(timestamp1).hour - datetime.fromtimestamp(timestamp2).hour
        if differences > 24:
            return "<html><body style='text-align:center'><h1>URL Not Found</h1></body></html>"
        else:
            return "<html><head> <script>function formvalidation(form) { password1 = form.password.value; password2 = form.confirmpassword.value; var format = /[ `!@#$%^&*()_+\-=\[\]{};':\\|,.<>\/?~]/; if(!password1.match(format)){ alert('At least one Special character is required!'); return false } else if(!password1.match(/\d/)) {alert('At least one digit required!'); return false;} else if(!password1.match(/[a-z]/i)){ alert('At least one letter required!')} else { if(password1 != password2){ alert ('Password did not match: Please try again...'); return false;} else {return true;}}}</script></head><style>.form_input{ height: 40px; width: 300px; padding: 5px; border-style: solid; border-width: 3px; color: black; border-color: black; margin: 5px; font-size: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; } .form_input:focus{ outline: none; } .form_input::placeholder{ color: black; opacity: 1; } .form_submit { height: 40px; width: 300px; padding: 5px; background-color: black; color: white; border: none; margin: 5px; border-radius: 10px; font-size: 14px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; } </style> <body> <div style='text-align: center;'> <p style='width: 100%; padding: 10px;background-color: black;color: white; font-size: 17px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;'>Tour Tracker</p> <H2 style=' margin-top: 10% ;font-weight: bold;color: black; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;'>Choose a new <br/> password</H1> <form action='/passwordreset' method='post' onsubmit='return formvalidation(this)'> <input type='hidden' name='email' value='"+data[0]['email_id']+"' required/><br/> <input class='form_input' type='password' name='password' placeholder='Password' required></input><br/> <input class='form_input' type='password' name='confirmpassword' placeholder='Confirm Password' required></input><br/> <input class='form_submit' type='submit' value='Submit'></input> </form> </div> </body> </html>"


@app.route('/passwordreset', methods=['POST'])
def passwordReset():
    conn = con.Connection()
    email = req.form['email']
    password = req.form['password']
    confirmpassword = req.form['confirmpassword']
    return conn.Update_password(conn.get_Cursor(), email, password)


@app.route(route.createTripDetail, methods=['POST'])
def create_Trip_Detail():
    conn = con.Connection()

    trip_title = req.form.get('trip_title')
    source_location = req.form.get('source_location')
    destination_location = req.form.get('destination_location')
    start_time_date = req.form.get('start_time_date')
    end_time_date = req.form.get('end_time_date')
    noof_place_visit = req.form.get('no_of_place_visit')
    tour_place_id = req.form.get('id')

    if check_Validation(trip_title, source_location, destination_location, start_time_date, end_time_date, noof_place_visit, tour_place_id):
        return invalid_Data()

    data = conn.Insert_Create_Trip_Detail(conn.get_Cursor(), trip_title, source_location, destination_location, start_time_date, end_time_date, noof_place_visit, tour_place_id)
    return jsonify({
        'data':data,
        'status':'success',
        'message':'Trip Created Successfully'
    })
    
@app.route(route.createPlaceDetail, methods=['POST'])
def create_Place_Detail():
    conn = con.Connection()

    place_name = req.form.get('place_name')
    address1 = req.form.get('address1')
    address2 = req.form.get('address2')
    trip_id = req.form.get('trip_id')

    if check_Validation(place_name, address1, address2, trip_id):
        return invalid_Data()

    data = conn.Insert_Create_Place_Detail(conn.get_Cursor(), place_name, address1, address2, trip_id)
    return jsonify({
        'data':data,
        'status':'success',
        'message':'Place Added Successfully'
    })

@app.route(route.updatePlaceDetail, methods=['POST'])
def update_Place_Detail():
    conn = con.Connection()

    place_id = req.form.get('place_id')
    place_name = req.form.get('place_name')
    address1 = req.form.get('address1')
    address2 = req.form.get('address2')

    if check_Validation(place_name, address1, address2):
        return invalid_Data()

    data = conn.Update_Place_Detail(conn.get_Cursor(), place_id, place_name, address1, address2)
    return jsonify({
        'data':[],
        'status':'failer' if data == 'NOT_FOUND' else 'success',
        'message':'Place Detail Not Found' if data == 'NOT_FOUND' else 'Place Detail updated'
    })

@app.route(route.deletePlaceDetail, methods=['POST'])
def delete_Place_Detail():
    conn = con.Connection()
    place_id = req.form.get('place_id')

    if check_Validation(place_id):
        return invalid_Data()

    data = conn.Delete_Place_Detail(conn.get_Cursor(), place_id)
    return jsonify({
        'data':[],
        'status':'failer' if data == 'NOT_FOUND' else 'success',
        'message':'Place Detail Not Found' if data == 'NOT_FOUND' else 'Place Detail Delete Sucessfully'
    })


@app.route(route.createTCode, methods=['POST'])
def create_T_Code():
    conn = con.Connection()

    trip_id = req.form.get('trip_id')
    trip_code = 'T-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    trip_code = check_Code_Exists(conn, trip_code, query.Check_T_Code)
    if check_Validation(trip_id):
        return invalid_Data()

    data = conn.Insert_Create_T_Code(conn.get_Cursor(), trip_code, trip_id)
    return jsonify({
        'data':[] if data == "ALREADY" else data,
        'status':'failer' if data == "ALREADY" else 'success',
        'message':'Already generated for this trip' if data == "ALREADY" else 'Trip Code Generated'
    })

# Join group api
@app.route(route.createaddtripmember, methods=['POST'])
def create_Add_Trip_Member():
    conn = con.Connection()
    trip_id = req.form.get('trip_id')
    id = req.form.get('id')
    trip_code = req.form.get('trip_code')
    if check_Validation(trip_id, id, trip_code):
        return invalid_Data()

    data = conn.Insert_Create_Add_Trip_Members(conn.get_Cursor(), trip_id, id, trip_code)
    return jsonify({
        'data': [] if data == "ALREADY" else [] if data == "CODE_NOT_FOUND" else data,
        'status':'failer' if data == "ALREADY" else 'failer' if data == "CODE_NOT_FOUND" else'success',
        'message':'This member already added' if data == "ALREADY" else 'This code not found' if data == "CODE_NOT_FOUND" else 'Member added',
    })

@app.route(route.createaddtriplocation, methods=['POST'])
def create_Add_Trip_Location():
    conn = con.Connection()
    # first longitude second latitude
    source = req.form.get('source_location')
    destination = req.form.get('destination_location')
    sdKey = req.form.get('polyline_key')
    trip_id = req.form.get('trip_id')

    if check_Validation(source, destination, sdKey, trip_id):
        return invalid_Data()

    data = conn.Insert_Create_Add_Trip_Location(conn.get_Cursor(), source, destination, sdKey, trip_id)
    return jsonify({
        'data':[] if data == "ALREADY" else data,
        'status':'failer' if data == "ALREADY" else 'success',
        'message':'Already Location added for this trip' if data == "ALREADY" else 'Trip Location added'
    })

@app.route(route.trustedperson, methods=['POST'])
def add_Trusted_Person():
    conn = con.Connection()
    trusted_code = req.form.get('trusted_person_code')
    userid = req.form.get('userid')

    if check_Validation(trusted_code, userid):
        return invalid_Data()

    data = conn.Insert_Add_Trusted_Person(conn.get_Cursor(), trusted_code, userid)
    return jsonify({
        'data': [] if data == "ALREADY" else [] if data == "USER_NOT_FOUND" else data ,
        'status': 'failer' if data == "ALREADY" else 'failer' if data == "USER_NOT_FOUND" else 'success',
        'message': 'you can select only one trusted person' if data == "ALREADY" else "This User Not Found" if data == "USER_NOT_FOUND" else "select your trusted person"
    })

@app.route(route.updatetrustedperson, methods=['POST'])
def update_Trusted_Person():
    conn = con.Connection()
    trusted_code = req.form.get('trusted_person_code')
    userid = req.form.get('userid')

    if check_Validation(trusted_code, userid):
        return invalid_Data()

    data = conn.update_Add_Trusted_Person(conn.get_Cursor(), trusted_code, userid)
    return jsonify({
        'data': [] if data == "NOT_FOUND" else data,
        'status': 'failer' if data == "NOT_FOUND" else 'success',
        'message': 'Data Not Found' if data == "NOT_FOUND" else "update your trusted person"
    })

@app.route(route.getmytrustedperson, methods=['POST'])
def get_My_Trusted_Person():
    conn = con.Connection()
    userid = req.form.get('userid')

    if check_Validation(userid):
        return invalid_Data()
    trusted_code = conn.get_My_Trusted_Person(conn.get_Cursor(), userid)
    return jsonify({
        'data':[] if trusted_code == "NOT_FOUND" else trusted_code,
        'status':'success',
        'message':''
    })

@app.route(route.deletetrip, methods=['POST'])
def delete_Trip():
    conn = con.Connection()
    trip_id = req.form.get('trip_id')
    if check_Validation(trip_id):
        return invalid_Data()
    #conn.get_Trip_Detail(conn.get_Cursor())
    deletetrip = conn.delete_Trip(conn.get_Cursor(), trip_id)
    return jsonify({
        'message':deletetrip
    })
    
    
@app.route(route.alltrip, methods=['POST'])
def All_Trip():
    conn = con.Connection()
    id = req.form.get('userId')
    completed_json, current_json, upcoming_json = conn.get_All_Trip(conn.get_Cursor(), id)
    return jsonify({
        'upcoming': upcoming_json,
        'current': current_json,
        'completed': [] if completed_json == "NO_DATA" else completed_json,
        'status': 'failer' if completed_json == "NO_DATA" else 'success',
        'message': 'Data Not Found' if completed_json == "NO_DATA" else 'Trip Data'
    })
        
# General defination

def check_Validation(*args):
    isValid = False
    for arg in args:
        if arg == "" or arg == None:
            isValid = True
    return isValid

def check_Code_Exists(conn, code, tquery):
    Code_isExists = conn.Code_Is_Exists(conn.get_Cursor(), code, tquery)
    if Code_isExists:
        new_Code = 'T-'+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return check_Code_Exists(conn, new_Code, tquery)
    else:
        return code

def invalid_Data():
    return jsonify({'data':[],'status': 'failer','message': 'Invalid Data'})


if __name__ == '__main__':
        app.run(debug=True)
#host='192.168.43.4', port=5000,
