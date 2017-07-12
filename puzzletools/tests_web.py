"""
Tests to make sure that the sites that we scrape haven't changed their
data formats.
"""

import unittest
from time import sleep, strptime
from puzzletools.enumerations_web import *
from puzzletools.subway import *

class WebTest(unittest.TestCase):

    def check_exists(self,it):
        try:
            return next(it)
        except StopIteration:
            self.assertTrue(False,'not found')

    def check_data(self,enum,data):
        key=enum.display_key
        item=self.check_exists(i for i in enum if getattr(i,key)==data[key])
        for k,v in data.items():
            with self.subTest(name=k):
                i1 = data[k]
                i2 = getattr(item,k)
                if isinstance(i1,list) and isinstance(i2,list):
                    self.assertEqual(set(i1),set(i2))
                else:
                    self.assertEqual(i1,i2)

    def test_countries(self):
        sleep(1)
        self.check_data(countries(),{
            'name': 'United States of America',
            'alpha2': 'US',
            'alpha3': 'USA',
            'numeric': 840,
            'independent': True
        })

    def test_states(self):
        sleep(1)
        self.check_data(_us_states(),{
            'name': 'Massachusetts',
            'abbr': 'MA',
            'capital': 'Boston',
            'statehood': strptime('6 Feb 1788','%d %b %Y')
        })

    def test_resistors(self):
        sleep(1)
        self.check_data(resistor_colors(), {
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
        self.check_data(zodiac(),{
            'name': 'Capricorn',
            'start': strptime('22 Dec','%d %b'),
            'end': strptime('20 Jan','%d %b')
        })

    def test_currency(self):
        sleep(1)
        self.check_data(currency(),{
            'code': 'CHF',
            'number': 756,
            'name': 'Swiss franc',
            'countries': ['Switzerland','Liechtenstein']
        })

    def test_language(self):
        sleep(1)
        self.check_data(languages(),{
            'name': 'English',
            'native_name': 'English',
            'code': 'en'
        })

    def test_london_wiki(self):
        sleep(1)
        self.check_data(london_underground_stations(),{
            'name': 'London Bridge',
            'lines': ['Northern','Jubilee']
        })

    def test_mbta_wiki(self):
        sleep(1)
        self.check_data(mbta_stations(),{
            'name': 'Kendall/MIT',
            'lines': ['Red Line']
        })

    def test_paris_wiki(self):
        sleep(1)
        self.check_data(paris_metro_stations(),{
            'name': 'Jussieu',
            'code': '12-07',
            'lines': ['7','10']
        })

    def test_washington_wiki(self):
        sleep(1)
        self.check_data(washington_metro_stations(),{
            'name': 'Crystal City',
            'lines': ['Blue Line','Yellow Line'],
        })

    def test_airport(self):
        self.check_data(airport_codes(),{
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
        self.check_data(airlines(),{
            'name': 'Turkmenistan Airlines',
            'alias': 'Turkmenhovayollary',
            'iata': 'T5',
            'icao': 'TUA',
            'callsign': 'TURKMENISTAN',
            'country': 'Turkmenistan',
            'active': True
        })

    def test_stock(self):
        self.check_data(stocks(),{
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
        self.check_data(MBTA.stations(),{
            'name': 'Kendall/MIT',
            'lines': ['Red Line']
        })

    def test_ny_transitland(self):
        sleep(1)
        self.check_data(NewYork.stations(),{
            'name': 'Grand Central - 42 St'
            # site has incorrect line data
        })

    def test_bart_transitland(self):
        sleep(1)
        self.check_data(BART.stations(),{
            'name': 'Downtown Berkeley',
            'lines': ['Warm Springs/South Fremont - Richmond', 'Richmond - Daly City/Millbrae']
        })

    def test_washington_transitland(self):
        sleep(1)
        self.check_data(Washington.stations(),{
            'name': 'Crystal City',
            'lines': ['Blue','Yellow'],
        })

    def test_paris_transitland(self):
        sleep(1)
        self.check_data(Paris.stations(),{
            'name': 'Jussieu',
            'lines': ['7','10']
        })

    def test_london_transitland(self):
        sleep(1)
        self.check_data(London.stations(),{
            'name': 'London Bridge',
            'lines': ['Jubilee','Northern']
        })
