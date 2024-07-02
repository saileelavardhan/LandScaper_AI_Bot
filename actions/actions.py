# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetCityInfo(Action):

    def name(self) -> Text:
        return "action_get_city_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract the city name from the user message
        city = tracker.get_slot('city')

        # Your API Ninja key
        api_key = ''
        url = "https://api.api-ninjas.com/v1/city?name={}".format(city)
        
        headers = {
            'X-Api-Key': api_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code ==  requests.codes.ok:
            data = response.json()
            if data:
                city_info = data[0]  # assuming the API returns a list
                city_name = city_info.get('name')
                country = city_info.get('country')
                population = city_info.get('population')
                latitude = city_info.get('latitude')
                longitude = city_info.get('longitude')

                message = (f"City: {city_name}\n"
                           f"Country: {country}\n"
                           f"Population: {population}\n"
                           f"longitude: {longitude}\n"
                           f"latitude: {latitude}")

                dispatcher.utter_message(text=f"the {city} is resided in {country}with population {population} and parameters {longitude} and {latitude} ")
            else:
                dispatcher.utter_message(text=f"No information found for city: {city}")
        else:
            dispatcher.utter_message(text="Failed to retrieve city information. Please try again later.")

        return []
