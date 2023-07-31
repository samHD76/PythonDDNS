import os
import requests
import time
from datetime import datetime


waitTimesec = os.environ['wait']
email =  os.environ['email']
domain = os.environ['domain']
zoneID = os.environ['zoneID']
globalAPI = os.environ['globalAPI']
ip = 0

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': f"{email}",
    'X-Auth-Key': f'{globalAPI}',
    }


print("getting current public IP")

print("Current public IP address:", ip)


def updateCF(identifier):
    global headers
    global ip
    global zoneID
    print("*** found DNS entry with same domain -> updating it . . . ")
    json_data = {
    'content': f'{ip}',
    'name': f'{domain}',
    'proxied': False,
    'type': 'A',
    'comment': 'DDNS',
    }

    try:

        response = requests.put(
        f'https://api.cloudflare.com/client/v4/zones/{zoneID}/dns_records/{identifier}',
        headers=headers,
        json=json_data,
        )
    except:
        print("an error occurred, maybe there is no internet connection?")    
    print(response.text)

def checkCF():          #checking cloudflare to prevent duplicate entry
    global headers
    global ip
    ip = requests.get("https://api.ipify.org").text
    print("****checking cloudflare to prevent duplicate entry****")

    try:
        response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zoneID}/dns_records', headers=headers)
        response = response.json()
    except:
        print("an error occurred, maybe there is no internet connection?")
    
    for i in response["result"]:
        if i["name"] == domain:
            updateCF(i["id"])
            return
    pushtoCF()

def pushtoCF():
    global headers
    json_data = {
    'content': f'{ip}',
    'name': f'{domain}',
    'proxied': False,
    'type': 'A',
    'comment': 'DDNS',
    }

    try:

        response = requests.post(
        f'https://api.cloudflare.com/client/v4/zones/{zoneID}/dns_records',
        headers=headers,
        json=json_data,
        )
    except:
        print("an error occurred, maybe there is no internet connection?")

    print(response.text)


while 1:
    checkCF()
    print(f"time : {datetime.now()}DNS record has been updated .  waiting for {int(waitTimesec)} seconds")
    time.sleep(int(waitTimesec))