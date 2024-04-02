import urllib.request
import json


def people_space():
  url = 'http://api.open-notify.org/astros.json' #url for opennotify API
  response = urllib.request.urlopen(url) #opening the url
  result = json.loads(response.read()) #reading the response
  #print(result)
  return f"{result['number']}"
