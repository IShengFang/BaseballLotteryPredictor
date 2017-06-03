from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import pandas as pd
import os
import json
date = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def GetData(year, data_time):
    url = 'http://www.baseball-reference.com/previews/' + year + '/' + data_time + '.shtml'
    data = pd.read_html(url)
    x = data[0]
    x.columns = range(x.shape[1])
    x = x[x[0].notnull()]
    x = x.loc[list(map(lambda x: len(x) > 50, x[0]))]
    x = x.loc[:, 0:1]

    ## road
    texts = x[0][1]
    texts = texts.replace('(', ' (')
    texts = texts.replace(':', ' ')

    # team name
    team_name = ""
    for text in texts:
        if text.isdigit():
            break
        team_name += text

    # data detail
    texts_split = texts.split(" ")
    while "" in texts_split:
        texts_split.remove("")
    texts_detail = texts_split[texts_split.index("Home"):texts_split.index("IL")+2]
    road = dict({"Team name": team_name})
    for index in range(0, len(texts_detail), 2):
        road[texts_detail[index]] = texts_detail[index+1]

    # last 10 games
    last_10_games = texts_split.copy()
    last_10_games.remove('Last')
    last_10_games = last_10_games[last_10_games.index('Place/GB')+1:last_10_games.index('Last')]
    while "" in last_10_games:
        last_10_games.remove("")
    for item in last_10_games:
        if "(" in item:
            last_10_games.remove(item)
    while 'gb' in last_10_games:
        last_10_games.remove('gb')
    while 'up' in last_10_games:
        last_10_games.remove('up')
    while '-' in last_10_games:
        if last_10_games.index('-')%10 == 5:
            last_10_games[last_10_games.index('-')] = 'T'
        else:
            fore = last_10_games[:last_10_games.index('-')]
            back = last_10_games[last_10_games.index('-')+1:]
            last_10_games = fore + [None, None, None] + back
    last_10_game_list = []
    for i in range(0, 100, 10):
        if i > len(last_10_games)-1:
            last_10_game_list.append([None, None, None, None, None, None, None, None])
        else:
            if len(last_10_games[i+3]) < 2:
                day = date[last_10_games[i+2]] + '0' + last_10_games[i+3]
            else:
                day = date[last_10_games[i+2]] + last_10_games[i+3]
            if '@' in last_10_games[i+4]:
                opp = last_10_games[i+4]
                opp = opp.replace("@", "")
                flag = 0
            else:
                opp = last_10_games[i+4]
                flag = 1
            if last_10_games[i+5] == 'W':
                W_L = 1
            elif last_10_games[i+5] == 'L':
                W_L = 0
            else:
                W_L = 0.5
            if len(last_10_games[i+3]) == 1:
                last_10_games[i+3] = '0' + last_10_games[i+3]
            if last_10_games[i+7] != None:
                record = last_10_games[i+7]
            else:
                record = None
            if last_10_games[i+8] != None:
                place = int(last_10_games[i+8][0])
            else:
                place = None
            if last_10_games[i+9] != None:
                try:
                    GB = float(last_10_games[i+9])
                except:
                    GB = 0.0
            else:
                GB = None
            last_10_game_list.append([day,
                                      flag,
                                      opp,
                                      W_L,
                                      last_10_games[i+6],
                                      record,
                                      place,
                                      GB])
    road["last_10_game"] = last_10_game_list


    ## home
    texts = x[1][1]
    texts = texts.replace('(', ' (')
    texts = texts.replace(':', ' ')

    # team name
    team_name = ""
    for text in texts:
        if text.isdigit():
            break
        team_name += text

    # data detail
    texts_split = texts.split(" ")
    while "" in texts_split:
        texts_split.remove("")
    texts_detail = texts_split[texts_split.index("Home"):texts_split.index("IL")+2]
    home = dict({"Team name": team_name})
    for index in range(0, len(texts_detail), 2):
        home[texts_detail[index]] = texts_detail[index+1]

    # last 10 games
    last_10_games = texts_split.copy()
    last_10_games.remove('Last')
    last_10_games = last_10_games[last_10_games.index('Place/GB')+1:last_10_games.index('Last')]
    while "" in last_10_games:
        last_10_games.remove("")
    for item in last_10_games:
        if "(" in item:
            last_10_games.remove(item)
    while 'gb' in last_10_games:
        last_10_games.remove('gb')
    while 'up' in last_10_games:
        last_10_games.remove('up')
    while '-' in last_10_games:
        if last_10_games.index('-')%10 == 5:
            last_10_games[last_10_games.index('-')] = 'T'
        else:
            fore = last_10_games[:last_10_games.index('-')]
            back = last_10_games[last_10_games.index('-')+1:]
            last_10_games = fore + [None, None, None] + back
            last_10_games = fore + [None, None, None] + back+ [None, None, None] + back
    last_10_game_list = []
    for i in range(0, 100, 10):
        if i > len(last_10_games)-1:
            last_10_game_list.append([None, None, None, None, None, None, None, None])
        else:
            if len(last_10_games[i+3]) < 2:
                day = date[last_10_games[i+2]] + '0' + last_10_games[i+3]
            else:
                day = date[last_10_games[i+2]] + last_10_games[i+3]
            if '@' in last_10_games[i+4]:
                opp = last_10_games[i+4]
                opp = opp.replace("@", "")
                flag = 0
            else:
                opp = last_10_games[i+4]
                flag = 1
            if last_10_games[i+5] == 'W':
                W_L = 1
            elif last_10_games[i+5] == 'L':
                W_L = 0
            else:
                W_L = 0.5
            if len(last_10_games[i+3]) == 1:
                last_10_games[i+3] = '0' + last_10_games[i+3]
            if last_10_games[i+7] != None:
                record = last_10_games[i+7]
            else:
                record = None
            if last_10_games[i+8] != None:
                place = int(last_10_games[i+8][0])
            else:
                place = None
            if last_10_games[i+9] != None:
                try:
                    GB = float(last_10_games[i+9])
                except:
                    GB = 0.0
            else:
                GB = None
            last_10_game_list.append([day,
                                      flag,
                                      opp,
                                      W_L,
                                      last_10_games[i+6],
                                      record,
                                      place,
                                      GB])
    home["last_10_game"] = last_10_game_list

    ## head_to_head
    try:
        texts = x[0][2]
        texts = texts.replace('(', ' (')
        texts = texts.replace(",", "")
        texts_split = texts.split(" ")
        head_to_head = texts_split.copy()
        while "" in head_to_head:
            head_to_head.remove("")
        for item in head_to_head:
            if "(" in item:
                head_to_head.remove(item)

        head_to_head = head_to_head[head_to_head.index('head-to-head')+1:head_to_head.index('Season')]
        new_head = []
        i = 0
        while i < len(head_to_head):
            if head_to_head[i] in week:
                j = i+1
                while not 'W:' in head_to_head[j]:
                    j += 1
                new_head.append(head_to_head[i+1:j])
                i = j+1
            else:
                i += 1
        head_to_head = []
        for col in new_head:
            day = col[2] + date[col[0]] + col[1]
            if '@' in col[5]:
                flag = 0
                loss = col[5].replace('@', '')
            else:
                flag = 1
                loss = col[5]
            win = col[3]

            head_to_head.append([day, win, loss, flag, int(col[4]), int(col[6])])
    except:
        head_to_head = []
        for i in range(10):
            head_to_head.append([None, None, None, None, None, None])
        
    return road, home, head_to_head

