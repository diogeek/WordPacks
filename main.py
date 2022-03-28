import requests,sqlite3
from bs4 import BeautifulSoup
import datetime

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
    mot=mot.replace("</div>","")
    mot=mot.replace("\n","")
    mot=mot.lower()
    return mot

def creer_dresseur(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    
    sql_select_Query = (f"INSERT INTO dresseurs (nom,cooldown) VALUES ('{dresseur}',{datetime.datetime.now()-timedelta(hours=20)})")
    cursor = sqliteConnection.cursor()
    cursor.execute(sql_select_Query)

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()

def ouverture_booster(dresseur):
  from random import randint
  code = requests.get('https://www.palabrasaleatorias.com/mots-aleatoires.php?fs=3&fs2=0&Submit=Nouveau+mot')
  #else: code = requests.get('https://www.textfixerfr.com/outils/generateur-de-mots-aleatoires.php') faut trouver un moyen de faire marcher ça
  #else: code = requests.get('http://romainvaleri.online.fr/' ça aussi
  lines=list(code.iter_lines())
  liste=[simp(lines[112].decode("utf-8")),\
         simp(lines[118].decode("utf-8")),\
         simp(lines[124].decode("utf-8"))\
         ]
  return(capturer_mots(liste,dresseur))

def cooldown_ready(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select cooldown from dresseurs WHERE nom='{dresseur}'")
    cooldown = cursor.fetchall()[0][0]
    if cooldown<datetime.datetime.now()-timedelta(hours=12):
      return (True,cooldown<datetime.datetime.now()-timedelta(hours=20))
    return (False,cooldown<datetime.datetime.now()-timedelta(hours=20))
  
#________________________________________________________________________

def capturer_mots(mots,dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select * from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()

    id_dresseur=record[0][0]

    for mot_capture in mots:
        try:
            cursor = sqliteConnection.cursor()
            cursor.execute(f"INSERT INTO mots (nom,dresseur) VALUES ('{mot_capture}','{id_dresseur}')")
        except sqlite3.IntegrityError:
            cursor = sqliteConnection.cursor()
            cursor.execute(f"UPDATE mots SET dresseur = '{id_dresseur}' WHERE nom= '{mot_capture}'")

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
        return(f"Error while connecting to sqlite : {error}")
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

def check_mot(mot,dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
        return
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom from mots WHERE nom='{mot}' and dresseur='{record[0][0]}'")
    record = cursor.fetchall()
    if (sqliteConnection):
        sqliteConnection.close()
      
    if record:
        return(record[0][0])
    else:
        return("")

def echanger_mots(mot1,mot2,dresseur1,dresseur2):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    record1=0
    record2=0
    
    record1=check_mot(mot1,dresseur1)
    record2=check_mot(mot2,dresseur2)
    """
    if not record1 and not record2 :
        return (f"@{dresseur1} n'a pas le mot '{mot1}' et @{dresseur2} n'a pas le mot '{mot2}'")
    if not record1:
        return (f"@{dresseur1} n'a pas le mot '{mot1}'")
    if not record2:
        return (f"@{dresseur2} n'a pas le mot '{mot2}'")
    """
    cursor = sqliteConnection.cursor()
    cursor.execute(f"update mots set dresseur='{dresseur1}' where nom='{mot2}'")
    cursor.execute(f"update mots set dresseur='{dresseur2}' where nom='{mot1}'")
    sqliteConnection.commit()
    if (sqliteConnection):
        sqliteConnection.close()
    return(f"Échange **complété** ! @{dresseur1} possède maintenant '{mot2}', et @{dresseur2} possède maitenant '{mot1}'")

#______________________________________________

def suppression_dresseur(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    cursor.execute(f"DELETE from mots WHERE dresseur='{record[0][0]}'")
    cursor.execute(f"DELETE from dresseurs WHERE ID={record[0][0]}")
    sqliteConnection.commit()
    if (sqliteConnection):
        sqliteConnection.close()
    return(f"Dresseur <@{dresseur}> supprimé avec succès. On est tristes de vous voir partir !")

#___________________________________________

def check_dresseur_existe(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    return not not record

#___________________________________________

def liste_dresseurs():
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select nom from dresseurs")
    record = cursor.fetchall()
    return record