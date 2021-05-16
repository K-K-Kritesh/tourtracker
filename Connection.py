from flask import json
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector import connection
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

                #self.get_Field(cur, query.TOUR_PEOPLE_REGISTER)
                #self.get_Field(cur, query.TRIP_DETAIL)
                #self.get_Field(cur, query.PLACE_DETAIL)
                #self.get_Field(cur, query.TRIP_CODE)
                #self.get_Field(cur, query.TRIP_MEMBERS)
                #self.get_Field(cur, query.TRIP_LOCATION)
                print("Database Initialize Successfully")

                
        except Error as e:
            print("Error while coonecting error",e)

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

    def Alter_Table_tour_people_register(self, cur):
        cur.execute(query.ALTER_TOUR_PEOPLE_REGISTER)
        print("done")

    def get_column_name(self, cur, conn):
        cur.execute(query.COLUMN_NAME)
        print(cur.fetchall())

    def get_Field(self, cur, tablename):
        cur.execute(f"select * from {tablename}")
        print([type(x[0]) for x in cur.description])

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


    def Update_User_Data(self, cur, *param):
        try:
            cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[0]}'")
            data = cur.fetchall()
            if len(data) == 0:
                return "NOT_FOUND"
            else:
                cur.execute(f"UPDATE {query.TOUR_PEOPLE_REGISTER} SET first_name = '{param[1]}', last_name = '{param[2]}', mobile_no = '{param[3]}', gender = '{param[4]}', address= '{param[5]}', birth_date='{param[6]}', blood_group='{param[7]}', health_problems='{param[8]}' WHERE email_id like '{param[0]}'")
                row_id = cur.lastrowid
                print(row_id)
                self.connection.commit()
                cur.execute(f"SELECT * from {query.TOUR_PEOPLE_REGISTER} WHERE email_id like '{param[0]}'")
                row_header = [x[0] for x in cur.description]
                rv = cur.fetchall()
                for result in rv:
                    json_data = dict(zip(row_header, result))
                return json_data
        except Exception as e:
            return []

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

    def delete_User(self, cur):
        try:
            cur.execute(f"DELETE FROM {query.TOUR_PEOPLE_REGISTER} WHERE id like 24 ")
            self.connection.commit()
            print("delete record")
        except Exception as e:
            print(str(e))

    def get_Data(self, cur, tableName):
        cur.execute(f"select * from {tableName}")
        row_header = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_header, result)))
        return json_data