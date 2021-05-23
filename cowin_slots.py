import http.client
import json
import datetime
import time
from os import system
from beepy import beep
import config

pin_codes = config.pin_codes
days = config.days
age = config.age
doses = config.dose
refresh_time = 30 if config.refresh_time < 30 else config.refresh_time


def print_report(session_details, center_details, dose, pin_code):
    capacity = session_details['available_capacity_dose1'] if dose == 1 else session_details['available_capacity_dose2']
    system('clear')
    print(f"Center Id           :{center_details['center_id']}\n"
          f"Name                :{center_details['name']}\n"
          f"Address             :{center_details['address']}\n"
          f"Pin Code            :{pin_code}\n"
          f"Date                :{session_details['date']}\n"
          f"Available capacity  :{capacity}, Dose: {dose}\n"
          f"Min age limit       :{session_details['min_age_limit']}\n"
          f"Vaccine             :{session_details['vaccine']}")
    print('\nClick here https://www.cowin.gov.in/home to book your appointment')
    while True: beep(sound=4)


def check_slot(dates, pin_code):
    date_param = ','.join(dates)
    try:
        conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
        conn.request("GET", f"/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={date_param}")
        response = json.loads(conn.getresponse().read().decode("utf-8"))
        if len(response['centers']) > 0:
            for center in response['centers']:
                for session in center['sessions']:
                    if session['min_age_limit'] in age:
                        for dose in doses:
                            if dose == 1 and session["available_capacity_dose1"] > 0:
                                print_report(session, center, dose, pin_code)
                            elif dose == 2 and session["available_capacity_dose2"] > 0:
                                print_report(session, center, dose, pin_code)
                            else:
                                print(f"\t{session['date']} : Center already booked   >> {center['name']}")
                    else:
                        print(f"\t{session['date']} : Not available for {age[0]}+   >> {center['name']}")
        else:
            print(f'\tNo centers available at {pin_code} for {len(days)} upcoming days')
    except:
        print('\tCowin API is not reachable right now')


days = [(datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%d-%m-%Y') for day in range(days)]
iterations = 1
while True:
    system('clear')
    print(f'Iteration: {iterations}, {datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")}')
    for pincode in pin_codes:check_slot(days, pincode)
    iterations += 1
    while refresh_time > 0: print(f'Checking again in {refresh_time} seconds..', end='\r'); refresh_time -= 1; time.sleep(1)
    refresh_time = config.refresh_time
