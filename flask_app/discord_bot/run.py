# run.py
"""Gets Civil Twilight time from coordinates"""
import json
import time
import threading

import schedule
from geopy.geocoders import Nominatim

from .astral import CivilTwilight
from .webhook import Embed

civil_twilight = CivilTwilight()
geolactor = Nominatim(user_agent = "Civil Twilight Locator")


def read_config():
    """ Reads JSON file for various config values """
    with open("discord_config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data['webhooks'], data['schedule_time']

def get_country(latittude : str, longitude : str):
    """ Gets country from coordinates """
    location = geolactor.reverse(latittude + "," + longitude, language='en')#
    return location.raw['address']['country']


def read_json():
    """ Read JSON from URL """
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def parse_json(data : list):
    """ Parses JSON file and gets start time"""
    location_data = {}
    for location in data:
        lattitude = str(location['lat'])
        longitude = str(location['lng'])

        country = get_country(lattitude, longitude)
        times = civil_twilight.calculate(lattitude, longitude)

        if country not in location_data:
            location_data[country] = {}
        if location['site'] not in location_data[country]:
            location_data[country][location['site']] = []

        location_data[country][location['site']].append({
            "times": times
        })

    return location_data


def task(webhook : Embed):
    """ Runs task at 4pm everyday """
    data = read_json()
    location_data = parse_json(data)
    print("Sending information to Discord")
    for country in location_data:
        webhook.send_times(location_data[country], country) # Send the embed object


def schedule_task(webhook : Embed, schedule_time : str):
    """ Schedules a task to run at 4pm everyday """
    schedule.every().day.at(schedule_time).do(task, webhook=webhook)
    print("Scheduled task")

    while True:
        schedule.run_pending()
        time.sleep(1)


def run():
    """ Main function handler """
    print("Started bot")
    webhooks, schedule_time = read_config()
    webhook = Embed(
        treatment=webhooks['treatment_start_time'],
        companion=webhooks['companion_start_time']
    )

    scheduler_thread = threading.Thread(target=schedule_task, args=(webhook, schedule_time))
    scheduler_thread.daemon = True
    scheduler_thread.start()


if __name__ == "__main__":
    run()
