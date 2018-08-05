import json
import requests
import datetime
from meteocalc import heat_index

# Contains ids and states for 125 cities in the US
cities = (
    {'id': 4960140, 'state': "ME"},  # "Caribou",
    {'id': 4975802, 'state': "ME"},  # "Portland",
    {'id': 5089178, 'state': "NH"},  # "Manchester",
    {'id': 5234372, 'state': "VT"},  # "Burlington",
    {'id': 4930956, 'state': "MA"},  # "Boston",
    {'id': 5106834, 'state': "NY"},  # "Albany",
    {'id': 5224151, 'state': "RI"},  # "Providence",
    {'id': 4835797, 'state': "CT"},  # "Hartford",
    {'id': 5140405, 'state': "NY"},  # "Syracuse",
    {'id': 5110629, 'state': "NY"},  # "Buffalo",
    {'id': 5134086, 'state': "NY"},  # "Rochester",
    {'id': 5128581, 'state': "NY"},  # "New York City",
    {'id': 5188843, 'state': "PA"},  # "Erie",
    {'id': 5206379, 'state': "PA"},  # "Pittsburgh",
    {'id': 5178127, 'state': "PA"},  # "Allentown",
    {'id': 5213681, 'state': "PA"},  # "State College",
    {'id': 4560349, 'state': "PA"},  # "Philadelphia",
    {'id': 4500546, 'state': "NJ"},  # "Atlantic City",
    {'id': 4142290, 'state': "DE"},  # "Dover",
    {'id': 4347778, 'state': "MD"},  # "Baltimore",
    {'id': 4366164, 'state': "Somewhere"},  # "Washington DC.",
    {'id': 4791259, 'state': "VA"},  # "Virginia Beach",
    {'id': 4782167, 'state': "VA"},  # "Roanoke",
    {'id': 4815352, 'state': "WV"},  # "Morgantown",
    {'id': 4801859, 'state': "WV"},  # "Charleston",
    {'id': 4164138, 'state': "FL"},  # "Miami",
    {'id': 4174757, 'state': "FL"},  # "Tampa",
    {'id': 4167147, 'state': "FL"},  # "Orlando",
    {'id': 4160021, 'state': "FL"},  # "Jacksonville",
    {'id': 4168228, 'state': "FL"},  # "Pensacola",
    {'id': 4174715, 'state': "FL"},  # "Tallahassee",
    {'id': 4180439, 'state': "GA"},  # "Atlanta",
    {'id': 4221552, 'state': "GA"},  # "Savannah",
    {'id': 4049979, 'state': "AL"},  # "Birmingham",
    {'id': 4431410, 'state': "MS"},  # "Jackson",
    {'id': 4574324, 'state': "SC"},  # "Charleston",
    {'id': 4575352, 'state': "SC"},  # "Columbia",
    {'id': 4460243, 'state': "NC"},  # "Charlotte",
    {'id': 4487042, 'state': "NC"},  # "Raleigh",
    {'id': 4499379, 'state': "NC"},  # "Wilmington",
    {'id': 4453066, 'state': "NC"},  # "Asheville",
    {'id': 4641239, 'state': "TN"},  # "Memphis",
    {'id': 4644585, 'state': "TN"},  # "Nashville",
    {'id': 4634946, 'state': "TN"},  # "Knoxville",
    {'id': 4299276, 'state': "KY"},  # "Louisville",
    {'id': 4297983, 'state': "KY"},  # "Lexington",
    {'id': 4508722, 'state': "OH"},  # "Cincinnati",
    {'id': 4509177, 'state': "OH"},  # "Columbus",
    {'id': 5150529, 'state': "OH"},  # "Cleveland",
    {'id': 4259418, 'state': "IN"},  # "Indianapolis",
    {'id': 4920423, 'state': "IN"},  # "Fort Wayne",
    {'id': 4887398, 'state': "IL"},  # "Chicago",
    {'id': 4887158, 'state': "IL"},  # "Champaign",
    {'id': 4990729, 'state': "MI"},  # "Detroit",
    {'id': 4994358, 'state': "MI"},  # "Grand Rapids",
    {'id': 4984075, 'state': "MI"},  # "Alpena",
    {'id': 5000947, 'state': "MI"},  # "Marquette",
    {'id': 5261457, 'state': "WI"},  # "Madison",
    {'id': 5254962, 'state': "WI"},  # "Green Bay",
    {'id': 5037649, 'state': "MN"},  # "Minneapolis",
    {'id': 5024719, 'state': "MN"},  # "Duluth",
    {'id': 7121191, 'state': "MN"},  # "Crescent Drive Mobile Village",
    {'id': 4853828, 'state': "IA"},  # "Des Moines",
    {'id': 4393217, 'state': "MO"},  # "Kansas City",
    {'id': 4407074, 'state': "MO"},  # "St. Louis",
    {'id': 4119403, 'state': "AR"},  # "Little Rock",
    {'id': 4341513, 'state': "LA"},  # "Shreveport",
    {'id': 4335045, 'state': "LA"},  # "New Orleans",
    {'id': 4684888, 'state': "TX"},  # "Dallas",
    {'id': 4671654, 'state': "TX"},  # "Austin",
    {'id': 4726206, 'state': "TX"},  # "San Antonio",
    {'id': 4699066, 'state': "TX"},  # "Houston",
    {'id': 4683416, 'state': "TX"},  # "Corpus Christi",
    {'id': 4676740, 'state': "TX"},  # "Brownsville",
    {'id': 5520076, 'state': "TX"},  # "Del Rio",
    {'id': 5525577, 'state': "TX"},  # "Lubbock",
    {'id': 5516233, 'state': "TX"},  # "Amarillo",
    {'id': 5520993, 'state': "TX"},  # "El Paso",
    {'id': 4544349, 'state': "OK"},  # "Oklahoma City",
    {'id': 4281730, 'state': "KS"},  # "Wichita",
    {'id': 5445298, 'state': "KS"},  # "Dodge City",
    {'id': 5074472, 'state': "NE"},  # "Omaha",
    {'id': 5697383, 'state': "NE"},  # "McCook",
    {'id': 5699404, 'state': "NE"},  # "Scottsbluff",
    {'id': 5768233, 'state': "SD"},  # "Rapid City",
    {'id': 5231851, 'state': "SD"},  # "Sioux Falls",
    {'id': 5767918, 'state': "SD"},  # "Pierre",
    {'id': 5059163, 'state': "ND"},  # "Fargo",
    {'id': 5688025, 'state': "ND"},  # "Bismarck",
    {'id': 5690532, 'state': "ND"},  # "Minot",
    {'id': 5640350, 'state': "MT"},  # "Billings",
    {'id': 5666639, 'state': "MT"},  # "Missoula",
    {'id': 5677433, 'state': "MT"},  # "Shelby",
    {'id': 5664486, 'state': "MT"},  # "Malta",
    {'id': 5820705, 'state': "WY"},  # "Casper",
    {'id': 5830007, 'state': "WY"},  # "Lander",
    {'id': 5828648, 'state': "WY"},  # "Jackson",
    {'id': 5423573, 'state': "CO"},  # "Grand Junction",
    {'id': 5419384, 'state': "CO"},  # "Denver",
    {'id': 5417598, 'state': "CO"},  # "Colorado Springs",
    {'id': 5454711, 'state': "NM"},  # "Albuquerque",
    {'id': 5467328, 'state': "NM"},  # "Farmington",
    {'id': 5308655, 'state': "AZ"},  # "Phoenix",
    {'id': 5294810, 'state': "AZ"},  # "Flagstaff",
    {'id': 5780993, 'state': "UT"},  # "Salt Lake City",
    {'id': 5546220, 'state': "UT"},  # "St. George",
    {'id': 5586437, 'state': "ID"},  # "Boise",
    {'id': 5604045, 'state': "ID"},  # "Pocatello",
    {'id': 5811696, 'state': "WA"},  # "Spokane",
    {'id': 5809844, 'state': "WA"},  # "Seattle",
    {'id': 5746545, 'state': "OR"},  # "Portland",
    {'id': 5713587, 'state': "OR"},  # "Bend",
    {'id': 5511077, 'state': "NV"},  # "Reno",
    {'id': 5506956, 'state': "NV"},  # "Las Vegas",
    {'id': 5703670, 'state': "NV"},  # "Elko",
    {'id': 5563397, 'state': "CA"},  # "Eureka",
    {'id': 5389489, 'state': "CA"},  # "Sacramento",
    {'id': 5391959, 'state': "CA"},  # "San Francisco",
    {'id': 5350937, 'state': "CA"},  # "Fresno",
    {'id': 5368361, 'state': "CA"},  # "Los Angeles",
    {'id': 5391811, 'state': "CA"},  # "San Diego",
    {'id': 5879400, 'state': "AK"},  # "Anchorage",
    {'id': 5554072, 'state': "AK"},  # "Juneau",
    {'id': 5861897, 'state': "AK"},  # "Fairbanks",
    {'id': 5856195, 'state': "HI"})  # "Honolulu"

