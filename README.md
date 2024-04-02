# Twilio SMS flask web application

## Objective
This application can fetch data from multiple APIs, construct a message, and send it to many contacts through the platform Twilio.(ideal for promotional campaigns)
[Bulk messaging]

For the purpose of implementing the data fetching from various APIs, I have used [Harry Potter API](https://hp-api.onrender.com/api/characters), [Open Notify](http://open-notify.org/) for ISS location and 
[OpenWeather](https://openweathermap.org/) for weather information. 

The Flask web application is facilitated with one button for sending messages. 

Once the message is sent, it is sent successfully if notified through a flash message. 

Finally, the messages' details are logged into a JSON file. 

## Step 1 - Fetching data from HP API. 

Here, I have extracted/fetched data from Harry Potter API and stored it in a string to pick a random character, a wizard. If the character is a wizard, then it will return a f string saying the name of the character and the image. These data are fetched from the API. 

```python
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
```
## Step 2 - Fetching data from Open Notify API

```python
import urllib.request
import json


def people_space():
  url = 'http://api.open-notify.org/astros.json' #url for opennotify API
  response = urllib.request.urlopen(url) #opening the url
  result = json.loads(response.read()) #reading the response
  #print(result)
  return f"{result['number']}"
```

## Step 3 - Fetching data from Openweather API

```python
import urllib.request
import json


#to get the city and the weather. 

def get_weather(city,country_code):
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid=cdae0d5319d984c40a8164638099431a"
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  temp = round(result["main"]["temp"]-273.15,2) #round up the temperature to 2 decimal places.
  return temp
```

## step 4 - Flask application and importing addtional pages to main.py

```python

import urllib.request
import json
import random
import os
from flask import Flask, render_template, request,flash , redirect, url_for,session
from twilio.rest import Client
from weather import get_weather
from hp import get_char
from space import people_space

app = Flask(__name__)
app.secret_key = os.urandom(24) # setting a secreat key for session management
app.config['SESSION_TYPE'] = 'filesystem' # configure session to use filesystem

# Twilio credentials
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# we are creating our own data base. 

people = {
  "Shamal":{
    "name" : "Shamal",
    "contact": "+16________",
    "city": "London",
    "country_code": "CA",
    "lucky_number": random.randint(1,10)
  },
  "Thenuka":{
    "name" : "Thenuka",
    "contact": "+13________",
    "city": "Alliston",
    "country_code": "CA",
    "lucky_number": random.randint(1,10)
  },
      "Anosha":{
        "name" : "Anosha",
        "contact": "+14________",
        "city": "Sudbury",
        "country_code": "CA",
        "lucky_number": random.randint(1,10)
  }
  
}


@app.route('/', methods=['GET', 'POST'])
def send_sms():
  messages = []
  if request.method == 'POST':
    try:
      for key,value in people.items():
        msg = f'Hi {value["name"].title()}, your lucky number is {value["lucky_number"]}. The current city you live in, is {value["city"].title()} and the temperature is {get_weather(value["city"],value["country_code"])}. Do you know at this moment the number of people in Space(ISS) is {people_space()}. Fan of Harry Potter? Haha. See this!! {get_char()}.'
  
        print(msg)
        message = client.messages \
                  .create(
                       body=msg,
                       from_='+16504602690',
                       to=value["contact"]

                  )
        print(message.sid)
        messages.append({"recipient":value["name"],"message":msg})

      with open('messages.json', 'w') as json_file:
        json.dump(messages, json_file)

      flash("SMS sent successfully!",'success') #flash is used to display a message to the user.
    except Exception as e:
      flash(f"Failed to send the SMS: {str(e)}",'error') 
    return redirect(url_for('send_sms'))
    
  return render_template('index.html', messages=messages)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

```
## Step 5 -  HTML page for web application 

```html
<!DOCTYPE html>
<html>
<head>
    <title>Send Message</title>
</head>
<body>
  <!--title of the page -->
    <h1>To Send the Message</h1>
  <!-- form a button to send the message -->
    <form method="post">
        <button type="submit"><i>Click Here</i></button>
    </form>
  <!-- display the flashed message if any-->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
  <!-- unordered list to display the message -->
  <ul>
    <!-- loop through the messages -->
                {% for category, message in messages %}
    <!-- list item to display the message -->
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
    </ul>
        {% endif %}
    {% endwith %}
</body>
</html>

```

