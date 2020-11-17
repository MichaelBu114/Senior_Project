import sys
import requests
import mysql.connector

from config import *

ZOMATO_BASE_URL = "https://developers.zomato.com/api/v2.1"
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

config = {
    'user': MYSQL_USERNAME,
    'password' : MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': MYSQL_DATABASE,
    'auth_plugin': 'mysql_native_password'}


FORCE_ERROR = False
header = {"user-key" : ZOMATO_API_KEY}

def check_response(response):
    if response.status_code != 200 or FORCE_ERROR:
        # Response error
        response_json['status'] = "ERROR"
        return -1

def mysql_database_call(function, user_id):
    categories = None
    connection = None
    result = ""
    #print("Executing %s ..." % function)
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    categories = cursor.callproc(function, args = [user_id])
    for r in cursor.stored_results():
        for i in list(r.fetchall()):
            result += str(i[0]) + ","
    connection.close()
    return result

def restaurant_details(res_id):
    global response_json
    
    response_json = {'status' : 'OK', 'location' : {}, 'user_rating' : {}}
    url = ZOMATO_BASE_URL+"/restaurant?res_id=%s" % res_id
    print ("Calling " + url)
    response = requests.get(url, headers=header)
    
    if check_response(response) == -1:
        return response_json
    
    response = response.json()
    
    response_json["id"] = response["id"]
    response_json["name"] = response["name"]
    response_json["phone_numbers"] = response["phone_numbers"].split(", ") # Convert string of phone numbers into list
    response_json["address"] = response["location"]["address"]
    response_json["city"] = response["location"]["city"]
    response_json["latitude"] = response["location"]["latitude"]
    response_json["longitude"] = response["location"]["longitude"]
    response_json["locality_verbose"] = response["location"]["locality_verbose"]
    response_json["cuisines"] = response["cuisines"]
    response_json["timings"] = response["timings"]
    response_json["average_cost_for_two"] = response["average_cost_for_two"]
    response_json["price_range"] = response["price_range"]
    response_json["currency"] = response["currency"]
    response_json["highlights"] = response["highlights"]
    response_json["aggregate_rating"] = response["user_rating"]["aggregate_rating"]
    response_json["rating_text"] = response["user_rating"]["rating_text"]
    response_json["menu_url"] = response["menu_url"]
    response_json["featured_image"] = response["featured_image"]
    response_json["has_online_delivery"] = response["has_online_delivery"]
    response_json["is_delivering_now"] = response["is_delivering_now"]
    response_json["is_table_reservation_supported"] = response["is_table_reservation_supported"]
    response_json["has_table_booking"] = response["has_table_booking"]
    response_json["establishment"] = response["establishment"]
    
    return response_json

def api_request(lat, lon, meters, sorting, categories, establishments, cuisines, start=0):
    url = ZOMATO_BASE_URL+"/search?lat=%s&lon=%s&radius=%s&sort=%s&category=%s&establishment_type=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, sorting, categories, establishments, cuisines, start)
    print ("Calling " + url)
    response = requests.get(url, headers=header)
    if check_response(response) == -1:
        return -1
    
    response = response.json()
    id = len(response_json) - 2
    
    # Parse
    for i in response["restaurants"]:
        response_json[id] = {} 
        response_json[id]["id"] = i["restaurant"]["id"]
        response_json[id]["coordinates"] = {}
        response_json[id]["name"] = i["restaurant"]["name"]
        response_json[id]["url"] = i["restaurant"]["url"]
        response_json[id]["phone_number"] = i["restaurant"]["phone_numbers"]
        response_json[id]["address"] = i["restaurant"]["location"]["address"]
        response_json[id]["coordinates"]["lat"] = i["restaurant"]["location"]["latitude"]
        response_json[id]["coordinates"]["lng"] = i["restaurant"]["location"]["longitude"]
        response_json[id]["currency"] = i["restaurant"]["currency"]
        response_json[id]["menu_url"] = i["restaurant"]["menu_url"]
        response_json[id]["cuisine"] = i["restaurant"]["cuisines"]
        response_json[id]["aggregate_rating"] = i["restaurant"]["user_rating"]["aggregate_rating"]
        response_json[id]["featured_image"] = i["restaurant"]["featured_image"]
        response_json[id]["rating_icon"] = str(round(float(i["restaurant"]["user_rating"]["aggregate_rating"])))
        id += 1

    return len(response["restaurants"])
    
def search(zip, radius, sorting, user_id, userCat = None, userCus = None, userEst = None):
    global response_json
    
    # Get user parameters
    if user_id != 0: 
        categories = mysql_database_call('getUserCategories', user_id)
        cuisines = mysql_database_call('getUserCuisines', user_id)
        establishments = mysql_database_call('getUserEstablishments', user_id)
    else:
        categories = userCat
        cuisines = userCus
        establishments = userEst

    # Convert zip code into coordinates
    maps_response = requests.get(GOOGLE_MAPS_BASE_URL+"?address=%s&key=%s" % (zip, GOOGLE_MAPS_API_KEY)).json()
    lat = maps_response["results"][0]["geometry"]["location"]["lat"]
    lon = maps_response["results"][0]["geometry"]["location"]["lng"]
    meters = int(radius) * 1609
    
    response_json = {'status' : 'OK', 'count' : 0}
    
    total_count = 0
    start = 21

    items = api_request(lat, lon, meters, sorting, categories, establishments, cuisines)
    response_json['count'] += items
    
    while items == 20 and start < 101:
        items = api_request(lat, lon, meters, sorting, categories, establishments, cuisines, start)
        response_json['count'] += items
        start += 20
    
    return response_json
