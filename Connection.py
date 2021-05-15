import mysql.connector as mysql
from mysql.connector import Error
import SqlQuery as query

class Connection:
    def __init__(self):
        try:
            connection = mysql.connect(
                host='localhost',
                user='root',
                password='root6575',
                database='tourtracker'
            )
            if connection.is_connected():
                cur = connection.cursor()
                #self.createDataBase(cur)
                #self.Create_Table_tour_people_register(cur)
                #self.Create_Table_trip_detail(cur)
                #self.Create_Table_place_detail(cur)
                #self.Create_Table_trip_codes(cur)
                #self.Create_Table_trip_members(cur)
                self.Create_Table_trip_location(cur)

                #self.get_Field(cur, query.TOUR_PEOPLE_REGISTER)
                #self.get_Field(cur, query.TRIP_DETAIL)
                #self.get_Field(cur, query.PLACE_DETAIL)
                #self.get_Field(cur, query.TRIP_CODE)
                #self.get_Field(cur, query.TRIP_MEMBERS)
                self.get_Field(cur, query.TRIP_LOCATION)
        except Error as e:
            print("Error while coonecting error",e)

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

    def get_Field(self, cur, tablename):
        cur.execute(f"select * from {tablename}")
        print([x[0] for x in cur.description])

Connection()
