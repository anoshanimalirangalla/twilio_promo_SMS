import urllib.request
import json


#to get the city and the weather. 

def get_weather(city,country_code):
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid=cdae0d5319d984c40a8164638099431a"
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  temp = round(result["main"]["temp"]-273.15,2) #round up the temperature to 2 decimal places.
  return temp 
