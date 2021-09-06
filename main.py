import requests
from twilio.rest import Client
from datetime import datetime
from decouple import config
import Constants as text


def callTwilio(text_to_send):

    account_sid = config('TWILIO_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    client.messages \
        .create(
        body=text_to_send,
        from_=config('SENDER_PHONE_NUMBER'),
        to=config('RECEIVER_PHONE_NUMBER')
    )


def checkWeatherAndSendText():

    URL = "https://api.openweathermap.org/data/2.5/onecall"
    weather_params = {
        "lat":34.112911,
        "lon":-78.797890,
        "appid": config('OWM_API_KEY'),
        "exclude":"current,minutely,daily"
    }

    response = requests.get(url=URL, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()

    willRain = False
    for hour in range(0,13):
        if weather_data["hourly"][hour]["weather"][0]["id"] < 700:
            willRain = True

    if willRain:
        callTwilio(text.RAIN_REMINDER)


def checkGarbageDayAndSendText():
    day = datetime.now().strftime("%A")
    if day == "Monday":
        callTwilio(f"{day}" + text.GARBAGE_DAYS["BLACK_GARBAGE"])
    elif day == "Thursday":
        callTwilio(f"{day}" + text.GARBAGE_DAYS["BLACK_AND_WHITE_GARBAGE"])


def testText():
    callTwilio(text.TEST_TEXT)


#testText() #use to make a test text first
checkGarbageDayAndSendText()
checkWeatherAndSendText()