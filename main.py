import requests,sqlite3
#from bs4 import BeautifulSoup
import datetime

cooldown_value=12
taille_booster=3
boosters_max=3

#creation de la db si elle n'existe pas
try:
  sqliteConnection = sqlite3.connect('WordPacks.db')
  cursor = sqliteConnection.cursor()
  cursor.execute(f"CREATE TABLE IF NOT EXISTS dresseurs ('ID' INT UNIQUE, 'nom' TEXT, 'cooldown' TEXT, 'boosters_dispo' INT, 'points' INT, PRIMARY KEY ('ID'));")
  cursor.execute(f"CREATE TABLE IF NOT EXISTS mots ('nom' TEXT UNIQUE, 'dresseur' INT, 'rarete' INT, PRIMARY KEY ('nom'));")
  sqliteConnection.commit()
  sqliteConnection.close()
except sqlite3.Error as error:
  print(f"Error while connecting to sqlite : {error}")

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
      
    cursor = sqliteConnection.cursor()
    cursor.execute(f"INSERT INTO dresseurs (nom,cooldown,boosters_dispo,points) VALUES ('{dresseur}','{datetime.datetime.now()-datetime.timedelta(days=1)}',5,0)")

    sqliteConnection.commit()
    
    if (sqliteConnection):
        sqliteConnection.close()

def ouverture_booster(dresseur,nb=1):
  try:
      sqliteConnection = sqlite3.connect('WordPacks.db')
  except sqlite3.Error as error:
      return(f"Error while connecting to sqlite : {error}")
  cursor = sqliteConnection.cursor()
  cursor.execute(f"UPDATE dresseurs SET boosters_dispo=boosters_dispo-{nb} WHERE nom='{dresseur}'")
  sqliteConnection.commit()
  cursor.execute(f"SELECT boosters_dispo from dresseurs WHERE nom='{dresseur}'")
  boosters_restants=cursor.fetchall()[0][0]
  if (sqliteConnection):
    sqliteConnection.close()
  global taille_booster
  code = requests.get(f'https://www.palabrasaleatorias.com/mots-aleatoires.php?fs={nb*taille_booster}&fs2=0&Submit=Nouveau+mot', timeout=(3.05,1))
  #else: code = requests.get('https://www.textfixerfr.com/outils/generateur-de-mots-aleatoires.php') faut trouver un moyen de faire marcher ça
  #else: code = requests.get('http://romainvaleri.online.fr/' ça aussi
  lines=list(code.iter_lines())
  decalage=0
  liste=[simp(lines[112+decalage+i*6].decode("utf-8")) if simp(lines[112+i*6].decode("utf-8"))!='<br /><div style="font-size:3em; color:#6200c5;">' else simp(lines[113+i*6].decode("utf-8")) for i in range(nb*taille_booster)]
  if '<br /><div style="font-size:3em; color:#6200c5;">' in liste:
    print(lines[110:126])
  return(capturer_mots(liste,dresseur),boosters_restants)

def cooldown_ready(dresseur):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select cooldown from dresseurs WHERE nom='{dresseur}'")
    cooldown = datetime.datetime.strptime(cursor.fetchall()[0][0], '%Y-%m-%d %H:%M:%S.%f')
    if cooldown<datetime.datetime.now()-datetime.timedelta(hours=cooldown_value):
      if sqliteConnection:
        sqliteConnection.close()
      return (True,None)
    if sqliteConnection:
      sqliteConnection.close()
    return (False,str(cooldown-(datetime.datetime.now()-datetime.timedelta(hours=cooldown_value)))[:-7])
  
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
            cursor.execute(f"INSERT INTO mots (nom,dresseur,rarete) VALUES ('{mot_capture}','{id_dresseur}',1)")
        except sqlite3.IntegrityError:
            cursor = sqliteConnection.cursor()
            cursor.execute(f"UPDATE mots SET rarete=rarete+1 WHERE dresseur='{id_dresseur}' AND nom='{mot_capture}' AND rarete<4")
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
    cursor.execute(f"select nom,rarete from mots WHERE mots.dresseur='{record[0][0]}'ORDER BY rarete DESC")
    record = [f"{mot[0]} ({mot[1]})" for mot in cursor.fetchall()]
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
    cursor.execute(f"DELETE from dresseurs WHERE nom='{dresseur}'")
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

