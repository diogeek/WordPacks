import requests
from sqlite3 import *

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
    return mot

def creer_dresseur(dresseur):
    import sqlite3
    try:
        #connexion à la bdd
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print("Error while connecting to sqlite : ", error)
    
    sql_select_Query = ("INSERT INTO dresseurs (nom) VALUES ('"+str(dresseur)+"')")
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)

    print("dresseur "+str(dresseur)+" créé.")

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()

def ouverture_booster(dresseur):
    url = 'https://www.palabrasaleatorias.com/mots-aleatoires.php?fs=3&fs2=0&Submit=Nouveau+mot'
    code = requests.get(url)
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
    print(liste)
    os.remove('temp.txt')
    capturer_mots(liste,dresseur)
    


#________________________________________________________________________
def capturer_mots(mots,dresseur):
    import sqlite3
    try:
        #connexion à la bdd
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print("Error while connecting to sqlite : ", error)
    sql_select_Query = "select * from dresseurs WHERE nom='"+str(dresseur)+"'"
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)
    record = cursor.fetchall()

    id_dresseur=record[0][0]

    for mot_capture in mots:
        try:
            sql_select_Query = ("INSERT INTO mots (nom,dresseur) VALUES ('"+str(mot_capture)+"','"+str(id_dresseur)+"')")
            cursor = sqliteConnection.cursor()
            cursor.execute(sql_select_Query)
        except:
            sql_select_Query = ("UPDATE mots SET dresseur = '"+str(id_dresseur)+"' WHERE nom = '"+str(mot_capture)+"'")
            cursor = sqliteConnection.cursor()
            cursor.execute(sql_select_Query)

    print("mots "+str(mots)+" capturés.")

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()



#________________________________________________________________________
def afficher_mots(dresseur):
    import sqlite3
    try:
        #connexion à la bdd
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        print("Error while connecting to sqlite : ", error)
    sql_select_Query = "select * from dresseurs WHERE nom='"+str(dresseur)+"'"
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)
    record = cursor.fetchall()

    id_dresseur,nom_dresseur=record[0]

    sql_select_Query = "select * from mots WHERE mots.dresseur='"+str(id_dresseur)+"'"
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)
    record = cursor.fetchall()

    print("Le dresseur {} possède les mots suivants :".format(nom_dresseur, ))
    for raw in record:
        print(raw[0])
    if (sqliteConnection):
        sqliteConnection.close()
"""
dresseur=str(input("créer un nom de dresseur (\"no\" pour skip):"))
if dresseur!="no":
    creer_dresseur(dresseur)  #sert à créer un nouveau dresseur
ouverture_booster(dresseur)   #sert à ouvrir un booster et capturer ses mots
afficher_mots("dionys")       #sert à montrer ta collection de mots
"""
