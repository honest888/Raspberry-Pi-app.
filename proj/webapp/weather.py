import json,requests 
try: 
    from .jsonFileReader import ConfigFileReader,WPA_Supplicant_Reader
except: 
    from jsonFileReader import ConfigFileReader,WPA_Supplicant_Reader
    pass



#  For geolocation based weather
# def weatherFunction():      
#     my_ip = requests.get("https://www.httpbin.org/ip").json()['origin'] 
#     my_location = requests.get(f"https://geolocation-db.com/json/{my_ip}?format=json").json()
#     latitude = my_location['latitude']
#     longitude = my_location['longitude']
#     api_key = 'ae6d37b4d05cadedfacb68d810b2cfc2' 
#     url  = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
#     weather_data = requests.get( url).json()
#     print(weather_data)
#     reader = ConfigFileReader()
#     reader.set_weather_data(weather_data) 


# for city based weather
def weatherFunction():
    reader = ConfigFileReader()
    print("-> Calling get_weather_data()")
    api_key  = reader.get_weather_data_api_key()
    city = reader.get_geo_location_city()
    print("-> Current city = ",city)
    api_key = reader.get_weather_data_api_key()
    url  = f'https://api.openweathermap.org/data/2.5/history?q={city}&appid={api_key}&units=metric'
    print("Weather API Response ")
    try:
        weather_data = requests.get(url).json()
        print(weather_data) 
        reader.set_weather_data(weather_data) 
    except Exception as e:
        print('Error getting weather data',str(e))
    
    
if __name__=="__main__"    :
    weatherFunction()   