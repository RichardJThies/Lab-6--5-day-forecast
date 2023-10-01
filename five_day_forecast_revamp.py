import os
import requests
from datetime import datetime
from pprint import pprint
"""Use the forecast API to create a detailed, neatly formatted 5-day forecast, for anywhere the user 
chooses. Ask the user for the location.
Make sure your API key is not coded into your program. Your program should read the key from an 
environment variable. 
Use a query parameter dictionary in the request.
Your forecast should show the temperature and unit (your choice of F or C), weather description, and 
wind speed for every three hour interval, over the next 5 days.
Your program should handle errors. What type of errors do you anticipate? How will you deal with them?"""

url = f'https://api.openweathermap.org/data/2.5/forecast' #"forecast" instead of "weather"
key = os.environ.get('WEATHER_KEY')#returns None if key doesn't exist
print(key) #only needed for verification during development

def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)#getting the tuple from get_current_weather()and storing
    if error:# could be made more specific for incorrect city name or country code
        print('Sorry, could not get weather')
    else:
        current_temp = get_temp(weather_data)
        print(f'The current temp is {current_temp}F.')

def get_location():#figure out what location for current weather
    city, country = '', ''
    while len(city) == 0:#loop to stop user from entering blank
        city = input('Enter the city: ').lower().strip()

    while len(country) != 2 or not country.isalpha():#must use !=, not "is not". Stops user from entering anything other than 2 letters
        country = input('Enter the 2-letter country code: ').lower().strip()

    location = f'{city},{country}'#formats the input to be used into URL, no spaces
    return location

def get_current_weather(location, key):#make request for the weather
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key}#APIs will return an error or a default if there are typos here. Dictionary format
        response = requests.get(url, params=query)#better way instead of f-sstrings for URLs
        response.raise_for_status() #exception if 400 or 500 errors are encountered
        data = response.json()# if the response is not json, there will be error
        return data, None#returns tuple of the response data, and the exception, which is None because the program didn't error
    except Exception as ex:
        print(ex)
        print(response.text)# for debugging. Use logging instead?
        return None, ex#returns tuple with the data, None, and the exception which has a value because an error tripped
    
def get_temp(data):#process information received from request into data
    try:
        list_of_forescasts = data['list']#pulling out of dictionary converted from json
        for forecast in list_of_forescasts:#loop to process a list returned by the api call
            temp = forecast['main']['temp']#pulling out of dictionary converted from json
            timestamp = forecast['dt']
            description = forecast['weather'][0]['description']# need a 0, to indicate first thing in the list, although there is only 1 in the list in this case
            wind_speed = forecast['wind']['speed']#pulling out the windspeed
            forecast_date = datetime.fromtimestamp(timestamp)#converting the 'dt' timestamp into human readable information
            # print(temp, forecast_date)
            print(f'At {forecast_date} the temperature will be {temp}F, with {description}, and a wind speed of {wind_speed} mph')
        # temp = weather_data['main']['temp']
        return temp
    except KeyError:#keyError is a key that doesn't exist
        print('This data is not in expected format')
        return 'Unknown'#returns a string to fit into the string output

if __name__ == '__main__':
    main()


#export WEATHER_KEY={REPLACEW/KEY}#setting temporarily wont with run button
#echo $WEATHER_KEY 6c3d42ae6b790d3b3dd46ec7b3317bb9
#python five_day_forecast.py #running file in git bash