import psycopg2
import uuid
from flask import session

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = 'blizzard86'
DATABASE = 'Hackathon2 - Buddy-Finder'

def make_id():
    id = uuid.uuid1()
    id_hex = id.hex
    new = False
    while new == False:
        unique_ids = "SELECT unique_id FROM users"
        for ids in unique_ids:
            if id_hex[:8] == ids:
                id = uuid.uuid1()
                id_hex = id.hex
            else:
                new = True
                return id_hex[:8]
       

def new_account(id_hex, full_name, username, email, country, password):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        query = f"INSERT INTO users (unique_id, full_name, username, email, country, password) VALUES ('{id_hex}', '{full_name}', '{username}', '{email}', '{country}', '{password}')"
        cursor.execute(query)

        connection.commit()

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
            return id_hex

def log_in(item1, password):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        logged_in = False
        cursor.execute(f"SELECT * FROM users WHERE username='{item1}' or email='{item1}'")
        log_in_user = cursor.fetchall()
        if log_in_user == []:
            print("invalid log in details!")
            return
        cursor.execute(f"SELECT * FROM users WHERE password='{password}'")
        log_in_psword = cursor.fetchall()
        if log_in_psword == []:
            print("invalid log in details!")
            return
        logged_in = True

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return logged_in

def country_db():
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM countries ORDER BY country")
        country_list = cursor.fetchall()
        list_temp = []
        for country in country_list:
            for item in country:
                list_temp.append(item)

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
            return list_temp

def update_profile(Full_name, Date_of_birth, Username, Country, City, Unique_id, Hobbies, Hidden):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"UPDATE user_profiles SET full_name = '{Full_name}', date_of_birth = '{Date_of_birth}', username = '{Username}', country = '{Country}', city = '{City}', hobbies = '{Hobbies}', hidden = '{Hidden}' WHERE unique_id = '{Unique_id}'")
        connection.commit()
        cursor.execute(f"SELECT * FROM user_profiles WHERE username = '{Username}'")
        user_details = cursor.fetchall()
        stuff = []
        for item in user_details:
            for detail in item:
                stuff.append(detail)

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return stuff


def new_profile(Full_name, Username, Country, Unique_id, Hidden):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO user_profiles (full_name, username, country, unique_id, hidden) VALUES ('{Full_name}', '{Username}', '{Country}', '{Unique_id}', '{Hidden}')")
        connection.commit()

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()

def open_profile(username):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        stuff = []
        print(username)
        cursor.execute(f"SELECT * FROM user_profiles WHERE username = '{username}'")
        user_details = cursor.fetchall()
        for item in user_details:
            for detail in item:
                stuff.append(detail)

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return stuff

def check_username(username):
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT username FROM user_profiles")
        user_details = cursor.fetchall()
        value = False
        for item in user_details:
            for detail in item:
                if detail == username:
                    value = False
                else:
                    value = True

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return value

def table_parts():
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT username FROM user_profiles WHERE hidden='no'")
        user_details = cursor.fetchall()
        x = 0
        for item in user_details:
            for detail in item:
                x+= 1

    except psycopg2.Error as err:
            print(err)

    finally:
        if connection:
            connection.close()
        return x


def table_items():
    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT username, country, city, hobbies FROM user_profiles WHERE hidden = 'no'")
        user_details = cursor.fetchall()
        rows = []
        for item in user_details:
            for detail in item:
                rows.append(detail)
        print(rows)

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return rows

def search_db(username = "", country = "", city = "", hobbies = ""):

    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f" SELECT * FROM user_profiles WHERE username LIKE '%{username}%' AND country LIKE '%{country}%' AND city LIKE '%{city}%' AND hobbies LIKE '%{hobbies}%'")
        table_data = cursor.fetchall()

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return table_data

def searchable_users():

    try:
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()
        cursor.execute(f" SELECT * FROM user_profiles WHERE hidden = 'no'")
        table_data = cursor.fetchall()

    except psycopg2.Error as err:
        print(err)

    finally:
        if connection:
            connection.close()
        return table_data



