import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime, date, timedelta
import csv


def getJSON(link):
    req = requests.get(link)
    json_data = req.json()
    return json_data

def tabulate(filename, matrix):
    with open(filename, "w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)


def get_races():
    today = datetime.today().strftime("%Y/%m/%d")
    link = "https://tab.ubet.com/api/racing/racingdaysummary/{}/[]".format(
        today)
    json_data = getJSON(link)
    json_data = json_data["RacingCodes"]
    racing_codes = []
    for racing_code in json_data:
        code = racing_code["MeetingCodeType"]["Code"]
        meetings = racing_code["Meetings"]
        for meeting in meetings:
            races = meeting["Races"]
            for race in races:
                if race["Status"] == "SELLING":
                    race_number =  race["RaceNumber"]
                    if race_number < 10:
                        race_number = "0" + str(race_number)
                    racing_codes.append(
                        "{}/{}/{}:{}".format(today, meeting["Code"],race_number, code))
    return racing_codes


def get_race_deatils(key):
    code = key.split(":")[1]
    key = key.split(":")[0]
    
    link_race_inf = "https://tab.ubet.com/api/racingViewData/raceInformation/{}".format(
        key)
    link_tips = "https://tab.ubet.com/api/racingViewData/tips/{}".format(key)
    link_runner_inf = "https://tab.ubet.com/api/racingViewData/racing/{}".format(
        key)
    link_runner_add = "https://api.beta.tab.com.au/v1/ubet-sky-vision-service/StreamFormGuide/{}{}/runners".format(key.replace("/", ""), code)
    # print(link_runner_add)

    json_race_inf = getJSON(link_race_inf)
    json_tips = getJSON(link_tips)
    json_runner_inf = getJSON(link_runner_inf)
    json_runner_add = getJSON(link_runner_add)

    race_details = {}

    race_details["raceDistance"] = json_race_inf["raceDistance"]
    race_details["raceName"] = json_race_inf["raceName"]
    race_details["raceTime"] = json_race_inf["raceDate"].split("T")[1][:-1]
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
        # pprint(runner_add_json.keys())
        try:
            runner_add['tabNumber'] = runner_add_json['tabNumber']
        except:
            runner_add['tabNumber'] = ""
        try:
            runner_add['jockeyName'] = runner_add_json['jockeyName']
        except:
            runner_add['jockeyName'] = ""
        try:
            runner_add['prizeMoney'] = runner_add_json['prizeMoney']
        except:
            runner_add['prizeMoney'] = ""
        try:
            runner_add['sire'] = runner_add_json['sire']
        except:
            runner_add['sire'] = ""
        try:
            runner_add['dam'] = runner_add_json['dam']
        except:
            runner_add['dam'] = ""
        try:
            runner_add['total'] = runner_add_json['total']
        except:
            runner_add['total'] = ""
        try:
            runner_add['winPercent'] = runner_add_json['winPercent']
        except:
            runner_add['winPercent'] = ""
        try:
            runner_add['placePercent'] = runner_add_json['placePercent']
        except:
            runner_add['placePercent'] = ""
        try:
            runner_add['resultAtThisDistance'] = runner_add_json['resultAtThisDistance']
        except:
            runner_add['resultAtThisDistance'] = ""
        try:
            runner_add['thisTrack'] = runner_add_json['thisTrack']
        except:
            runner_add['thisTrack'] = ""
        try:
            runner_add['thisSeason'] = runner_add_json['thisSeason']
        except:
            runner_add['thisSeason'] = ""
        try:
            runner_add['track'] = runner_add_json['tabFormData']['track']
        except:
            runner_add['track'] = ""
        try:
            runner_add['distance'] = runner_add_json['tabFormData']['distance']
        except:
            runner_add['distance'] = ""
        try:
            runner_add['trackAndDistance'] = runner_add_json['tabFormData']['trackAndDistance']
        except:
            runner_add['trackAndDistance'] = ""
        try:
            runner_add['class'] = runner_add_json['tabFormData']['class']
        except:
            runner_add['class'] = ""
        try:
            runner_add['firstUp'] = runner_add_json['tabFormData']['firstUp']
        except:
            runner_add['firstUp'] = ""
        try:
            runner_add['secondUp'] = runner_add_json['tabFormData']['secondUp']
        except:
            runner_add['secondUp'] = ""
        try:
            runner_add['jockey'] = runner_add_json['tabFormData']['jockey']
        except:
            runner_add['jockey'] = ""
        try:
            runner_add['firm'] = runner_add_json['tabFormData']['firm']
        except:
            runner_add['firm'] = ""
        try:
            runner_add['good'] = runner_add_json['tabFormData']['good']
        except:
            runner_add['good'] = ""
        try:
            runner_add['soft'] = runner_add_json['tabFormData']['soft']
        except:
            runner_add['soft'] = ""
        try:
            runner_add['heavy'] = runner_add_json['tabFormData']['heavy']
        except:
            runner_add['heavy'] = ""

        runner_adds.append(runner_add)

    for index, runner in enumerate(runners):
        runners[index].update(runner_adds[index])

    race_details["runners"] = runners
    # pprint(race_details)
    return race_details


def make_matrix(details):
    matrix = []
    heading = ["Race Name", "Race Time", "Race Distance", "Tips", "Tipster", "Runner Name", "Rider Name", "Trainer Name",
               "Rating", "Last Three Starts", "Form", "Weight", "Prize Money", "Sire", "Dam", "Total", "Win Percent", 
               "Place Percent", "Result","This Track", "This Season", "Track", "Distance", "Track and Distance", "Class", "First Up", "Second Up",
               "Jockey", "Firm", "Good", "Soft", "Heavy"]
    matrix.append(heading)

    for detail in details:
        for runner in detail["runners"]:
            row = []
            row.append(detail["raceName"])
            row.append(detail["raceTime"])
            row.append(detail["raceDistance"])
            row.append(detail["tips"])
            row.append(detail["tipster"])
            row.append(runner["runnerName"])
            row.append(runner["riderName"])
            row.append(runner["trainerName"])

            row.append(runner["rating"])
            row.append(runner["lastThreeStarts"])
            row.append(runner["form"])
            row.append(runner["weight"])
            row.append(runner["prizeMoney"])
            row.append(runner["sire"])
            row.append(runner["dam"])
            row.append(runner["total"])
            row.append(runner["winPercent"])

            row.append(runner["placePercent"])
            row.append(runner["resultAtThisDistance"])
            row.append(runner["thisTrack"])
            row.append(runner["thisSeason"])
            row.append(runner["track"])
            row.append(runner["distance"])
            row.append(runner["trackAndDistance"])
            row.append(runner["class"])
            row.append(runner["firstUp"])
            row.append(runner["secondUp"])

            row.append(runner["jockey"])
            row.append(runner["firm"])
            row.append(runner["good"])
            row.append(runner["soft"])
            row.append(runner["heavy"])

            matrix.append(row)
    return matrix

def driver():
    details = []
    racing_codes = get_races()
    for racing_code in racing_codes:
        print(racing_code)
        detail = get_race_deatils(racing_code)
        details.append(detail)
    matrix = make_matrix(details)
    tabulate("details.csv", matrix)