global_weather_bank = []
sorted_by_temp = []
sorted_by_humid = []
sorted_by_heat = []
sorted_by_chill = []


def update_all(init):
    print("Updating weather reports...")
    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/weather?id=" + str(
            city['id']) + "&APPID=5ccc58dedce73f6e956b4e063a2a9cfa"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Convert to Fahrenheit before storing
            jsoned = json.loads(response.content.decode('utf-8'))
            fahrenheit = kelvin_to_fahrenheit(jsoned['main']['temp'])
            jsoned['main']['temp'] = fahrenheit
            jsoned['state'] = city['state']
            if init:
                global_weather_bank.append(jsoned)
            else:
                for g in global_weather_bank:
                    if g['id'] == city['id']:
                        global_weather_bank[global_weather_bank.index(g)] = jsoned
        else:
            print("error for " + str(city['id']) + str(city['state']))
    print("Weather reports updated " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    sort_by_temp()
    sort_by_humid()
    sort_by_heat()
    sort_by_chill()


def get_local_weather(lat, long):
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(
        lat) + "&lon=" + str(long) + "&APPID=5ccc58dedce73f6e956b4e063a2a9cfa"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jsoned = json.loads(response.content.decode('utf-8'))
        fahrenheit = kelvin_to_fahrenheit(jsoned['main']['temp'])
        jsoned['main']['temp'] = fahrenheit
        jsoned['main']['heat'] = calculate_heat_index(jsoned['main']['temp'], jsoned['main']['humidity'])
        return jsoned


def get_single_weather(city):
    return {
        'hightemp': sorted_by_temp[0],
        'lowtemp': sorted_by_temp[len(sorted_by_temp) - 1],
        'highhumid': sorted_by_humid[0],
        'lowhumid': sorted_by_humid[len(sorted_by_humid) - 1],
        'heat': sorted_by_heat[0],
        'chill': sorted_by_chill[len(sorted_by_chill) - 1]
    }.get(city, {'response': 'Invalid answer'})


def get_all_weather():
    local_weather_bank = []
    for c in sorted_by_temp:
        local_weather_bank.append(c)

    return local_weather_bank


def sort_by_temp():
    global sorted_by_temp
    sorted_by_temp = []
    for w in global_weather_bank:
        placed = False

        if len(sorted_by_temp) == 0:
            sorted_by_temp.append(w)
            continue

        for s in sorted_by_temp:
            if s['main']['temp'] < w['main']['temp']:
                sorted_by_temp.insert(sorted_by_temp.index(s), w)
                placed = True
                break

        if placed is not True:
            sorted_by_temp.append(w)


def sort_by_humid():
    global sorted_by_humid
    sorted_by_humid = []
    for w in global_weather_bank:
        placed = False

        if len(sorted_by_humid) == 0:
            sorted_by_humid.append(w)
            continue

        for s in sorted_by_humid:
            if s['main']['humidity'] < w['main']['humidity']:
                sorted_by_humid.insert(sorted_by_humid.index(s), w)
                placed = True
                break

        if placed is not True:
            sorted_by_humid.append(w)


def sort_by_heat():
    global sorted_by_heat
    sorted_by_heat = []
    for w in global_weather_bank:
        w['main']['heat'] = calculate_heat_index(w['main']['temp'], w['main']['humidity'])
        placed = False

        if len(sorted_by_heat) == 0:
            sorted_by_heat.append(w)
            continue

        for s in sorted_by_heat:
            if s['main']['heat'] < w['main']['heat']:
                sorted_by_heat.insert(sorted_by_heat.index(s), w)
                placed = True
                break

        if placed is not True:
            sorted_by_heat.append(w)


def sort_by_chill():
    global sorted_by_chill
    sorted_by_chill = []
    for w in global_weather_bank:
        w['main']['chill'] = calculate_wind_chill(w['main']['temp'], w['wind']['speed'])
        placed = False

        if len(sorted_by_chill) == 0:
            sorted_by_chill.append(w)
            continue

        for s in sorted_by_chill:
            if s['main']['chill'] < w['main']['chill']:
                sorted_by_chill.insert(sorted_by_chill.index(s), w)
                placed = True
                break

        if placed is not True:
            sorted_by_chill.append(w)


def calculate_heat_index(temp, humid):
    return float(heat_index(temp, humid))


def calculate_wind_chill(temp, speed):
    speed *= 2.23694
    return 35.74 + (0.6215 * temp) - 35.75 * (speed ** 0.16) + 0.4275 * temp * (speed ** 0.16)


def kelvin_to_fahrenheit(kelvin):
    fahrenheit = ((kelvin - 273) * (9 / 5)) + 32
    return fahrenheit
