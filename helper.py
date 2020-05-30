import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime, date, timedelta
import re
import itertools

def getJSON(link):
    req = requests.get(link)
    json_data = req.json()
    return json_data

def get_races():
    today = datetime.today().strftime("%Y/%m/%d")
    link = "https://tab.ubet.com/api/racing/racingdaysummary/{}/[]".format(today)
    print(today)
    json_data = getJSON(link)
    json_data = json_data["RacingCodes"]
    racing_codes = []
    for racing_code in json_data:
        code = racing_code["MeetingCodeType"]["Code"]
        meetings = racing_code["Meetings"]
        for meeting in meetings:
            races = meeting["Races"]
            for race in races:
                if race["Status"] ==  "SELLING":
                    racing_codes.append("{}/{}/{}:{}".format(today, meeting["Code"], race["RaceNumber"], code))
    print(racing_codes)
    return racing_codes

def get_race_deatils(key):
    code = key.split(":")[1]
    key = key.split(":")[0]

    link_race_inf = "https://tab.ubet.com/api/racingViewData/raceInformation/{}".format(key)
    link_tips = "https://tab.ubet.com/api/racingViewData/tips/{}".format(key)
    link_runner_inf = "https://tab.ubet.com/api/racingViewData/racing/{}".format(key)
    link_runner_add = "https://api.beta.tab.com.au/v1/ubet-sky-vision-service/StreamFormGuide/{}{}/runners".format(key.replace("/", ""), code)

    json_race_inf = getJSON(link_race_inf)
    json_tips = getJSON(link_tips)
    json_runner_inf = getJSON(link_runner_inf)
    json_runner_add = getJSON(link_runner_add)

    race_details = {}

    race_details["raceDistance"] = json_race_inf["raceDistance"]
    race_details["raceName"] = json_race_inf["raceName"]
    race_details["tips"] = json_tips["racingTips"][0]["tipsData"][0]["tips"]
    race_details["tipster"] = json_tips["racingTips"][0]["tipsData"][0]["tipster"]

    runners = []
    for runner_json in json_runner_inf["runners"]:
        runner = {}
        runner['runnerNumber'] = runner_json['runnerInformation']['runnerNumber']
        runner['runnerName'] = runner_json['runnerInformation']['runnerName']
        runner['riderName'] = runner_json['runnerInformation']['riderName']
        runner['trainerName'] = runner_json['runnerInformation']['trainerName']
        runner['rating'] = runner_json['rating']
        runner['lastThreeStarts'] = runner_json["lastThreeStarts"]
        runner['form'] = runner_json['form']
        runner['weight'] = runner_json['runnerInformation']['weight']
        runners.append(runner)
    
    runner_adds = []
    for runner_add_json in json_runner_add:
        runner_add = {}
        runner_add['tabNumber'] = runner_add_json['tabNumber']
        runner_add['jockeyName'] = runner_add_json['jockeyName']
        runner_add['prizeMoney'] = runner_add_json['prizeMoney']
        runner_add['sire'] = runner_add_json['sire']
        runner_add['dam'] = runner_add_json['dam']
        runner_add['total'] = runner_add_json['total']
        runner_add['winPercent'] = runner_add_json['winPercent']
        runner_add['placePercent'] = runner_add_json['placePercent']
        runner_add['resultAtThisDistance'] = runner_add_json['resultAtThisDistance']
        # runner_add['thisTrack'] = runner_add_json['thisTrack']
        runner_add['thisSeason'] = runner_add_json['thisSeason']
        runner_add['track'] = runner_add_json['tabFormData']['track']
        runner_add['distance'] = runner_add_json['tabFormData']['distance']
        runner_add['trackAndDistance'] = runner_add_json['tabFormData']['trackAndDistance']
        runner_add['class'] = runner_add_json['tabFormData']['class']
        runner_add['firstUp'] = runner_add_json['tabFormData']['firstUp']
        runner_add['secondUp'] = runner_add_json['tabFormData']['secondUp']
        runner_add['jockey'] = runner_add_json['tabFormData']['jockey']
        runner_add['firm'] = runner_add_json['tabFormData']['firm']
        runner_add['good'] = runner_add_json['tabFormData']['good']
        runner_add['soft'] = runner_add_json['tabFormData']['soft']
        runner_add['heavy'] = runner_add_json['tabFormData']['heavy']
        runner_adds.append(runner_add)

    for index, runner in enumerate(runners):
        runners[index].update(runner_adds[index])

    race_details["runners"] = runners
    pprint(race_details)
    return race_details

def driver():
    # get_races()
    get_race_deatils("2020/05/30/QS/03:R")