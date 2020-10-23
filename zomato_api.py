import sys
import requests

ZOMATO_API_KEY = "eeb2c8d6b993c20bfd856f1b092ea075 "
GOOGLE_MAPS_API_KEY = "AIzaSyBTIYFA8avWuLBtGteyCUXhFdDFrqlS648"

ZOMATO_BASE_URL = "https://developers.zomato.com/api/v2.1/search"
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# These values will eventually be passed to this script
ZIP = sys.argv[1] # First argument to script
RADIUS = 5 # Miles
SORTING = "real_distance" # Sort by distance
CUISINES = "" # Filter by one or more cuisines

def test_location_call():
    header = {"user-key" : ZOMATO_API_KEY}
    
    # Convert zip code into coordinates
    maps_response = requests.get(GOOGLE_MAPS_BASE_URL+"?address=%s&key=%s" % (ZIP, GOOGLE_MAPS_API_KEY)).json()
    lat = maps_response["results"][0]["geometry"]["location"]["lat"]
    lon = maps_response["results"][0]["geometry"]["location"]["lng"]
    
    # Call zomato search api
    meters = RADIUS * 1609
    id = 0
    response_json = {}
    response_json["status"] = "OK"

    for start in ["0","21","41","61","81"]:
        response = requests.get(ZOMATO_BASE_URL+"?lat=%s&lon=%s&radius=%s&sort=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, SORTING, CUISINES, start), headers=header).json()
        print ("Calling " + ZOMATO_BASE_URL+"?lat=%s&lon=%s&radius=%s&sort=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, SORTING, CUISINES, start))
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

    print ("\n")
    print (response_json)
    
test_location_call()
