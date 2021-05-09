import mysql.connector
import sqlconn

def initDatabase():
    conn = sqlconn.sql_conn()
    curs = conn.cursor()
    with open("sql/initDatabase.sql", 'r') as codeFile:
        allCode = [command + '' for command in codeFile.read().split('$$') if command]
        for command in allCode:
            try:
                curs.execute(command)
            except mysql.connector.errors.DatabaseError as err:
                print("addTables Error: " + str(err))    
        conn.commit()
        

def main():
    initDatabase()




if __name__=='__main__':
    main()    