if __name__ == '__main__':
    years = ['2016', '2015', '2014']
    for year in years:
        soup = BeautifulSoup(urlopen('http://www.baseball-reference.com/previews/' + year + '/'))
        paragraphs = soup.find_all('a')
        for i in range(len(paragraphs)):
            if not ('-' in paragraphs[i].text or '/' in paragraphs[i].text):
                break
        if 'ALS' in paragraphs[i].text:
            i += 1
        paragraphs = paragraphs[i:]
        data_times = list(map(lambda x: x.text, paragraphs))
        data_times = list(map(lambda x: x[:-6], data_times))
        data = []
        error_list = []
        length = len(data_times)
        team_name = data_times[0][:3]
        for i in range(length):
            if not year in data_times[i]:
                continue
            if not team_name == data_times[i][:3]:
                with open('data-'+ year + team_name + '.json', 'w') as f:
                    json.dump(data, f)
                data = []
                if error_list:
                    with open('error-'+ year + team_name + '.json', 'w') as f:
                        json.dump(error_list, f)
                    error_list = []
                team_name = data_times[i][:3]
            if os.path.exists('data-' + year + team_name + '.json'):
                continue
            print('{} {} {:06.2f}%'.format( year, team_name, float(i)/length*100))
            try:
                road, home, head_to_head = GetData(year, data_times[i])
                data.append([data_times[i], road, home, head_to_head])
            except:
                error_list.append(data_times[i])

