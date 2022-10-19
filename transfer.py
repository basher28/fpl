import csv
import pandas as pd
import numpy as np
import operator
from collections import Counter

### current team
myteam = ['Trent Alexander-Arnold', 'Neco Williams', 'Joao Cancelo', 'Kieran Trippier', 'Rayan Ait-Nouri',
          'Gabriel Martinelli Silva', 'Josh Dasilva', 'Wilfried Zaha', 'James Maddison', 'Kevin De Bruyne',
          'Dominic Solanke', 'Erling Haaland', 'Gianluca Scamacca']


data = pd.read_csv('merged_gw.csv')
### read in latest data
names = data.name
forwards = {}
midfielders = {}
defenders = {}

### fixture difficulty list 3 is hardest - 1 easiest. Currently has not h/a mods
### so max difficulty for next 3 is 9, lowest is 3

fixdiffdict = {'Arsenal': 3, 'Aston Villa': 1, 'Bournemouth': 1, 'Brentford':2, 'Brighton':2,
           'Chelsea': 3, 'Crystal Palace': 2, 'Everton': 2, 'Fulham':1, 'Leeds':2, 'Leicester': 1,
           'Liverpool': 3, 'Man City': 3, 'Man Utd': 3, 'Newcastle':2, 'Nottingham Forest':1, 'Southampton':1,
           'Spurs':3, 'West Ham':2, 'Wolves':1}


def fixdiff(team):
    
    fixtures = pd.read_csv('epl-2022-UTC.csv')
    rows = fixtures[fixtures.apply(lambda r: r.str.contains(team, case=False).any(), axis=1)] 
    rows = rows.iloc[:3]
    teams = rows.values.tolist()
    oppo = []
    s = 0
    for i in teams:
        #print(i)
        if i[0] == team:
            oppo.append(i[1])
        else:
            oppo.append(i[0])
    for o in oppo:
        s += fixdiffdict.get(o)
    return s


###data management bits
for i in names:
    rows = data.loc[data['name'] == i]
    onerow = rows.head(1)
    position = onerow.iloc[0]['position']
    value = rows.iloc[-1:]
    value = value.iloc[0]['value']
    if position == 'FWD':
        ict = rows['ict_index'].sum() / len(rows)
        ict = round(float(ict),2)
        team = onerow.iloc[0]['team']
        names = str(i)
        forwards[names] = [position, ict, value, team]
    elif position == 'MID':
        ict = rows['ict_index'].sum() / len(rows)
        ict = round(float(ict),2)
        team = onerow.iloc[0]['team']
        names = str(i)
        midfielders[names] = [position, ict, value, team]
    elif position == 'DEF':
        ict = rows['ict_index'].sum() / len(rows)
        ict = round(float(ict),2)
        team = onerow.iloc[0]['team']
        names = str(i)
        defenders[names] = [position, ict, value, team]
    
###dictionaries of player sorted by positions and ict_index
sorted_forwards = dict(sorted(forwards.items(), key=operator.itemgetter(1)))
sorted_midfielders = dict(sorted(midfielders.items(), key=operator.itemgetter(1)))
sorted_defenders = dict(sorted(defenders.items(), key=operator.itemgetter(1)))

def transfer(pos, fee):
    fee = fee*10
    if pos == 'FWD':
        potentials = {}
        for i in sorted_forwards:
            if sorted_forwards[i][2] < fee:
                s = fixdiff(sorted_forwards[i][3])
                potentials[i] = sorted_forwards[i][0], sorted_forwards[i][1], sorted_forwards[i][2], sorted_forwards[i][3], s
    #print(potentials)
    if pos == 'MID':
        potentials = {}
        for i in sorted_midfielders:
            if sorted_midfielders[i][2] < fee:
                s = fixdiff(sorted_midfielders[i][3])
                potentials[i] = sorted_midfielders[i][0], sorted_midfielders[i][1], sorted_midfielders[i][2], sorted_midfielders[i][3], s
        
    if pos == 'DEF':
        potentials = {}
        for i in sorted_defenders:
            if sorted_defenders[i][2] < fee:
                s = fixdiff(sorted_defenders[i][3])
                potentials[i] = sorted_defenders[i][0], sorted_defenders[i][1], sorted_defenders[i][2], sorted_defenders[i][3], s
            
    k = Counter(potentials)
    high = k.most_common(3)
    print('Top 3 transfer prospects:')
    for i in high:
        price = i[1][2] / 10
        print(str(i[0])+' '+str(i[1][1])+' '+str(price)+' '+str(i[1][3]))
        print('fixture difficulty score = '+str(i[1][4]))
        print('\n')
    ###function to check if i(player) is in team already and swap to 4th best
    def isinteam(myteam):
        new = k.most_common(6)
        fourth = new[3]
        fifth = new[4]
        sixth = new[5]
        for i in high:
            #print(high)
            name = i[0]
            for j in myteam:
                if name == j:
                    if fourth not in high:
                        print(i[0]+' is already in your team')
                        high.remove(i)
                        high.append(fourth)
                        print('The next best player is '+ str(fourth))
                        #print(high)
                    elif fifth not in high:
                        print(i[0]+' is already in your team')
                        high.remove(i)
                        high.append(fifth)
                        print('The next best player is '+ str(fifth))
                    else:
                        print(i[0]+' is already in your team')
                        print('The next best player is '+ str(sixth))
            
    isinteam(myteam)

####input position want to change and budget        
transfer('DEF', 7.4)







    
