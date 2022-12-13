import json
import random
import mysql.connector
from geopy import distance


# connects to the db
def connect_to_database():
    # Connection to database
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='S4l4_sana',
        autocommit=True
    )
    return connection


# game starts:
def fetch_dialog(event, chname):
    connection = connect_to_database()
    sql = f'SELECT dialog from story where event="{event}" AND character_name="{chname}";'
    cursor_start = connection.cursor()
    cursor_start.execute(sql)
    result = cursor_start.fetchall()
    result = str(result[0])
    dialog1 = beautify_object(result)
    with open(dialog1) as dusk1:
        dialog1 = dusk1.readlines()
    return json.dumps(dialog1, default=lambda o: o.__dict__, indent=4)


# check if user in db already
def check_user_name(username):
    connection = connect_to_database()
    sql = f"SELECT screen_name FROM game WHERE screen_name='{username}';"
    cursor_check = connection.cursor()
    cursor_check.execute(sql)
    result = cursor_check.fetchall()
    if len(result) > 0:
        return False
    return True


# store values from flask
def store_values(value, input_type):
    values = dict()
    values.update({input_type: value})
    return values

# gets a starting location
def random_location():
    connection = connect_to_database()
    sql = f"SELECT latitude_deg, longitude_deg, elevation_ft from airport where airport.iso_country in("
    sql += "select objects.iso_country from objects);"
    cursor_location = connection.cursor()
    cursor_location.execute(sql)
    result = cursor_location.fetchall()
    index2 = -1
    for object in result:
        index2 += 1
    random_index = random.randint(1, index2)
    location = result[random_index]
    return location


# finds the locations for map api
def find_locations(degree):
    airports = []
    iso = []
    connection = connect_to_database()
    sql = f"SELECT {degree}, iso_country from airport where iso_country in("
    sql += "select iso_country from objects);"
    cursor_loc = connection.cursor()
    cursor_loc.execute(sql)
    result = cursor_loc.fetchall()
    if len(result) > 0:
        for row in result:
            if row[1] not in iso:
                airports.append(row[0])
                iso.append(row[1])
        return airports
    else:
        return False


def list_of_lat_long(deg_lang, deg_lon):
    lang_degrees = deg_lang
    long_degrees = deg_lon
    lat = []
    long = []
    latitudes = find_locations(lang_degrees)
    for row in latitudes:
        row = beautify_object(row)
        lat.append(row)
    longitudes = find_locations(long_degrees)
    for row in longitudes:
        row = beautify_object(row)
        long.append(row)
    result = [lat, long]
    return result


# checks if password exists
def check_password(password):
    connection = connect_to_database()
    sql = f"SELECT id FROM game WHERE password='{password}';"
    cursor_check = connection.cursor()
    cursor_check.execute(sql)
    result = cursor_check.fetchall()
    if len(result) > 0:
        return False


# creates user
def create_new_user(username, password):
    location_deg = random_location()
    location = get_loc_name(location_deg)
    connection = connect_to_database()
    sql = f"INSERT INTO game(location, screen_name, password, status) "
    sql += f"VALUES ('{location}','{username}', '{password}', 1);"
    cursor_create_new_user = connection.cursor()
    cursor_create_new_user.execute(sql)
    sql = f"UPDATE inventory SET player_id = (select id from game where screen_name = '{username}');"
    cursor_update_inv = connection.cursor()
    cursor_update_inv.execute(sql)
    return True

def get_loc_name(degs):
    connection = connect_to_database()
    sql = f"select iso_country from airport where latitude_deg={degs[0]} and longitude_deg={degs[1]};"
    cursor_get_iso = connection.cursor()
    cursor_get_iso.execute(sql)
    result = cursor_get_iso.fetchall()
    result = beautify_object(result)
    return result



# gets object for player to search
def get_and_rand_object():
    connection = connect_to_database()
    indexes = []
    i = 0
    sql = f"SELECT name FROM objects;"
    cursor_is_obj = connection.cursor()
    cursor_is_obj.execute(sql)
    result = cursor_is_obj.fetchall()
    index_for_random = len(result) - 1

    while i < 8:
        index = random.randint(0, index_for_random)
        if index not in indexes:
            indexes.append(index)
            i += 1

    sql = f"SELECT name FROM objects;"
    cursor_is_obj = connection.cursor()
    cursor_is_obj.execute(sql)
    result = cursor_is_obj.fetchall()
    objects_list = []

    for num in indexes:
        stuff_to_find = result[num]
        stuff_to_find = beautify_object(stuff_to_find)
        if stuff_to_find not in objects_list:
            objects_list.append(stuff_to_find)
        if len(objects_list) == 4:
            break
        add_to_inv(objects_list)
    return objects_list

#adds object to fetchlistdb

def add_to_inv(itemlist):
    connection = connect_to_database()
    for row in itemlist:
        sql = f'UPDATE objects SET status=0 WHERE name="{row}";'
        alter_stat = connection.cursor()
        alter_stat.execute(sql)
    return True

