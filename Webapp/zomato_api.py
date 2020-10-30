import sys
import requests

def search(ZIP, RADIUS, SORTING, CUISINES):
    ZOMATO_API_KEY = ""
    GOOGLE_MAPS_API_KEY = ""
    
    ZOMATO_BASE_URL = "https://developers.zomato.com/api/v2.1/search"
    GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    header = {"user-key" : ZOMATO_API_KEY}
    
    # Convert zip code into coordinates
    maps_response = requests.get(GOOGLE_MAPS_BASE_URL+"?address=%s&key=%s" % (ZIP, GOOGLE_MAPS_API_KEY)).json()
    lat = maps_response["results"][0]["geometry"]["location"]["lat"]
    lon = maps_response["results"][0]["geometry"]["location"]["lng"]
    
    # Call zomato search api
    meters = int(RADIUS) * 1609
    id = 0
    response_json = {}
    response_json["status"] = "OK"

    for start in ["0","21","41","61","81"]:
        print ("Calling " + ZOMATO_BASE_URL+"?lat=%s&lon=%s&radius=%s&sort=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, SORTING, CUISINES, start))
        response = requests.get(ZOMATO_BASE_URL+"?lat=%s&lon=%s&radius=%s&sort=%s&cuisines=%s&start=%s&count=20" % (lat, lon, meters, SORTING, CUISINES, start), headers=header).json()
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
        response_json['count'] = id

    return response_json
