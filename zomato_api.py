import sys
import os
import requests

ZOMATO_API_KEY = ""
GOOGLE_MAPS_API_KEY = ""
ZIP = ""

ZOMATO_BASE_URL = "https://developers.zomato.com/api/v2.1/geocode"
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def test_location_call():
    header = {"user-key" : ZOMATO_API_KEY}
    
    # Convert zip code into coordinates
    maps_response = requests.get(GOOGLE_MAPS_BASE_URL+"?address=%s&key=%s" % (ZIP, GOOGLE_MAPS_API_KEY)).json()
    lat = maps_response["results"][0]["geometry"]["location"]["lat"]
    lon = maps_response["results"][0]["geometry"]["location"]["lng"]
    
    # Call zomato geocode api
    response = requests.get(ZOMATO_BASE_URL+"?lat=%s&lon=%s" % (lat, lon), headers=header).json()
    
    print "Found %s locations for zip code %s\n" % (len(response["nearby_restaurants"]), ZIP)
    
    for i in response["nearby_restaurants"]:
        print "Name: " + i["restaurant"]["name"]
        print "URL: " + i["restaurant"]["url"]
        print "Address: " + i["restaurant"]["location"]["address"]
        print "Coordinates: " + i["restaurant"]["location"]["latitude"] + ", " + i["restaurant"]["location"]["longitude"]
        print "Currency: " + i["restaurant"]["currency"]
        print "Menu URL: " + i["restaurant"]["menu_url"]
        print "Delivery: " + str(i["restaurant"]["R"]["has_menu_status"]["delivery"])
        print "Takeaway: " + str(i["restaurant"]["R"]["has_menu_status"]["takeaway"])
        
        online = "Yes" if i["restaurant"]["has_online_delivery"] == 1 else "No"
        delivery = "Yes" if i["restaurant"]["is_delivering_now"] == 1 else "No"
        reservation = "Yes" if i["restaurant"]["is_table_reservation_supported"] == 1 else "No"
        booking = "Yes" if i["restaurant"]["has_table_booking"] == 1 else "No"
        grocery = "Yes" if i["restaurant"]["R"]["is_grocery_store"] == "true" else "No"
        
        print "Has Online Delivery: " + online
        print "Delivering Now: " + delivery
        print "Is Table Revervation Supported: " + reservation
        print "Has Table Booking: " + booking
        print "Is Grocery Store: " + grocery
        
        print "\n"
    
test_location_call()