from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import json

import tvlogo
import fetcher

daddyLiveChannelsFileName = '247channels.html'
daddyLiveChannelsURL = 'https://thedaddy.to/24-7-channels.php'

tvLogosFilename = 'tvlogos.html'
tvLogosURL = 'https://github.com/tv-logo/tv-logos/tree/main/countries/united-states'

matches = []

def search_streams(file_path, keyword):
    """
    Searches for a keyword in a file and outputs the stream number and name for each match.

    Parameters:
    file_path (str): The path to the file.
    keyword (str): The keyword to search for.

    Returns:
    list: A list of tuples containing the stream number and name for each match.
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                if keyword.lower() in link.text.lower():
                    href = link['href']
                    stream_number = href.split('-')[-1].replace('.php', '')
                    stream_name = link.text.strip()
                    match = (stream_number, stream_name)

                    if match not in matches:
                        matches.append(match)

    except FileNotFoundError:
        print(f'The file {file_path} does not exist.')

    return matches

def search_channel_ids(file_path, search_string, idMatches):
    """
    Parses an XML file and finds channel tags with an id attribute that matches the search string.

    Parameters:
    file_path (str): The path to the XML file.
    search_string (str): The string to search for within the id attribute.

    Returns:
    list: A list of channel ids that match the search string.
    """

    # idMatches = []
    search_words = search_string.lower().split() # Split the search string into words

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for channel in root.findall('.//channel'):
            channel_id = channel.get('id')
            if channel_id:
                for word in search_words:
                    if word in channel_id.lower():
                        if channel_id not in idMatches:
                            idMatches.append({'id':channel_id, 'source': file_path})
                            if 'National Geographic' in channel_id:
                                print('What')
                        break  # Break the loop if one word idMatches to avoid duplicate entries

    except FileNotFoundError:
        print(f'The file {file_path} does not exist.')
    except ET.ParseError:
        print(f'The file {file_path} is not a valid XML file.')

    return idMatches

def print_possible_ids(possibleIds, channel):
    """
    Prints the possible IDs with their indices and takes user input to make a selection.

    Parameters:
    possibleIds (list): The list of possible IDs to print.

    Returns:
    str: The selected ID based on user input.
    """
    if possibleIds:

        print(f'0). I dont want this channel.')
        for index, match in enumerate(possibleIds):
            print(f'{index+1}). {match['id']} {match['source']}')
        
        while True:
            try:
                user_input = int(input(f"Select the index of the Channel ID you want ({channel}):"))-1
                if user_input == -1:
                    print(f'Not adding a match for this channel.')
                    return -1
                if 0 <= user_input < len(possibleIds):
                    selected_id = possibleIds[user_input]
                    print(f'You selected: {selected_id}')
                    return selected_id
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print('No matches found.')

def delete_file_if_exists(file_path):
    """
    Checks if a file exists and deletes it if it does.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    bool: True if the file was deleted, False if it didn't exist.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f'File {file_path} deleted.')
        return True
    else:
        print(f'File {file_path} does not exist.')
        return False


delete_file_if_exists('out.m3u8')
delete_file_if_exists('tvg-ids.txt')

epgs = [
    {'filename': 'epgShare1.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz'},
    {'filename': 'epgShare2.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS2.xml.gz'},
    # {'filename': 'epgShare3.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz'},
    # {'filename': 'epgShare4.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_UK1.xml.gz'},
    # {'filename': 'epgShare5.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_AU1.xml.gz'},
    # {'filename': 'epgShare6.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_IE1.xml.gz'},
    # {'filename': 'epgShare7.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz'},
    # {'filename': 'epgShare8.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_ZA1.xml.gz'},
    {'filename':'bevyCustom.xml','url':'https://www.bevy.be/generate/8TbvgWSctM.xml.gz'}
]

fetcher.fetchHTML(daddyLiveChannelsFileName, daddyLiveChannelsURL)
fetcher.fetchHTML(tvLogosFilename, tvLogosURL)

for epg in epgs:
    fetcher.fetchXML(epg['filename'], epg['url'])


search_terms = [
    # "Disney"]
    # "Altitude"]
    # "ABC",
    # "NBC",
    # "TNT"]
    # "Lifetime",
    # "CBS",
    # "Discovery"]
    # "NHL",
    # "gamecenter".
    # "Fox"]
    # "wnyw"]
    # "FOX USA"]
    # "HBO"]
    # "ESPN",
    # "A&E",
    # "AMC",
    # "FX"]
    # "NBA",
    # "NFL",
    # "Network"]
    # "TMC",
    # "Showtime"]
    # "Animal Planet",
    # "pbs",
    # "BBC America",
    # "Nick"]
    # "Starz",
    # "syfy"]
    # "Bally"
    # "NHL"]
    # "ESPN"]
    # "cinemax"]
    # "fox"]
    "nfl network"]
# ]


payload = tvlogo.extract_payload_from_file(tvLogosFilename)
print(json.dumps(payload, indent=2))

# Example usage with search_streams function
for term in search_terms:
    search_streams(daddyLiveChannelsFileName, term)

for channel in matches:
    word = channel[1].lower().replace('channel', '').replace('hdtv', '').replace('tv','').replace(' hd', '').replace('2','').replace('sports','').replace('1','').replace('usa','')
    possibleIds = []


    user_input = int(input(f"Do you want this channel? 0 = no 1 = yes ({channel[1]}):"))

    if(user_input == 0):
        continue
    else:
        print("Searching for matches...")
    for epg in epgs:
        search_channel_ids(epg['filename'], word, possibleIds)
    # search_channel_ids(epgShareEpg, word, possibleIds)

    matches = tvlogo.search_tree_items(word, payload)
    # print(json.dumps(matches, indent=2))

    channelID = print_possible_ids(possibleIds, channel[1])

    if(channelID != -1 and channelID != None):
        tvicon = print_possible_ids(matches, channel[1])
        if tvicon == None or tvicon == -1:
            tvicon = {'id':{'path':''}}

        with open("out.m3u8", 'a', encoding='utf-8') as file:  # Use 'a' mode for appending
            initialPath = payload.get('initial_path')
            file.write(f'#EXTINF:-1 tvg-id="{channelID['id']}" tvg-name="{channel[1]}" tvg-logo="https://raw.githubusercontent.com{initialPath}{tvicon['id']['path']}" group-title="USA (DADDY LIVE)", {channel[1]}\n')
            file.write(f"https://dlhd.global.ssl.fastly.net/dlhd/premium{channel[0]}\n")
            file.write('\n')

        with open("tvg-ids.txt", 'a', encoding='utf-8') as file:  # Use 'a' mode for appending
            file.write(f'{channelID['id']}\n')

    # if possibleIds:
    #     print(f"Enter the option that best matches the channel name ({channel[1]}):")
    #     for index, match in enumerate(possibleIds):
    #         print(f'{index}). {match}')
    # else:
    #     print('No id matches found.')


# if matches:
#     for match in matches:
#         print(f"Name: {match[1]}")
#         # print('#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="" group-title="" ,ABCNY')
#         # print(f"https://xyzdddd.mizhls.ru/lb/premium{match[0]}/index.m3u8")
#         # print()
#         # print(f'Stream Number: {match[0]}, Stream Name: {match[1]}')
# else:
#     print('No matches found.')

print("Number of Streams: ", len(matches))
