import requests
import sqlite3
import datetime

PLACES = [1591974778, 1591974778]


mydb = sqlite3.connect("servers.db") 
cursor = mydb.cursor()

def CheckIfPlace(placeId):
    GetTablesCommand = 'SELECT name from sqlite_master where type= "table"'
    cursor.execute(GetTablesCommand)
    l = cursor.fetchall()
    if str(placeId) in l[0]:
        return True
    return False

def AddTable(placeId):
    AddTableCommand = "CREATE TABLE `{}` (playerCount INT, serverCount INT, averagePing INT, averageFPS INT, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);".format(placeId)
    cursor.execute(AddTableCommand)
    mydb.commit()

def WorkOutAverage(numberslist):
    if numberslist:
        return sum(numberslist)/len(numberslist)
    return 0

def Record(placeId, playerCount, serverCount, AveragePing, AverageFPS):
    if not CheckIfPlace(placeId):
        AddTable(placeId)   
    Record = "INSERT INTO `{}` (playerCount, serverCount, averagePing, averageFPS) VALUES ({}, {}, {}, {})".format(placeId, int(playerCount), int(serverCount), int(AveragePing), int(AverageFPS))
    cursor.execute(Record)  
    mydb.commit()

def GetPlayerCount(ServerDict):
    count = 0
    for i in ServerDict:
        count += i['playing']
    return count

def GetServers(placeId):
    servers = []
    nextpagecursor = " " 
    while nextpagecursor:
        print("While Loop")
        f = requests.get('https://games.roblox.com/v1/games/{}/servers/Public?cursor={}&limit=100&sortOrder=Asc'.format(placeId, nextpagecursor)).json()
        nextpagecursor = f['nextPageCursor']
        for i in f['data']:
            servers.append(i)
    return servers


def ForEveryPlace(placeId):
    s = GetServers(placeId)
    pings = []
    fps = []
    players = 0
    servers = len(s)
    for i in s:
        players += i['playing']
        fps.append(i['fps'])
        pings.append(i['ping'])
    avfps = WorkOutAverage(fps)
    avping = WorkOutAverage(pings)
    Record(placeId, players, servers, avping, avfps)
    
def main():
    for i in PLACES:
        ForEveryPlace(i)
        print("Done: {}".format(i))
            
main()