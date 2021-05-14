import mysql.connector as mysql
from mysql.connector import Error

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
                self.createDataBase(cur)
        except Error as e:
            print("Error while coonecting error",e)

    def createDataBase(self,cur):
        cur.execute("CREATE DATABASE IF NOT EXISTS tourtracker")



Connection()
