# Check if Website is down
# Vikram Anantha
# Jun 11 2022


import requests
import smtplib
import sys
from helper_functions import send_email_v2
from datetime import datetime
import pytz

 
phone_number = "7819957110"
carrier = "att"
message = "HELMDown"

CARRIERS = {
            "att": "@mms.att.net",
            "tmobile": "@tmomail.net",
            "verizon": "@vtex.com",
            "sprint": "@page.nextel.com"
}


EMAIL = "helmlearning2020@gmail.com"
PASSWORD = "yerkkkxwiafkwyik"

def main():
    URL = "https://signup.helmlearning.com:5000/api/v1/resources/testerbester"
    
    try:
        r = requests.get(url = URL)
        data = r.json()
        print(data)
    except:
        send_message(phone_number, carrier, message)

def send_email():
    time_est = datetime.now(pytz.timezone('America/New_York') )
    send_email_v2(
        "HELM DOWN",
        "HELM is DOWN as of %s" % time_est,
        "vikramanantha@gmail.com"
    )
 
def send_message(phone_number, carrier, message):
    
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)

main()