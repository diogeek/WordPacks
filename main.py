import requests,sqlite3

def simp(mot):
    mot=mot.replace("Ã©","é")
    mot=mot.replace("Ã¨","è")
    mot=mot.replace("Ãª","ê")
    mot=mot.replace("Ã«","ë")
    mot=mot.replace("Ã¹","ù")
    mot=mot.replace("Ã®","î")
    mot=mot.replace("Ã¯","ï")
    mot=mot.replace("Ã¤","ä")
    mot=mot.replace("Ã¢","â")
    mot=mot.replace("Ã ","à")
    mot=mot.replace("Ã§","ç")
    mot=mot.replace("Ã»","û")
    mot=mot.replace("Ã¼","ü")
    mot=mot.replace("Ã´","ô")
    mot=mot.replace("Ã¶","ö")
    mot=mot.replace("</div>\n","")
    mot=mot.lower()
    return mot

def creer_dresseur(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print("Error while connecting to sqlite : ", error)
        return
    
    sql_select_Query = (f"INSERT INTO dresseurs (nom) VALUES ('{dresseur}')")
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()

def ouverture_booster(dresseur):
    code = requests.get('https://www.palabrasaleatorias.com/mots-aleatoires.php?fs=3&fs2=0&Submit=Nouveau+mot')
    open('temp.txt', 'wb').write(code.content)
    import os
    liste=[]
    lines = []
    with open('temp.txt') as f:
        lines = f.readlines()
        
    liste=[simp(lines[112]),\
           simp(lines[118]),\
           simp(lines[124])\
           ]
    os.remove('temp.txt')
    capturer_mots(liste,dresseur)


#________________________________________________________________________

def capturer_mots(mots,dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print(f"Error while connecting to sqlite : {error}")
        return
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select * from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()

    id_dresseur=record[0][0]

    for mot_capture in mots:
        try:
            cursor = sqliteConnection.cursor()
            cursor.execute(f"INSERT INTO mots (nom,dresseur) VALUES ('{mot_capture}','{id_dresseur}')")
        except:
            cursor = sqliteConnection.cursor()
            cursor.execute(f"INSERT INTO mots (nom,dresseur) VALUES ('{mot_capture}','{id_dresseur}')")

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()
    
    return(mots)

#________________________________________________________________________


def afficher_mots(dresseur):
    try:
        #connexion à la bdd
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print("Error while connecting to sqlite : ", error)
        return
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select * from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()

    id_dresseur,nom_dresseur=record[0]


    cursor.execute(f"select * from mots WHERE mots.dresseur='{id_dresseur}'")
    record = cursor.fetchall()

    if (sqliteConnection):
        sqliteConnection.close()

    return(record)

#_________________________________________________________________________

def echanger_mots(mot1,mot2,dresseur1,dresseur2):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print(f"Error while connecting to sqlite : {error}")
        return
    record1=0
    record2=0
    
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur1}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom from mots WHERE nom='{mot1}' and dresseur='{record[0][0]}'")
    record = cursor.fetchall()
    if record:
        record1 = record[0][0]
    
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur2}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom from mots WHERE nom='{mot2}' and dresseur='{record[0][0]}'")
    record = cursor.fetchall()
    if record:
        record2 = record[0][0]
    if not record1 and not record2:
        return (f"{dresseur1} n'a pas le mot '{mot1}' et {dresseur2} n'a pas le mot '{mot2}'")
    if not record1:
        return (f"{dresseur1} n'a pas le mot '{mot1}'")
    if not record2:
        return (f"{dresseur2} n'a pas le mot '{mot2}'")
    
    cursor.execute(f"update mots set dresseur='{dresseur1}' where nom='{mot2}'")
    cursor.execute(f"update mots set dresseur='{dresseur2}' where nom='{mot1}'")
    return("échange réussi")

