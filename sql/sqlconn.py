import mysql.connector as mysql
import json

def sql_conn():
    auth_dict = {
                        "USER":"",
                        "PASSWORD":"",
                        "DATABASE":""
                }
    try:
            with open("AUTH", 'r') as infile:
                    auth_dict = json.load(infile)
    except:
            with open("AUTH", 'w') as outfile:
                    json.dump(auth_dict, outfile, indent=4)

    try:
        connection = mysql.connect(host='127.0.0.1', 
                            user=auth_dict["USER"], 
                            passwd=auth_dict["PASSWORD"], 
                            db=auth_dict["DATABASE"], 
                            port=3306)
    except ValueError:
            print("Please enter your credentials in AUTH!")
            quit()
    
    
    return connection

def main():
    conn = sql_conn()
    curs = conn.cursor()
    curs.execute("select * from Hero")
    print(curs.fetchall()[0])




if __name__=='__main__':
    main()