# gives the hints of objects
def hint_country(items):
    connection = connect_to_database()
    sql = f"SELECT hint FROM objects WHERE name='{items}'"
    hints_fetch = connection.cursor()
    hints_fetch.execute(sql)
    hints_get = hints_fetch.fetchall()
    for row in hints_get:
        hint = beautify_object(row)
        with open(hint) as dusk1:
            hint = dusk1.readlines()
    return hint


def fly_to_a_country(lat, lon):
    connection = connect_to_database()
    sql = f"SELECT name FROM airport WHERE latitude_deg='{lat}' AND longitude_deg='{lon}';"
    cursor_country = connection.cursor()
    cursor_country.execute(sql)
    result = cursor_country.fetchall()
    result = beautify_object(result)
    return result


def calculate_co2(location, country):
    connection = connect_to_database()
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE iso_country='{location}';"
    cursor_country = connection.cursor()
    cursor_country.execute(sql)
    cord1 = cursor_country.fetchall()
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE iso_country='{country}';"
    cursor_country = connection.cursor()
    cursor_country.execute(sql)
    cord2 = cursor_country.fetchall()
    distance_km = distance.distance(cord1[0:1], cord2[0:1]).km
    result = 3.16 * distance_km
    return result


def update_co2(username, co2):
    co2 = float(co2)
    connection = connect_to_database()
    sql = f"SELECT co2_consumed FROM game WHERE screen_name='{username}';"
    cursor_find = connection.cursor()
    cursor_find.execute(sql)
    prev_co2 = cursor_find.fetchall()
    prev_co2 = beautify_object(prev_co2)
    new_co2 = float(prev_co2) + co2
    sql = f"UPDATE game SET co2_consumed = {new_co2} WHERE screen_name='{username}';"
    cursor_co2 = connection.cursor()
    cursor_co2.execute(sql)
    return True


def find_loc(username):
    connection = connect_to_database()
    sql = f"SELECT location FROM game WHERE screen_name='{username}';"
    cursor_userdata = connection.cursor()
    cursor_userdata.execute(sql)
    result = cursor_userdata.fetchall()
    result = beautify_object(result)
    return result


def change_loc(username, country):
    connection = connect_to_database()
    sql = f"UPDATE game SET location = '{country}' where screen_name='{username}';"
    cursor_loc = connection.cursor()
    cursor_loc.execute(sql)
    return True


# searches the country and object from database
def find_object(iso_country):
    connection = connect_to_database()
    sql = f"SELECT name FROM objects where iso_country='{iso_country}';"
    cursor_location = connection.cursor()
    cursor_location.execute(sql)
    result = cursor_location.fetchall()
    return result


# make an object to a string
def beautify_object(object_func):
    object_func = str(object_func)
    object_func = object_func.replace(",", "")
    object_func = object_func.replace(" ", "")
    object_func = object_func.replace("'", "")
    object_func = object_func.replace("(", "")
    object_func = object_func.replace(")", "")
    object_func = object_func.replace("[", "")
    object_func = object_func.replace("]", "")
    return object_func


# check if item in the list
def check_list(item_found, objects_to_find):
    inventory_func = []
    if item_found in objects_to_find:
        return True
    else:
        return False


# to limit spaghetti, a function that checks the object found
def search_object_from(obj_func, iso_code_func, find_items_func, inventory_func):
    obj_func = find_object(iso_code_func)
    obj_func = beautify_object(obj_func)
    print(f"Congratulations, you found {obj_func}!")

    if check_list(obj_func, find_items_func) == True and obj_func not in inventory_func:
        inventory_func.append(obj_func)
        print(f"Your inventory has now {len(inventory_func)} items\n"
              f"{inventory_func}")
        print(f"objects you must find:{find_items_func}")
    else:
        print(f"couldn't add {obj_func} to the list")
        print(f"objects you must find:{find_items_func}")


def fetch_co2(username):
    connection = connect_to_database()
    sql = f"SELECT co2_consumed FROM game WHERE screen_name='{username}';"
    cursor_co2 = connection.cursor()
    cursor_co2.execute(sql)
    result = cursor_co2.fetchall()
    return result


def leaderboard():
    connection = connect_to_database()
    sql = f"SELECT screen_name, co2_consumed FROM game ORDER BY co2_consumed;"
    cursor_lead = connection.cursor()
    cursor_lead.execute(sql)
    result = cursor_lead.fetchall()
    board = []
    for stuff in result:
        board.append(stuff)
    return board


# checks password
def check_password(password):
    connection = connect_to_database()
    sql = f"SELECT id FROM game WHERE password='{password}';"
    cursor_check = connection.cursor()
    cursor_check.execute(sql)
    result = cursor_check.fetchall()
    if len(result) > 0:
        return False

    return True