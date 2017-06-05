'''
as filename
this is build data set
output is pickle numpy array

'''

import json
import Score
import os
import numpy as np

path = 'data/'

#Build Dictionary

team_dic = {'Arizona Diamondbacks':'ARI',
            'Atlanta Braves':'ATL',
            'Baltimore Orioles':'BAL',
            'Boston Red Sox':'BOS',
            'Chicago Cubs':'CHN',
            'Chicago White Sox':'CHA',
            'Cincinnati Reds':'CIN',
            'Cleveland Indians':'CLE',
            'Colorado Rockies':'COL',
            'Detroit Tigers':'DET',
            'Miami Marlins':'MIA',
            'Houston Astros':'HOU',
            'Kansas City Royals':'KCA',
            'Los Angeles Angels of Anaheim':'ANA',
            'Los Angeles Dodgers':'LAN',
            'Milwaukee Brewers':'MIL',
            'Minnesota Twins':'MIN',
            'New York Mets':'NYN',
            'New York Yankees':'NYA',
            'Oakland Athletics':'OAK',
            'Philadelphia Phillies':'PHI',
            'Pittsburgh Pirates':'PIT',
            'San Diego Padres':'SDN',
            'San Francisco Giants':'SFN',
            'Seattle Mariners':'SEA',
            'St. Louis Cardinals':'SLN',
            'Tampa Bay Rays':'TBA',
            'Texas Rangers':'TEX',
            'Toronto Blue Jays':'TOR',
            'Washington Nationals':'WAS'
           }
team_dic_o={'Arizona Diamondbacks':'ARI',
            'Atlanta Braves':'ATL',
            'Baltimore Orioles':'BAL',
            'Boston Red Sox':'BOS',
            'Chicago Cubs':'CHC',
            'Chicago White Sox':'CHW',
            'Cincinnati Reds':'CIN',
            'Cleveland Indians':'CLE',
            'Colorado Rockies':'COL',
            'Detroit Tigers':'DET',
            'Miami Marlins':'MIA',
            'Houston Astros':'HOU',
            'Kansas City Royals':'KCR',
            'Los Angeles Angels of Anaheim':'LAA',
            'Los Angeles Dodgers':'LAD',
            'Milwaukee Brewers':'MIL',
            'Minnesota Twins':'MIN',
            'New York Mets':'NYM',
            'New York Yankees':'NYY',
            'Oakland Athletics':'OAK',
            'Philadelphia Phillies':'PHI',
            'Pittsburgh Pirates':'PIT',
            'San Diego Padres':'SDP',
            'San Francisco Giants':'SFG',
            'Seattle Mariners':'SEA',
            'St. Louis Cardinals':'STL',
            'Tampa Bay Rays':'TBR',
            'Texas Rangers':'TEX',
            'Toronto Blue Jays':'TOR',
            'Washington Nationals':'WAS'
           }
team_dic_o_inv = {v: k for k, v in team_dic_o.items()}
team_dic_o_inv['WSN'] = 'Washington Nationals'
team_dic_o_inv['ANA'] = 'Los Angeles Angels of Anaheim'

team_encode = {}
temp = list(team_dic.values())
code = np.eye(30)
for i in range(30):
    team_encode[temp[i]] = code[i]
    
def Arrayize(a1):
    team_name = team_encode[team_dic[a1['Team name']]]
    
    home = []
    for i in a1['Home'].split('-'):
        home.append(int(i))
    home = np.array(home)

    road = []
    for i in a1['Road'].split('-'):
        road.append(int(i))
    road = np.array(road)

    extr_inn = []
    for i in a1['ExtrInn'].split('-'):
        extr_inn.append(int(i))
    extr_inn = np.array(extr_inn)

    rhp = []
    for i in a1['vsRHP'].split('-'):
        rhp.append(int(i))
    rhp = np.array(rhp)

    lhp= []
    for i in a1['vsLHP'].split('-'):
        lhp.append(int(i))
    lhp = np.array(lhp)

    one_run= []
    for i in a1['1-Run'].split('-'):
        one_run.append(int(i))
    one_run = np.array(one_run)

    il= []
    for i in a1['IL'].split('-'):
        il.append(int(i))
    il = np.array(il)

    road_data = np.concatenate((team_name, home, road, extr_inn, rhp, lhp, one_run, il))

    last_10_game = a1['last_10_game']

    for temp in last_10_game:
        if None in temp:
            np.zeros(39*2)
        else:
            temp_encode = []

            #temp_encode.append(int(temp[0]))
            temp_encode.append(temp[1])
            temp_encode.append(temp[3])

            for i in temp[4].split('-'):
                temp_encode.append(int(i))

            for i in temp[5].split('-'):
                temp_encode.append(int(i))

            temp_encode.append(temp[6])
            temp_encode.append(temp[7])

            t_e = team_encode[team_dic[team_dic_o_inv[temp[2]]]]
            temp_encode = np.array(temp_encode)
            road_data = np.concatenate((road_data, np.ones(39), temp_encode, t_e))
            
    return road_data

def TenGameArray(a3):
    j = 0
    for i in a3:
        temp = []
        #temp.append(int(i[0]))
        temp.append(i[3])
        temp.append(i[4])
        temp.append(i[5])
        temp = np.array(temp)
        r = team_encode[team_dic[team_dic_o_inv[i[1]]]]
        h = team_encode[team_dic[team_dic_o_inv[i[2]]]]
        if j == 0:
            ten_game = np.concatenate((temp, r, h))
            j+=1
        else:
            ten_game = np.concatenate((ten_game, temp, r, h))
    return ten_game

x_data = []
y_data = []
error = []

for filename in os.listdir(path):
    real_path = path+filename
    print(real_path)
    with open(real_path) as data_file:    
        data = json.load(data_file)
    for i in data:
        print(i[0])
        try:
            road_data = Arrayize(i[1])
            home_data = Arrayize(i[2])
            ten_game = TenGameArray(i[3])
            preview = np.concatenate((road_data,home_data,ten_game))
            
            y_data.append(Score.WinOrLoss(Score.FindScore(i[0]) )) 
            print(i[0]+'y done')
            x_data.append(preview.tolist())
            print(i[0]+'x done')
        except:
            print('error')
            error.append(i[0])
            
x_data = np.array(x_data)
y_data = np.array(y_data)

import pickle
output = open('data.pkl','wb')
data = (x_data, y_data)
pickle.dump(data, output)
print("data done")

output = open('error.pkl','wb')
pickle.dump(error, output)
print("data done")