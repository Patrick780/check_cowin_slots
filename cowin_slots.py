import http.client
import json
import datetime
import sys
import time
from os import system
from beepy import beep
import config

pin_code = config.pin_code
refresh_time = config.refresh_time
days = config.days
age = config.age


def print_report(session_details, center_details):
        system('clear')
        print(f"Center Id           :{center_details['center_id']}\n"
              f"Name                :{center_details['name']}\n"
              f"Address             :{center_details['address']}\n"
              f"Date                :{session_details['date']}\n"
              f"Available capacity  :{session_details['available_capacity']}\n"
              f"Min age limit       :{session_details['min_age_limit']}\n"
              f"Vaccine             :{session_details['vaccine']}")
        while True: beep(sound=4)


def check_slot(day):
    try:
        conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
        conn.request("GET", f"/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={day}")
        response = json.loads(conn.getresponse().read().decode("utf-8"))
        [[print_report(session, center) if session['available_capacity'] > 0 and session['min_age_limit'] in age else print(
            'Already booked') for session in center['sessions']] for center in response['centers']] if len(
            response['centers']) > 0 else print(f"\t{day}: No centers available")
    except:
        print('\tCowin API is not reachable right now')



dates = [(datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%d-%m-%Y') for day in range(days)]
iterations = 1
while True:
    print(f'\nIteration: {iterations}, {datetime.datetime.now().strftime("%H:%M")}')
    [check_slot(day) for day in dates]
    iterations += 1
    while refresh_time > 0:
        print(f'Checking again in {refresh_time} seconds..', end='\r')
        refresh_time -= 1
        time.sleep(1)
    refresh_time = config.refresh_time
