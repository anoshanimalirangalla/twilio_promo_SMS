import urllib.request
import json
import random

# harry potter API
def get_char():
  url = "https://hp-api.onrender.com/api/characters"
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  
  char = random.randint(1,40)
  #print(char)
  if result[char]["wizard"]==True:
    return f"{result[char]['name']} is a wizard and the image is {result[char]['image']}"
  else :
    return f"{result[char]['name']} is not a wizard and the image is {result[char]['image']}"
