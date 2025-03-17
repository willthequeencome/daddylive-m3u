import xml.etree.ElementTree as ET
import random
import uuid
import fetcher
import json
import os
import datetime
import pytz

NUM_CHANNELS = 400
DADDY_JSON_FILE = "daddyliveSchedule.json"
M3U8_OUTPUT_FILE = "daily.m3u8"
EPG_OUTPUT_FILE = "daily.xml"
LOGO = "https://raw.githubusercontent.com/JHarding86/daddylive-m3u/refs/heads/main/hardingtv.png"

mStartTime = "0"
mStopTime = "0"

def generate_unique_ids(count, seed=42):
    random.seed(seed)
    return [str(uuid.UUID(int=random.getrandbits(128))) for _ in range(count)]

def loadJSON(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def createSingleChannelEPGData(UniqueID, tvgName):
    xmlChannel = ET.Element('channel', id=UniqueID)
    ET.SubElement(xmlChannel, 'display-name').text = tvgName
    ET.SubElement(xmlChannel, 'icon', src=LOGO)
    return xmlChannel

def createSingleEPGData(startTime, stopTime, UniqueID, channelName, description):
    programme = ET.Element('programme', start=str(startTime) + " +0000", stop=str(stopTime) + " +0000", channel=UniqueID)
    ET.SubElement(programme, 'title').text = channelName
    ET.SubElement(programme, 'desc').text = description
    return programme

def addChannelsByLeagueSport(leagueSportTuple):
    for day, value in dadjson.items():
        try:
            for leagueSport in leagueSportTuple:
                sport_data = dadjson.get(day, {}).get(leagueSport["sport"], [])
                for game in sport_data:
                    if leagueSport["league"] in game.get("event", ""):
                        print(game["event"])
                        for channel in game.get("channels", []):
                            date_time = day.replace("th ", " ").replace("rd ", " ").replace("st ", " ").replace("nd ", " ")
                            date_time = date_time.replace("-", game["time"] + " -")
                            date_format = "%A %d %b %Y %H:%M - Schedule Time UK GMT"
                            start_date = datetime.datetime.strptime(date_time, date_format)
                            global mStartTime, mStopTime
                            mStartTime = start_date.strftime("%Y%m%d%H%M%S")
                            mStopTime = (start_date + datetime.timedelta(hours=3)).strftime("%Y%m%d%H%M%S")
                            UniqueID = unique_ids.pop(0)
                            channelName = f"{game['event']} {start_date.strftime('%m/%d/%y %I:%M %p')} {channel['channel_name']}"
                            channelID = f"{channel['channel_id']}"
                            global channelCount
                            tvgName = f"OpenChannel{str(channelCount).zfill(3)}"
                            channelCount += 1
                            with open(M3U8_OUTPUT_FILE, 'a', encoding='utf-8') as file:
                                file.write(f'#EXTINF:-1 tvg-id="{UniqueID}" tvg-name="{tvgName}" tvg-logo="{LOGO}" group-title="USA (DADDY LIVE)", {tvgName}\n')
                                file.write(f"https://dlhd.global.ssl.fastly.net/dlhd/premium{channelID}\n\n")
                            root.append(createSingleChannelEPGData(UniqueID, tvgName))
                            root.append(createSingleEPGData(mStartTime, mStopTime, UniqueID, channelName, "No Description"))
        except KeyError as e:
            print(f"KeyError: {e} - Missing key in JSON for {day} or {leagueSportTuple}.")

channelCount = 0
unique_ids = generate_unique_ids(NUM_CHANNELS)
fetcher.fetchHTML(DADDY_JSON_FILE, "https://thedaddy.to/schedule/schedule-generated.json")
dadjson = loadJSON(DADDY_JSON_FILE)
if os.path.isfile(M3U8_OUTPUT_FILE):
    os.remove(M3U8_OUTPUT_FILE)
root = ET.Element('tv')
leageSportTuple = [{"league": "NHL", "sport": "Ice Hockey"}, {"league": "NFL", "sport": "Am. Football"}]
addChannelsByLeagueSport(leageSportTuple)
for id in unique_ids:
    with open(M3U8_OUTPUT_FILE, 'a', encoding='utf-8') as file:
        channelNumber = str(channelCount).zfill(3)
        tvgName = f"OpenChannel{channelNumber}"
        file.write(f'#EXTINF:-1 tvg-id="{id}" tvg-name="{tvgName}" tvg-logo="{LOGO}" group-title="USA (DADDY LIVE)", {tvgName}\n')
        file.write(f"https://dlhd.global.ssl.fastly.net/dlhd/premium{channelID}\n\n")
        channelCount += 1
    root.append(createSingleChannelEPGData(id, tvgName))
    root.append(createSingleEPGData(mStartTime, mStopTime, id, "No Programme Available", "No Description"))
tree = ET.ElementTree(root)
tree.write(EPG_OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
