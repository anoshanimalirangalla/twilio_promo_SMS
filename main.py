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
