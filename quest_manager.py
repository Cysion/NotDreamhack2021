import mysql.connector
import sql.sqlconn

#Template
#quest:[heroId, name, description, reward, priority, repeatable, startTime, duration],
#item:[heroId, name, description, duration, cost]
#hero:[heroId, name]



def addQuest(questDict):
    conn = sql.sqlconn.sql_conn()
    curs = conn.cursor()

    sqlQuery = f"""insert into Quest (HeroId, QuestName, QuestDescription, 
                Reward, Prio, RepeatableQuest, startTime, Duration) values 
                ({questDict['heroId']}, '{questDict['name']}', '{questDict['description']}',
                {int(questDict['reward'])}, {int(questDict['priority'])}, '{questDict['repeatable']}',
                '{questDict['startTime']}', {int(questDict['duration'])}) """
    try:
        curs.execute(sqlQuery)
    except mysql.connector.errors.DatabaseError as err:
        print("addTables Error: " + str(err))    
    else:
        conn.commit()

def addItem(itemDict):
    pass

def getShop(userId):
    """Returns (list of dicts containing items, gold in users inventory)"""
    pass

def purchase(userId, itemId):
    pass

def getQuestLog(userId):
    """Returns list of dicts containing quests in questlog"""
    pass

def registerHero(heroDict):
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
    print(checkId(1))
    """quest = {
        'heroId':54,
        'name':'Jaina Proudmoore rampage',
        'description':'Purge Dalaran by killing every single one of those filthy blood elfes',
        'reward':'500',
        'priority':'2',
        'repeatable':'daily',
        'startTime':'2020-05-09 21:00:00',
        'duration':'30'
    }
    addQuest(quest)
    """
if __name__ == '__main__':
    main()