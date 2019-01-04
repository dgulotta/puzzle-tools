"""
Tests to make sure that the sites that we scrape haven't changed their
data formats.
"""

import unittest
from datetime import date
from time import sleep
from puzzletools.enumerations_web import *
from puzzletools.enumerations_web import _us_states
from puzzletools.subway import *

def canonicalize(item):
    if isinstance(item,list):
        return set(item)
    else:
        return item

class WebTest(unittest.TestCase):

    def check_exists(self,it):
        try:
            return next(it)
        except StopIteration:
            self.fail('not found')

    def check_data(self, enum, data):
        closest = None
        closest_fails = None
        for item in enum.items:
            fails = [k for k,v in data.items() if canonicalize(getattr(item, k)) != canonicalize(v)]
            if not fails:
                return
            if closest is None or len(fails) < len(closest_fails):
                closest = item
                closest_fails = fails
        self.fail('Could not find any item of {} matching:\n{}.\nClosest is:\n{}\nFailed to match: {}'
            .format(enum.__name__, data, closest, closest_fails))

    def test_countries(self):
        sleep(1)
        self.check_data(Country, {
            'name': 'United States of America',
            'alpha2': 'US',
            'alpha3': 'USA',
            'numeric': 840,
            'independent': True
        })

    def test_states(self):
        sleep(1)
        class State:
            items = _us_states()
        self.check_data(State,{
            'name': 'Massachusetts',
            'abbr': 'MA',
            'capital': 'Boston',
            'statehood': date(1788,2,6)
        })

    def test_resistors(self):
        sleep(1)
        self.check_data(ResistorColor, {
            'name': 'Red',
            'code': 'RD',
            'ral': 3000,
            'sigfig': 2,
            'log_multiplier': 2,
            'tolerance_letter': 'G',
            'temp_coeff': 50,
            'temp_coeff_letter': 'R'
        })

    def test_zodiac(self):
        sleep(1)
        self.check_data(Zodiac, {
            'name': 'Capricorn',
            'start': datetime.date(1900,12,22),
            'end': datetime.date(1900,1,20)
        })

    def test_currency(self):
        sleep(1)
        self.check_data(Currency, {
            'code': 'CHF',
            'number': 756,
            'name': 'Swiss franc',
            'countries': ['Switzerland','Liechtenstein']
        })

    def test_language(self):
        sleep(1)
        self.check_data(Language, {
            'name': 'English',
            'native_name': 'English',
            'code': 'en'
        })

    def test_london_wiki(self):
        sleep(1)
        self.check_data(LondonUnderground, {
            'name': 'London Bridge',
            'lines': ['Northern','Jubilee']
        })

    def test_mbta_wiki(self):
        sleep(1)
        self.check_data(MBTAStation, {
            'name': 'Kendall/MIT',
            'lines': ['Red Line']
        })

    def test_paris_wiki(self):
        sleep(1)
        self.check_data(ParisMetro, {
            'name': 'Jussieu',
            'code': '12-07',
            'lines': ['7','10']
        })

    def test_washington_wiki(self):
        sleep(1)
        self.check_data(WashingtonMetro,{
            'name': 'Crystal City',
            'lines': ['Blue','Yellow'],
        })

    def test_airport(self):
        self.check_data(Airport, {
            'name': 'General Edward Lawrence Logan International Airport',
            'city': 'Boston',
            'country': 'United States',
            'iata': 'BOS',
            'icao': 'KBOS',
            'latitude': 42.36429977,
            'longitude': -71.00520325,
            'altitude': 20,
            'utcoff': -5.0,
            'dst': 'A',
            'timezone': 'America/New_York'
        })

    def test_airline(self):
        self.check_data(Airline, {
            'name': 'Turkmenistan Airlines',
            'alias': 'Turkmenhovayollary',
            'iata': 'T5',
            'icao': 'TUA',
            'callsign': 'TURKMENISTAN',
            'country': 'Turkmenistan',
            'active': True
        })

    def test_stock(self):
        self.check_data(Stock, {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'ipo_yr': 1980,
            'sector': 'Technology',
            'industry': 'Computer Manufacturing',
            'exchange': 'NASDAQ',
        })

    def test_mit(self):
        data=mit_subject_listing_by_course(18)
        c=self.check_exists(s[1] for s in data if s[0]=='18.726')
        self.assertEqual(c,'Algebraic Geometry II')


    def test_mbta_transitland(self):
        sleep(1)
        self.check_data(MBTA.stations, {
            'name': 'Kendall/MIT',
            'lines': ['Red Line']
        })

    def test_ny_transitland(self):
        sleep(1)
        self.check_data(NewYork.stations, {
            'name': 'Grand Central - 42 St'
            # site has incorrect line data
        })

    def test_bart_transitland(self):
        sleep(1)
        self.check_data(BART.stations, {
            'name': 'Downtown Berkeley',
            'lines': ['Orange', 'Red']
        })

    def test_washington_transitland(self):
        sleep(1)
        self.check_data(Washington.stations, {
            'name': 'Crystal City',
            'lines': ['Blue','Yellow'],
        })

    def test_paris_transitland(self):
        sleep(1)
        self.check_data(Paris.stations, {
            'name': 'Jussieu',
            'lines': ['7','10']
        })

    def test_london_transitland(self):
        sleep(1)
        self.check_data(London.stations, {
            'name': 'London Bridge',
            'lines': ['Jubilee','Northern']
        })
