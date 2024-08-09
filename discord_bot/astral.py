# astral.py
""" Script to generate civil twilight start and end times for multiple locations """

from datetime import datetime, timedelta
import ephem

class CivilTwilight:
    """ Object for ephem library to handle multiple locations """
    def __init__(self):
        self.sun = ephem.Sun()
        self.observer = ephem.Observer()
        self.observer.pressure = 0
        self.arrive_before_time = 45

    def __get_timestamp(self, time : ephem.Date):
        """ Converts ephem.Date to time string """
        return ephem.localtime(time).strftime("%H:%M:%S %p")

    def __get_shift_start(self, time : ephem.Date):
        """ Converts ephem.Date to time and subtracts 45 minutes """
        converted_time = ephem.localtime(time)
        converted_time -= timedelta(minutes=self.arrive_before_time)
        return converted_time.strftime("%H:%M:%S %p")

    def calculate(self, lat: str, lon: str):
        """ Takes lat and lon coordinates and returns civil twilight start and end time in local time """
        self.observer.lat = lat
        self.observer.lon = lon
        self.observer.horizon = '-6'
        self.observer.date = datetime.utcnow().replace(hour=12, minute=0, second=0)

        twilight_start = self.observer.next_setting(self.sun, use_center=True)
        twilight_end = self.observer.next_rising(self.sun, use_center=True)

        return {
            "twilight_start": self.__get_timestamp(twilight_start),
            "twilight_end": self.__get_timestamp(twilight_end),
            "companion_start_time": self.__get_shift_start(twilight_start)
        }
