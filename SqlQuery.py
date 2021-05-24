TOUR_PEOPLE_REGISTER = "tourPeopleRegister"
TRIP_DETAIL = "tripdetail"
PLACE_DETAIL = "placedetail"
TRIP_CODE = "tripcodes"
TRIP_MEMBERS = "tripmembers"
TRIP_LOCATION = "triplocation"
TRUSTED_REQUEST = "trusted_request"
TRUSTED_PERSON = "trusted_person"
RESET_PASSWORD = "reset_password"


# Create table query
CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS tourtracker"
CREATE_TABLE_TOUR_PEOPLE_REGISTER = f"CREATE TABLE IF NOT EXISTS {TOUR_PEOPLE_REGISTER} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255),last_name VARCHAR(255),email_id VARCHAR(255),mobile_no VARCHAR(255),gender INT(1),address TEXT,password VARCHAR(255),trusted_person_t_code VARCHAR(255),created_trips VARCHAR(255),joined_trips VARCHAR(255),trusted_person VARCHAR(255),birth_date DATETIME,blood_group VARCHAR(255),health_problems VARCHAR(255))"
CREATE_TABLE_TRIP_DETAIL = f"CREATE TABLE IF NOT EXISTS {TRIP_DETAIL} (trip_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trip_title VARCHAR(255), sorce_location VARCHAR(255), destination_location VARCHAR(255), start_time_date VARCHAR(255), end_time_date VARCHAR(255), no_of_place_visit INT(2), id INT)"
CREATE_TABLE_PLACE_DETAIL = f"CREATE TABLE IF NOT EXISTS {PLACE_DETAIL} (place_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, place_name VARCHAR(255), address1 VARCHAR(255), address2 VARCHAR(255), trip_id INT)"
CREATE_TABLE_TRIP_CODES = f"CREATE TABLE IF NOT EXISTS {TRIP_CODE} (trip_code_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trip_code VARCHAR(255), trip_id INT)"
CREATE_TABLE_TRIP_MEMBERS = f"CREATE TABLE IF NOT EXISTS {TRIP_MEMBERS} (trip_member_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trip_id INT, id INT, trip_code_id INT)"
CREATE_TABLE_TRIP_LOCATION = f"CREATE TABLE IF NOT EXISTS {TRIP_LOCATION} (trip_location_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, source_location VARCHAR(255), destination_location VARCHAR(255), s_d_key VARCHAR(255), trip_id INT)"
# not nedded now
CREATE_TABLE_TRUSTED_REQUEST = f"CREATE TABLE IF NOT EXISTS {TRUSTED_REQUEST} (request_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trusted_code VARCHAR(255), id INT, FOREIGN KEY (id) REFERENCES {TOUR_PEOPLE_REGISTER}(id))"
# ---------------
CREATE_TABLE_TRUSTED_PERSON = f"CREATE TABLE IF NOT EXISTS {TRUSTED_PERSON} (trusted_person_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trusted_code VARCHAR(255), id INT, FOREIGN KEY (id) REFERENCES {TOUR_PEOPLE_REGISTER}(id))"
CREATE_TABLE_RESET_PASSWORD_LINK = f"CREATE TABLE IF NOT EXISTS {RESET_PASSWORD} (email_id VARCHAR(255) unique, reset_link_key VARCHAR(255), date VARCHAR(255))"






# update table column data type and other change in table
ALTER_TOUR_PEOPLE_REGISTER = f"ALTER TABLE {TRIP_LOCATION} MODIFY s_d_key TEXT"
ALTER_TRIP_DETAIL_ADD_COLUMN = f"ALTER TABLE {TRIP_DETAIL} ADD id INT"
ALTER_TRIP_DETAIL_ADD_FORGIN_KEY = f"ALTER TABLE {PLACE_DETAIL} ADD FOREIGN KEY (trip_id) REFERENCES {TRIP_DETAIL}(trip_id) ON DELETE CASCADE"
ALTER_TRIP_DETAIL_ADD_FORGIN_KEYY = f"ALTER TABLE `{TRIP_MEMBERS}` ADD CONSTRAINT `{TRIP_MEMBERS}_people_id` FOREIGN KEY (`id`) REFERENCES `{TOUR_PEOPLE_REGISTER}` (`id`) ON DELETE CASCADE ON UPDATE CASCADE"
DROP_FORGIN_KEY = f"ALTER TABLE {PLACE_DETAIL} DROP FOREIGN KEY {PLACE_DETAIL}"

COLUMN_NAME = f"SELECT column_name as 'Column Name', data_type as 'Data Type',character_maximum_length as 'Max Length' FROM information_schema.columns WHERE table_name = '{PLACE_DETAIL}' "
CHECK_FK = f"select * from information_schema.table_constraints where constraint_schema = 'tourtracker'"


truncate = f"DROP TABLE {TRIP_MEMBERS}"








# General query
Check_Code_Is_Exists = f"SELECT * FROM {TOUR_PEOPLE_REGISTER} WHERE trusted_person_t_code like "
Check_T_Code = f"SELECT * FROM {TRIP_CODE} WHERE trip_code_id like "
Change_Password =  "UPDATE " + TOUR_PEOPLE_REGISTER + " SET password  = '{0}' WHERE email_id like '{1}'"
Select_Data = "SELECT password FROM " + TOUR_PEOPLE_REGISTER + " WHERE email_id like '{0}'"
