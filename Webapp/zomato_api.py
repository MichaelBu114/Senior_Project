import sys
import requests
import mysql.connector

ZOMATO_API_KEY = "eeb2c8d6b993c20bfd856f1b092ea075"
GOOGLE_MAPS_API_KEY = "AIzaSyBTIYFA8avWuLBtGteyCUXhFdDFrqlS648"

ZOMATO_BASE_URL = "https://developers.zomato.com/api/v2.1/search"
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

config = {
    'user': 'root',
    'password' : 'snowflake6365stark',
    'host': 'mysql-development',
    'database': 'dp_sp',
    'auth_plugin': 'mysql_native_password'}


FORCE_ERROR = False

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

def api_request(lat, lon, meters, sorting, categories, establishments, cuisines, start=0):
    url = ZOMATO_BASE_URL+"?lat=%s&lon=%s&radius=%s&sort=%s&category=%s&establishment_type=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, sorting, categories, establishments, cuisines, start)
    print ("Calling " + url)
    header = {"user-key" : ZOMATO_API_KEY}
    response = requests.get(url, headers=header)
    if response.status_code != 200 or FORCE_ERROR:
        # Response error
        response_json['status'] = "ERROR"
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
        response_json[id]["menu"] = i["restaurant"]["menu_url"]
        response_json[id]["cuisine"] = i["restaurant"]["cuisines"]
        id += 1
    
    return len(response["restaurants"])
    
def search(zip, radius, sorting, user_id):
    global response_json
    
    # Get user parameters
    categories = mysql_database_call('getUserCategories', user_id)
    cuisines = mysql_database_call('getUserCuisines', user_id)
    establishments = mysql_database_call('getUserEstablishments', user_id)
    
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
