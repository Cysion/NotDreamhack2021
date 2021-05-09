import mysql.connector
import sql.sqlconn
from datetime import datetime

#Template
#quest:[heroId, name, description, reward, priority, repeatable, startTime, duration, active],
#item:[heroId, name, description, duration, cost]
#hero:[heroId, name]



def addQuest(questDict):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"""insert into Quest (HeroId, QuestName, QuestDescription, 
                Reward, Prio, RepeatableQuest, startTime, Duration, ActiveQuest) values 
                ({questDict['heroId']}, '{questDict['name']}', '{questDict['description']}',
                {int(questDict['reward'])}, {int(questDict['priority'])}, '{questDict['repeatable']}',
                '{questDict['startTime']}', {int(questDict['duration'])}, {'true' if questDict['active'] == 'yes' else 'false'}) """
    try:
        curs.execute(sqlQuery)
    except mysql.connector.errors.DatabaseError as err:
        print("addTables Error: " + str(err))    
    else:
        conn.commit()

def addItem(itemDict):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"""insert into Item (HeroId, ItemName, ItemDescription, Duration, Cost) values 
                ({itemDict['heroId']}, '{itemDict['name']}', '{itemDict['description']}',
                {int(itemDict['duration'])}, {int(itemDict['cost'])}) """
    try:
        curs.execute(sqlQuery)
    except mysql.connector.errors.DatabaseError as err:
        print("addTables Error: " + str(err))    
    else:
        conn.commit()

def getShop(heroId):
    """Returns (list of dicts containing items, gold in users inventory)"""
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"select * from Item where HeroId = {heroId}"
    curs.execute(sqlQuery)
    toReturn = []
    for c in curs.fetchall():
        toReturn.append({'heroId':c[1], 'name':c[2], 'description':c[3], 'duration':f'{c[4]//60}H {c[4]%60}M', 'cost':c[5]})
    sqlQuery = f"select Gold from Hero where HeroId = {heroId}"
    curs.execute(sqlQuery)
    return toReturn, curs.fetchall()[0][0]

def purchase(heroId, itemId):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"select Cost from Item where HeroId = {heroId} and ItemId = {itemId}"
    curs.execute(sqlQuery)
    try:
        cost = curs.fetchall()[0][0]
    except IndexError:
        raise IndexError("Item does not exist")
    sqlQuery = f"select Gold from Hero where HeroId = {heroId}"
    curs.execute(sqlQuery)
    try:
        gold = curs.fetchall()[0][0]
    except IndexError:
        raise IndexError("Hero does not exist")
    if gold >= cost:
        sqlQuery = f"update Hero set Gold = Gold-{cost} where HeroId = {heroId}"
        curs.execute(sqlQuery)
        conn.commit()
        return True
    return False

def getQuestLog(heroId, active = 1):
    """Returns list of dicts containing quests in questlog"""
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"select * from Quest where HeroId = {heroId} and ActiveQuest = {active}"
    curs.execute(sqlQuery)
    toReturn = []
    for c in curs.fetchall():
        toReturn.append({'heroId':c[1], 'name':c[2], 'description':c[3], 'reward':f'{c[4]} Gold', 'priority':c[5], 'repeatable':c[6], 'startTime':str(c[7]), 'duration':f'{c[8]//60}H {c[8]%60}M', 'active':c[9]})
    return toReturn

def registerHero(heroDict):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    
    sqlQuery = f"select * from Hero where HeroId = {heroDict['heroId']}"
    curs.execute(sqlQuery)
    if not curs.fetchall():
        sqlQuery = f"insert into Hero(HeroId, HeroName, Gold) values ({heroDict['heroId']}, '{heroDict['name']}', 0)"
        curs.execute(sqlQuery)
        conn.commit()
    else:
        raise ValueError("Hero already exists")


def turnIn(heroId, questId):
    pass

def abandon(heroId, questId):
    pass


def checkId(heroId):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()
    sqlQuery = f"select HeroId from Hero where HeroId={heroId}"
    try:
        curs.execute(sqlQuery)
    except mysql.connector.errors.DatabaseError as err:
        print("addTables Error: " + str(err))   
    return False if curs.fetchall() == [] else True

def main():
    """
    print(checkId(1))
    quest = {
        'heroId':1,
        'name':'Jaina Proudmoore rampage',
        'description':'Purge Dalaran by killing every single one of those filthy blood elfes',
        'reward':'500',
        'priority':'2',
        'repeatable':'daily',
        'startTime':'2020-05-09 21:00:00',
        'duration':'30',
        'active':'no'
    }
    addQuest(quest)

    item = {
        'heroId':1,
        'name':'Play WoW',
        'description':'Play WoW',
        'duration': 120,
        'cost': 800
    }
    addItem(item)
    
    """
    #print(getQuestLog(1))
    #print(getShop(1))

    #print(purchase(1,1))
    
    registerHero({'heroId':55,'name':'Pelle2'})




if __name__ == '__main__':
    main()
