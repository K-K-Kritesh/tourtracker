from datetime import datetime
from flask import jsonify
import mysql.connector as mysql
from mysql.connector import Error
import SqlQuery as query
from passlib.hash import pbkdf2_sha256 as sha256


class Connection():
    def __init__(self):
        try:
            self.connection = mysql.connect(
                host='localhost',
                user='root',
                password='root6575',
                database='tourtracker'
            )
            if self.connection.is_connected():
                cur = self.connection.cursor()
                #self.delete_User(cur)
                #self.createDataBase(cur)
                #self.Create_Table_tour_people_register(cur)
                #self.Create_Table_trip_detail(cur)
                #self.Create_Table_place_detail(cur)
                #self.Create_Table_trip_codes(cur)
                #self.Create_Table_trip_members(cur)
                #self.Create_Table_trip_location(cur)
                #self.Alter_Table_tour_people_register(cur)
                #self.get_column_name(cur, self.connection)
                #self.Create_Table_trusted_request(cur)
                #self.Create_Table_trusted_person(cur)
                #self.Create_Table_Reset_Password(cur)
                #self.Alter_Table_add_column_trip_detail(cur)
                #self.Alter_Table_add_forgin_key_trip_detail(cur)

                #self.get_Field(cur, query.TOUR_PEOPLE_REGISTER)
                #self.get_Field(cur, query.TRIP_DETAIL)
                #self.get_Field(cur, query.PLACE_DETAIL)
                #self.get_Field(cur, query.TRIP_CODE)
                #self.get_Field(cur, query.TRIP_MEMBERS)
                #self.get_Field(cur, query.TRIP_LOCATION)
                #self.get_Field(cur, query.TRUSTED_REQUEST)
                #self.get_Field(cur, query.TRUSTED_PERSON)
                print("Database Initialize Successfully") 
        except Error as e:
            print("Error while coonecting error",e)

    # ==== Create Table and change table field get column of table defination start

    def get_Cursor(self):
        return self.connection.cursor()

    def createDataBase(self,cur):
        cur.execute(query.CREATE_DATABASE)

    def Create_Table_tour_people_register(self, cur):
        cur.execute(query.CREATE_TABLE_TOUR_PEOPLE_REGISTER)

    def Create_Table_trip_detail(self, cur):
        cur.execute(query.CREATE_TABLE_TRIP_DETAIL)

    def Create_Table_place_detail(self, cur):
        cur.execute(query.CREATE_TABLE_PLACE_DETAIL)

    def Create_Table_trip_codes(self, cur):
        cur.execute(query.CREATE_TABLE_TRIP_CODES)

    def Create_Table_trip_members(self, cur):
        cur.execute(query.CREATE_TABLE_TRIP_MEMBERS)

    def Create_Table_trip_location(self, cur):
        cur.execute(query.CREATE_TABLE_TRIP_LOCATION)

    def Create_Table_trusted_request(self, cur):
        cur.execute(query.CREATE_TABLE_TRUSTED_REQUEST)
        print("Table created")

    def Create_Table_trusted_person(self, cur):
        cur.execute(query.CREATE_TABLE_TRUSTED_PERSON)    
        print("Table created")

    def Create_Table_Reset_Password(self, cur):
        cur.execute(query.CREATE_TABLE_RESET_PASSWORD_LINK)
        print('reset password created')

    def Alter_Table_tour_people_register(self, cur):
        cur.execute(query.ALTER_TOUR_PEOPLE_REGISTER)
        print("done")

    def Alter_Table_add_column_trip_detail(self, cur):
        cur.execute(query.ALTER_TRIP_DETAIL_ADD_COLUMN)
        print("Trip detail add new column")

    def Alter_Table_add_forgin_key_trip_detail(self, cur):
        #cur.execute(query.DROP_FORGIN_KEY)
        cur.execute(query.ALTER_TRIP_DETAIL_ADD_FORGIN_KEYY)
        #cur.execute(query.CHECK_FK)
        #print(cur.fetchall())
        #cur.execute(query.COLUMN_NAME)
        #print(cur.fetchall())
        #cur.execute(query.truncate)
        print("add forgin key")

    def get_column_name(self, cur, conn):
        cur.execute(query.COLUMN_NAME)
        print(cur.fetchall())

    def get_Field(self, cur, tablename):
        cur.execute(f"select * from {tablename}")
        print([x[0] for x in cur.description])

    # Create Table and change table field get column of table defination over===

    # === Table Insert, Update, Delete query start
    
    def Insert_tour_people_register(self, cur, *param):
        try:
            cur.execute(f"select * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[2]}'")
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute(f"INSERT INTO {query.TOUR_PEOPLE_REGISTER} (first_name, last_name, email_id, mobile_no, gender, address, password, trusted_person_t_code, created_trips, joined_trips, trusted_person, birth_date, blood_group, health_problems) VALUES('{param[0]}','{param[1]}','{param[2]}','{param[3]}','{param[4]}','{param[5]}','{param[6]}','{param[7]}','{param[8]}','{param[9]}','{param[10]}','{param[11]}','{param[12]}','{param[13]}')")
                row_id = cur.lastrowid
                self.connection.commit()
                cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE id = {row_id}")
                row_header = [x[0] for x in cur.description]
                rv = cur.fetchall()
                for result in rv:
                    json_data = dict(zip(row_header, result))
                return json_data
            else:
                return []
        except Exception as e:
            return []
        finally:
            cur.close()

    def Insert_reset_password_link_key(self, cur, *param):
        try:
            cur.execute(f"select * from {query.RESET_PASSWORD} WHERE email_id like '{param[0]}'")
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute(f"INSERT INTO {query.RESET_PASSWORD} (email_id, reset_link_key, date) VALUES('{param[0]}','{param[1]}','{param[2]}')")
                row_id = cur.lastrowid
                self.connection.commit()
                return "INSERT"
            else:
                cur.execute(f"UPDATE {query.RESET_PASSWORD} SET reset_link_key = '{param[1]}', date = '{param[2]}' WHERE email_id like '{param[0]}'")
                row_id = cur.lastrowid
                self.connection.commit()
                return "UPDATE"
        except Exception as e:
            return []
        finally:
            cur.close()

    def Update_User_Data(self, cur, *param):
        try:
            cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[0]}'")
            data = cur.fetchall()
            if len(data) == 0:
                return "NOT_FOUND"
            else:
                cur.execute(f"UPDATE {query.TOUR_PEOPLE_REGISTER} SET first_name = '{param[1]}', last_name = '{param[2]}', mobile_no = '{param[3]}', gender = '{param[4]}', address= '{param[5]}', birth_date='{param[6]}', blood_group='{param[7]}', health_problems='{param[8]}' WHERE email_id like '{param[0]}'")
                row_id = cur.lastrowid
                self.connection.commit()
                cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[0]}'")
                row_header = [x[0] for x in cur.description]
                rv = cur.fetchall()
                for result in rv:
                    json_data = dict(zip(row_header, result))
                return json_data
        except Exception as e:
            return []
        finally:
            cur.close()

    def Update_password(self, cur, *param):
        try:
            enctypted_password = str(sha256.using(salt_size = 16, rounds =200).hash(param[1]))
            cur.execute(f"UPDATE {query.TOUR_PEOPLE_REGISTER} SET password = '{enctypted_password}' WHERE email_id like '{param[0]}'")
            self.connection.commit()
            return "Password Reset Successfully"
        except Exception as e:
            return str(e)

    def login(self, cur, *param):
        try:
            cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[0]}'")
            row_header = [x[0] for x in cur.description]
            rv = cur.fetchall()
            if len(rv) == 0:
                return "NOT_FOUND"
            else:
                if sha256.using(salt_size=16, rounds=200).verify(f"{param[1]}", rv[0][7]):
                    for result in rv:
                        json_data = dict(zip(row_header, result))
                    return json_data
                else:
                    return "WRONG_PASSWORD"
        except Exception as e:
            return e
        finally:
            cur.close()

    def delete_User(self, cur):
        try:
            cur.execute(f"DELETE FROM {query.TOUR_PEOPLE_REGISTER} WHERE id like 24 ")
            self.connection.commit()
            print("delete record")
        except Exception as e:
            print(str(e))
        finally:
            cur.close()

    def get_Data(self, cur, tableName):
        cur.execute(f"select * from {tableName}")
        row_header = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_header, result)))
        cur.close()
        return json_data

    def get_reset_password_emailid(self, cur, key):
        cur.execute(f"select * from {query.RESET_PASSWORD} WHERE reset_link_key like '{key}'")
        row_header = [x[0] for x in cur.description]
        rv = cur.fetchall()
        if len(rv) == 0 :
            return "URL_NOT_FOUND"
        else:
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_header, result)))
            email_id = json_data[0]['email_id']
            cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{email_id}'")
            data = cur.fetchall()
            if len(data) == 0:
                cur.close()
                return "NOT_FOUND"
            else:
                cur.close()
                return json_data

    def Code_Is_Exists(self, cur, code, tquery):
        try:
            cur.execute(tquery + f"'{code}'")
            if len(cur.fetchall()) == 0:
                return False
            else:
                return True
        except Exception as e:
            cur.close()
            return e
        finally:
            cur.close()

    def Change_Password(self, cur, *param):
        try:
            cur.execute(query.Select_Data.format(param[0]))
            result = cur.fetchone()
            if sha256.using(salt_size=16, rounds=200).verify(f"{param[2]}", result[0]):
                cur.execute(query.Change_Password.format(param[1], param[0]))
                self.connection.commit()
                cur.close()
                return 'Password change Sucessfully'
            else:
                cur.close()
                return 'Old Password is not match'
        except Exception as e:
            cur.close()
            return e
        finally:
            cur.close()

    def Insert_Create_Trip_Detail(self, cur, *param):
        cur.execute(f"INSERT INTO {query.TRIP_DETAIL} (trip_title, sorce_location, destination_location, start_time_date, end_time_date, no_of_place_visit, id) VALUES('{param[0]}','{param[1]}','{param[2]}','{param[3]}','{param[4]}',{param[5]},{param[6]})")
        row_id = cur.lastrowid
        self.connection.commit()
        cur.execute(f"SELECT * from {query.TRIP_DETAIL} WHERE trip_id = {row_id}")
        row_header = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data = dict(zip(row_header, result))
        cur.close()
        return json_data

    def Insert_Create_Place_Detail(self, cur, *param):
        cur.execute(f"INSERT INTO {query.PLACE_DETAIL} (place_name, address1, address2, trip_id) VALUES('{param[0]}','{param[1]}','{param[2]}',{param[3]})")
        row_id = cur.lastrowid
        self.connection.commit()
        cur.execute(f"SELECT * from {query.PLACE_DETAIL} WHERE place_id = {row_id}")
        row_header = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data = dict(zip(row_header, result))
        cur.close()
        return json_data

    def Update_Place_Detail(self, cur, *param):
        cur.execute(f"SELECT * FROM {query.PLACE_DETAIL} WHERE place_id = {param[0]}")
        if len(cur.fetchall()) != 0:
            cur.execute(f"UPDATE {query.PLACE_DETAIL} set place_name = '{param[1]}', address1 = '{param[2]}', address2 = '{param[3]}' WHERE place_id = {param[0]}")
            self.connection.commit()
            return "UPDATE"
        else:
            return "NOT_FOUND"

    def Delete_Place_Detail(self, cur, place_id):
        cur.execute(f"SELECT * FROM {query.PLACE_DETAIL} WHERE place_id = {place_id}")
        if len(cur.fetchall()) != 0:
            cur.execute(f"DELETE {query.PLACE_DETAIL} WHERE place_id = {place_id}")
            self.connection.commit()
            return "DELETE"
        else:
            return "NOT_FOUND"

    def Insert_Create_T_Code(self, cur, *param):

        cur.execute(f"SELECT * from {query.TRIP_CODE} WHERE trip_id = {param[1]}")
        if len(cur.fetchall()) == 0:
            cur.execute(f"INSERT INTO {query.TRIP_CODE} (trip_code, trip_id) VALUES('{param[0]}',{param[1]})")
            row_id = cur.lastrowid
            self.connection.commit()
            cur.execute(f"SELECT * from {query.TRIP_CODE} WHERE trip_code_id = {row_id}")
            row_header = [x[0] for x in cur.description]
            rv = cur.fetchall()
            json_data = []
            for result in rv:
                json_data = dict(zip(row_header, result))
            cur.close()
            return json_data
        else:
            return "ALREADY"
        
    def Insert_Create_Add_Trip_Members(self, cur, *param):

        cur.execute(f"SELECT * from {query.TRIP_MEMBERS} WHERE trip_id = {param[0]} and id = {param[1]}")
        if len(cur.fetchall()) == 0:
            cur.execute(f"SELECT trip_code_id from {query.TRIP_CODE} WHERE trip_code like '{param[2]}'")
            trip_code_id = cur.fetchone()
            if trip_code_id != None:
                cur.execute(f"INSERT INTO {query.TRIP_MEMBERS} (trip_id, id, trip_code_id) VALUES({param[0]} ,{param[1]}, {trip_code_id[0]})")
                row_id = cur.lastrowid
                self.connection.commit()
                cur.execute(f"SELECT * from {query.TRIP_MEMBERS} WHERE trip_code_id = {row_id}")
                row_header = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_data = []
                for result in rv:
                    json_data = dict(zip(row_header, result))
                cur.close()
                return json_data
            else:
                return "CODE_NOT_FOUND"
        else:
            return "ALREADY"
            

    def Insert_Create_Add_Trip_Location(self, cur, *param):

        cur.execute(f"SELECT * from {query.TRIP_LOCATION} WHERE trip_id = {param[3]}")
        if len(cur.fetchall()) == 0:
            cur.execute(f"INSERT INTO {query.TRIP_LOCATION} (source_location, destination_location, s_d_key, trip_id) VALUES('{param[0]}','{param[1]}','{param[2]}',{param[3]})")
            row_id = cur.lastrowid
            self.connection.commit()
            cur.execute(f"SELECT * from {query.TRIP_LOCATION} WHERE trip_location_id = {row_id}")
            row_header = [x[0] for x in cur.description]
            rv = cur.fetchall()
            json_data = []
            for result in rv:
                json_data = dict(zip(row_header, result))
            cur.close()
            return json_data
        else:
            return "ALREADY"
        
    def Insert_Add_Trusted_Person(self, cur, *param):

        cur.execute(f"SELECT id from {query.TOUR_PEOPLE_REGISTER} WHERE trusted_person_t_code like '{param[0]}'")
        trusted_person_id = cur.fetchone()
        if trusted_person_id != None:
            cur.execute(f"SELECT * from {query.TRUSTED_PERSON} WHERE id = {param[1]}")    
            if len(cur.fetchall()) == 0:
                cur.execute(f"INSERT INTO {query.TRUSTED_PERSON} (trusted_code, id) VALUES('{param[0]}',{param[1]})")
                cur.execute(f"UPDATE {query.TOUR_PEOPLE_REGISTER} set trusted_person = '{trusted_person_id[0]}' WHERE id = {param[1]}")
                row_id = cur.lastrowid
                self.connection.commit()
                cur.execute(f"SELECT * from {query.TRUSTED_PERSON} WHERE trusted_person_id = {row_id}")
                row_header = [x[0] for x in cur.description]
                rv = cur.fetchall()
                json_data = []
                for result in rv:
                    json_data = dict(zip(row_header, result))
                cur.close()
                return json_data
            else:
                return "ALREADY"
        else:
            return "USER_NOT_FOUND"

    def update_Add_Trusted_Person(self, cur, *param):
        cur.execute(f"SELECT * FROM {query.TRUSTED_PERSON} WHERE id = {param[1]}")
        if len(cur.fetchall()) != 0:
            cur.execute(f"UPDATE {query.TRUSTED_PERSON} SET trusted_code = '{param[0]}' WHERE id = {param[1]}")
            self.connection.commit()
            return 'UPDATE'
        else:
            return "NOT_FOUND"    
        
        
    def get_My_Trusted_Person(self, cur, userid):
        cur.execute(f"SELECT trusted_code from {query.TRUSTED_PERSON} WHERE id = {userid}")
        trusted_code = cur.fetchone()[0]
        if trusted_code != None:
            cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE trusted_person_t_code like '{trusted_code}'")
            people_data = cur.fetchone()
            row_header = [x[0] for x in cur.description]
            people_json = dict(zip(row_header, people_data))
            return people_json
        else:
            return "NOT_FOUND"

    def delete_Trip(self, cur, trip_id):
        cur.execute(f"SELECT * FROM {query.TRIP_DETAIL} WHERE trip_id like {trip_id}")
        if len(cur.fetchall()) == 0:
            return "NOT_FOUND"
        else:
            cur.execute(f"DELETE FROM {query.TRIP_DETAIL} WHERE trip_id like {trip_id}")
            self.connection.commit()
            return "DELETE"
            
    def get_All_Trip(self, cur, id):
        ids = self.getalltripdata(cur, id)
        now_date = datetime.now()
        current_date = datetime(now_date.year, now_date.month, now_date.day).strftime('%d-%m-%Y') 
        second_date = datetime.strptime(current_date,'%d-%m-%Y')
        cur.execute(f"SELECT t.*, c.trip_code FROM {query.TRIP_DETAIL} t, {query.TRIP_CODE} c WHERE t.trip_id IN {ids} and t.trip_id = c.trip_id")
        allTrip = cur.fetchall()
        if len(allTrip) != 0:
            row_header = [x[0] for x in cur.description]
            completed_json = []
            upcoming_json = []
            current_json = []
            print(type(completed_json))
            for result in allTrip:
                first_date, thired_date = self.get_StartDate_EndDate(result[4], result[5])
                placedetaildata = self.get_Place_Detail(cur, result[0])
                membersdata = self.get_Members_Detail(cur, result[0])
                if first_date < second_date > thired_date:
                    completed_json.append(dict(zip(row_header, result), placedetail=placedetaildata, members=membersdata))
                elif first_date == second_date == thired_date:
                    current_json.append(dict(zip(row_header, result), placedetail=placedetaildata, members=membersdata))
                else:
                    upcoming_json.append(dict(zip(row_header, result), placedetail=placedetaildata, members=membersdata))

            return (completed_json, current_json, upcoming_json)
        else:
            return ("NO_DATA", [],[])

        
    def get_Place_Detail(self, cur, id):
        cur.execute(f"SELECT * FROM {query.PLACE_DETAIL} WHERE trip_id = {id}")
        placedata = cur.fetchall()
        if len(placedata) != 0:
            row_header = [x[0] for x in cur.description]
            place_json = []
            for result in placedata:
                place_json.append(dict(zip(row_header, result)))
            return place_json
        else:
            return []

    def get_Members_Detail(self, cur, id):
        cur.execute(f"SELECT p.first_name, p.last_name, p.id, p.mobile_no,m.trip_id, m.id FROM {query.TRIP_MEMBERS} m, {query.TOUR_PEOPLE_REGISTER} p WHERE m.id = p.id and m.trip_id = {id}")
        placedata = cur.fetchall()
        if len(placedata) != 0:
            row_header = [x[0] for x in cur.description]
            place_json = []
            for result in placedata:
                place_json.append(dict(zip(row_header, result)))
            return place_json
        else:
            return []


    def get_Trip_Detail(self, cur):
        cur.execute(f"SELECT * FROM {query.TRIP_DETAIL}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.PLACE_DETAIL}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.TRIP_CODE}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.TRIP_LOCATION}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.TRIP_MEMBERS}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.TRUSTED_PERSON}")
        print(cur.fetchall())
        cur.execute(f"SELECT * FROM {query.TRUSTED_REQUEST}")
        print(cur.fetchall())
    

    #Table Insert, Update, Delete query start ===


    def get_StartDate_EndDate(self, s_date, e_date):
        start_date = datetime.strptime(s_date,'%d-%m-%Y')
        start_date = datetime(start_date.year, start_date.month, start_date.day).strftime('%d-%m-%Y') 
        end_date = datetime.strptime(e_date,'%d-%m-%Y')
        end_date = datetime(end_date.year, end_date.month, end_date.day).strftime('%d-%m-%Y') 
        first_date = datetime.strptime(start_date,'%d-%m-%Y')
        thired_date = datetime.strptime(end_date,'%d-%m-%Y')
        return (first_date, thired_date)


    def getalltripdata(self, cur, myid):
        datajson = list()
        cur.execute(f"select {query.TRIP_CODE}.trip_id from {query.TRIP_MEMBERS} as member INNER JOIN {query.TRIP_CODE} ON member.trip_code_id = {query.TRIP_CODE}.trip_code_id where member.id = {myid}")
        tripids = cur.fetchall()
        for id in tripids:
            datajson.append(id[0])
        cur.execute(f"SELECT * FROM {query.TRIP_DETAIL} WHERE id = {myid}")
        tripidss = cur.fetchall()
        for id in tripidss:
            if id[0] not in datajson:
                datajson.append(id[0])
        return tuple(datajson)
    
        