#___________________________________________

def boosters_dispo(dresseur,nb=1):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"select boosters_dispo from dresseurs WHERE nom={dresseur}")
    record=cursor.fetchall()[0][0]
    if nb-record<=0:
      cursor.execute(f"UPDATE dresseurs SET cooldown='{datetime.datetime.now()}' WHERE nom='{dresseur}'")
    sqliteConnection.commit()
    if sqliteConnection:
      sqliteConnection.close()
    return (nb <= record,record)

#__________________________________________

def remplir_boosters(dresseur,nb=boosters_max):
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"UPDATE dresseurs SET boosters_dispo={nb} WHERE nom={dresseur}")
    sqliteConnection.commit()
    if sqliteConnection:
      sqliteConnection.close()
    return

#___________________________________________

def upgrade(dresseur,nb=1):
  dispo,nb_dispo=boosters_dispo(dresseur,nb)
  if dispo:
    try:
        sqliteConnection = sqlite3.connect('WordPacks.db')
    except sqlite3.Error as error:
        return(f"Error while connecting to sqlite : {error}")
    cursor = sqliteConnection.cursor()
    cursor.execute(f"UPDATE dresseurs SET boosters_dispo=boosters_dispo-{nb} WHERE nom={dresseur}")
    cursor.execute(f"SELECT nom FROM mots ORDER BY RANDOM() LIMIT {nb*2}")
    randomwords="'"+("', '").join([i[0] for i in cursor.fetchall()])+"'"
    cursor.execute(f"UPDATE mots SET rarete=rarete+1 WHERE nom IN ({randomwords})")
    sqliteConnection.commit()
    if sqliteConnection:
      sqliteConnection.close()
    return(f"Bravo <@{dresseur}> ! Vous avez sacrifié {nb} booster{'s' if nb!=1 else ''} et avez upgrade les mots suivants : {randomwords}. Il vous reste {nb_dispo-nb} boosters !")
  else: return(f"Désolé <@{dresseur}>, vous n'avez que {nb_dispo} boosters !")

#______________________________________________

def info(dresseur,nom):
  from random import choice
  try:
    sqliteConnection = sqlite3.connect('WordPacks.db')
  except sqlite3.Error as error:
    return(f"Error while connecting to sqlite : {error}")
  cursor = sqliteConnection.cursor()
  cursor.execute(f"SELECT nom,points,boosters_dispo FROM dresseurs where nom={dresseur}")
  record=cursor.fetchall()[0]
  print(record)
  return(f"```DRESSEUR '{nom.upper()}'```\n\
{choice([':person_bowing:',':person_doing_cartwheel:',':person_facepalming:',':person_raising_hand:',':person_running:',':person_tipping_hand:',':person_in_lotus_position:',':person_in_tuxedo:',':person_in_manual_wheelchair:',':person_in_motorized_wheelchair:',':person_in_steamy_room:',':person_playing_handball:',':person_pouting:',':person_shrugging:',':person_standing:',':person_frowning:',':person_gesturing_no:',':person_gesturing_ok:',':person_getting_massage:',':person_golfing:',':person_juggling:',':person_kneeling:',':person_lifting_weights:',':person_walking:',':person_with_probing_cane:',':person_bouncing_ball:'])} _Nom_ : `{nom}`\n\n\
:slot_machine: _Score_ : `{record[1]}`\n\n\
:red_envelope: _Boosters Disponibles_ : `{record[2]}`\n\n\
||<@{record[0]}>||")