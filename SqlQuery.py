TOUR_PEOPLE_REGISTER = "tourPeopleRegister"
TRIP_DETAIL = "tripdetail"
PLACE_DETAIL = "placedetail"
TRIP_CODE = "tripcodes"
TRIP_MEMBERS = "tripmembers"
TRIP_LOCATION = "triplocation"


CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS tourtracker"
CREATE_TABLE_TOUR_PEOPLE_REGISTER = f"CREATE TABLE IF NOT EXISTS {TOUR_PEOPLE_REGISTER} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255),last_name VARCHAR(255),email_id VARCHAR(255),mobile_no VARCHAR(255),gender INT(1),address TEXT,password VARCHAR(255),trusted_person_t_code VARCHAR(255),created_trips VARCHAR(255),joined_trips VARCHAR(255),trusted_person VARCHAR(255),birth_date DATETIME,blood_group VARCHAR(255),health_problems VARCHAR(255))"
CREATE_TABLE_TRIP_DETAIL = f"CREATE TABLE IF NOT EXISTS {TRIP_DETAIL} (trip_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, trip_title VARCHAR(255), sorce_location VARCHAR(255), destination_location VARCHAR(255), start_time_date DATETIME, end_time_date DATETIME, no_of_place_visit INT(2))"
