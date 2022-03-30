import sqlite3
def echanger_mots(mot1,mot2,dresseur1,dresseur2):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print(f"Error while connecting to sqlite : {error}")
        return
    
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur1}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom from mots WHERE nom='{mot1}' and dresseur='{record[0][0]}'")
    record = cursor.fetchall()
    if not record:
        return ("tu n'as pas ce mot")
    
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur2}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom from mots WHERE nom='{mot2}' and dresseur='{record[0][0]}'")
    record = cursor.fetchall()
    if not record:
        return ("tu n'as pas ce mot")

    cursor.execute(f"update mots set dresseur='{dresseur1}' where nom='{mot2}'")
    cursor.execute(f"update mots set dresseur='{dresseur2}' where nom='{mot1}'")
    return("échange réussi")
