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
  cursor.execute(f"CREATE TABLE IF NOT EXISTS dresseurs ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'nom' TEXT, 'cooldown' TEXT, 'boosters_dispo' INT, 'points' INT);")
  cursor.execute(f"CREATE TABLE IF NOT EXISTS mots ('nom' TEXT PRIMARY KEY, 'dresseur' INT, 'rarete' INT);")
  cursor.execute(f"CREATE TABLE IF NOT EXISTS echange ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'nom' TEXT,'dresseur1' TEXT, 'dresseur2' TEXT, 'mot1' TEXT, 'mot2' TEXT, 'halfcomplete' INT, 'origine' TEXT)")
  cursor.execute(f"CREATE TABLE IF NOT EXISTS prefixes ('serveur' TEXT PRIMARY KEY,'prefix' TEXT)")
  sqliteConnection.commit()
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
    mot=mot.replace("œ","oe")
    mot=mot.replace("</div>","")
    mot=mot.replace("\n","")
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZéèêëùîïäâàçûüôö-')
    mot = ''.join(filter(whitelist.__contains__, mot))
    mot=mot.lower()
    return mot

#________________________________________________________________________

def creer_dresseur(dresseur):
    cursor.execute(f"INSERT INTO dresseurs (nom,cooldown,boosters_dispo,points) VALUES ('{dresseur}','{datetime.datetime.now()-datetime.timedelta(days=1)}',5,0)")
    sqliteConnection.commit()
    return

#________________________________________________________________________

def ouverture_booster(dresseur,nb=1):
  cursor.execute(f"UPDATE dresseurs SET boosters_dispo=boosters_dispo-{nb} WHERE nom='{dresseur}'")
  sqliteConnection.commit()
  cursor.execute(f"SELECT boosters_dispo from dresseurs WHERE nom='{dresseur}'")
  boosters_restants=cursor.fetchall()[0][0]
  global taille_booster
  code = requests.get(f'https://www.palabrasaleatorias.com/mots-aleatoires.php?fs={nb*taille_booster}&fs2=0&Submit=Nouveau+mot', timeout=(3.05,1))
  #else: code = requests.get('https://www.textfixerfr.com/outils/generateur-de-mots-aleatoires.php') faut trouver un moyen de faire marcher ça
  #else: code = requests.get('http://romainvaleri.online.fr/' ça aussi
  lines=list(code.iter_lines())
  decalage=0
  liste=[simp(lines[112+decalage+i*6].decode("utf-8")) if simp(lines[112+i*6].decode("utf-8"))!='br div stylefont-sizeem colorc' else simp(lines[113+i*6].decode("utf-8")) for i in range(nb*taille_booster)]
  return(capturer_mots(liste,dresseur),boosters_restants)

#________________________________________________________________________

def cooldown_ready(dresseur):
    cursor.execute(f"select cooldown from dresseurs WHERE nom='{dresseur}'")
    cooldown = datetime.datetime.strptime(cursor.fetchall()[0][0], '%Y-%m-%d %H:%M:%S.%f')
    if cooldown<datetime.datetime.now()-datetime.timedelta(hours=cooldown_value):
      return (True,None)
    return (False,str(cooldown-(datetime.datetime.now()-datetime.timedelta(hours=cooldown_value)))[:-7])
  
#________________________________________________________________________

def capturer_mots(mots,dresseur):
    cursor.execute(f"select * from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()

    id_dresseur=record[0][0]
    mots_upgrade,mots_final=[],[]
    for mot_capture in mots:
        try:
            cursor.execute(f"INSERT INTO mots (nom,dresseur,rarete) VALUES ('{mot_capture.split(' ',1)[0]}','{id_dresseur}',1)")
            mots_final.append(mot_capture)
        except sqlite3.IntegrityError:
            cursor.execute(f"UPDATE mots SET rarete=rarete+1 WHERE dresseur='{id_dresseur}' AND nom='{mot_capture}' AND rarete<4")
            cursor.execute(f"SELECT nom FROM mots WHERE dresseur='{id_dresseur}' AND nom='{mot_capture}'")
            try: mots_upgrade.append(cursor.fetchall()[0][0])
            except IndexError :
              cursor.execute(f"UPDATE mots SET dresseur = '{id_dresseur}' WHERE nom='{mot_capture}'")
              mots_final.append(mot_capture)
    sqliteConnection.commit()
    return(mots_final,mots_upgrade)

#________________________________________________________________________


def afficher_mots(dresseur):
    cursor.execute(f"select * from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom,rarete from mots WHERE mots.dresseur='{record[0][0]}'ORDER BY rarete DESC")
    record = [f"{mot[0]} ({mot[1]})" for mot in cursor.fetchall()]
    return(record,len(record))

#_________________________________________________________________________

def check_mot(mot,dresseur):
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    cursor.execute(f"select nom,rarete from mots WHERE nom='{mot}' and dresseur='{record[0][0]}'")
    try:return(list(cursor.fetchall()[0]))
    except IndexError: return("")

#_________________________________________________________________________

def echanger_mots(channel):
    cursor.execute(f"SELECT dresseur1,dresseur2 FROM echange WHERE nom='{channel}'")
    record=list(cursor.fetchall()[0])
    final=list(record)
    for i in record:
      cursor.execute(f"SELECT ID FROM dresseurs WHERE nom='{i}'")
      final.append(cursor.fetchall()[0][0])
    cursor.execute(f"SELECT mot1,mot2 FROM echange WHERE nom='{channel}'")
    final=final[2:]+list(cursor.fetchall()[0])
    cursor.execute(f"SELECT rarete from mots WHERE nom IN ('{final[2]}','{final[3]}') ORDER BY rarete LIMIT 1")
    rarete=cursor.fetchall()[0][0]
    cursor.executescript(f"""UPDATE mots SET dresseur='{final[0]}' WHERE nom='{final[3]}';
UPDATE mots SET dresseur='{final[1]}' WHERE nom='{final[2]}';
UPDATE mots SET rarete=('{rarete}') WHERE nom in ('{final[2]}','{final[3]}');
DELETE FROM echange WHERE nom='{channel}'""")
    sqliteConnection.commit()
    return(f"Échange **complété** ! <@{record[0]}> possède maintenant '{final[3]}', et <@{record[1]}> possède maitenant '{final[2]}'. les 2 mots sont maintenant de rareté `{rarete}`")

#______________________________________________

def suppression_dresseur(dresseur):
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    record = cursor.fetchall()
    cursor.executescript(f"""DELETE from mots WHERE dresseur='{record[0][0]}';
DELETE from dresseurs WHERE nom='{dresseur}'""")
    sqliteConnection.commit()
    return(f"Dresseur <@{dresseur}> supprimé avec succès. On est tristes de vous voir partir !")

#___________________________________________

def check_dresseur_existe(dresseur):
    cursor.execute(f"select ID from dresseurs WHERE nom='{dresseur}'")
    return not not cursor.fetchall()

#___________________________________________

def liste_dresseurs():
    cursor.execute(f"select nom from dresseurs")
    return [i[0] for i in cursor.fetchall()]
#___________________________________________

def boosters_dispo(dresseur,nb=1):
    cursor.execute(f"select boosters_dispo from dresseurs WHERE nom={dresseur}")
    record=cursor.fetchall()[0][0]
    if nb-record<=0:
      cursor.execute(f"UPDATE dresseurs SET cooldown='{datetime.datetime.now()}' WHERE nom='{dresseur}'")
    sqliteConnection.commit()
    return (nb <= record,record)

#__________________________________________

def remplir_boosters(dresseur,nb=boosters_max):
    cursor.execute(f"UPDATE dresseurs SET boosters_dispo={nb} WHERE nom={dresseur}")
    sqliteConnection.commit()
    return

#___________________________________________

def upgrade(dresseur,nb=1):
  cursor.execute(f"SELECT ID from dresseurs WHERE nom={dresseur}")
  id=cursor.fetchall()[0][0]
  cursor.execute(f"SELECT * from mots WHERE dresseur={id}")
  try : nb_mots=len(list(cursor.fetchall()[0]))
  except IndexError: return(f"Désolé <@{dresseur}>, vous n'avez encore aucun mot !")
  if nb_mots>1:
    dispo,nb_dispo=boosters_dispo(dresseur,nb)
    if dispo:
      cursor.execute(f"UPDATE dresseurs SET boosters_dispo=boosters_dispo-{nb} WHERE nom={dresseur}")
      cursor.execute(f"SELECT nom FROM mots WHERE dresseur={id} ORDER BY RANDOM() LIMIT {nb*2}")
      randomwords="'"+("', '").join([i[0] for i in cursor.fetchall()])+"'"
      cursor.execute(f"UPDATE mots SET rarete=rarete+1 WHERE nom IN ({randomwords})")
      sqliteConnection.commit()
      return(f"Bravo <@{dresseur}> ! Vous avez sacrifié {nb} booster{'s' if nb!=1 else ''} et avez upgrade les mots suivants : {randomwords}. Il vous reste {nb_dispo-nb} boosters !")
    else: return(f"Désolé <@{dresseur}>, vous n'avez que {nb_dispo} boosters !")
  else: return(f"Désolé <@{dresseur}>, vous n'avez pas assez de mots !")

#___________________________________________

def info(dresseur,nom,auteur=None):
  from random import choice
  cursor.execute(f"SELECT ID,nom,points,boosters_dispo FROM dresseurs WHERE nom='{dresseur}'")
  record=list(cursor.fetchall()[0])
  cursor.execute(f"SELECT COUNT(*),MAX(rarete) from mots where dresseur={record[0]};")
  record.extend(list(cursor.fetchall()[0]))
  return(f"```DRESSEUR '{nom.upper()}'```\n\
{choice([':person_bowing:',':person_doing_cartwheel:',':person_facepalming:',':person_raising_hand:',':person_running:',':person_tipping_hand:',':person_in_lotus_position:',':person_in_tuxedo:',':person_in_manual_wheelchair:',':person_in_motorized_wheelchair:',':person_in_steamy_room:',':person_playing_handball:',':person_pouting:',':person_shrugging:',':person_standing:',':person_frowning:',':person_gesturing_no:',':person_gesturing_ok:',':person_getting_massage:',':person_golfing:',':person_juggling:',':person_kneeling:',':person_lifting_weights:',':person_walking:',':person_with_probing_cane:',':person_bouncing_ball:'])} _Nom_ : `{nom}`\n\n\
:capital_abcd: _Mots possédés_ : `{record[4]}`\n\n\
:star: _Rareté la plus haute possédée_ : `{record[5] if record[5] else 'Aucune'}`\n\n\
:slot_machine: _Score_ : `{record[2]}`\n\n\
:trophy: _Position dans le Classement_ : `{pos_classement(dresseur)}`\n\n\
:red_envelope: _Boosters disponibles_ : `{record[3]}`\n\n\
||<@{auteur if auteur is not None else dresseur}>||")

#___________________________________________

def proposer_echange(dresseur1,dresseur2,origine):
  cursor.execute(f"SELECT * FROM echange WHERE dresseur1='{dresseur1}' AND dresseur2='{dresseur2}'")
  if not cursor.fetchall():
    cursor.execute(f"INSERT INTO echange (nom, dresseur1, dresseur2, mot1, mot2, halfcomplete, origine) VALUES ('', '{dresseur1}', '{dresseur2}', '', '', 0, '{origine}')")
  sqliteConnection.commit()
  return

#___________________________________________

def creer_channel_echange(channel_echange,dresseur1,dresseur2):
  cursor.execute(f"UPDATE echange SET nom='{channel_echange}' WHERE dresseur1='{dresseur1}' AND dresseur2='{dresseur2}'")
  sqliteConnection.commit()
  return

def delete_channel_echange(channel_echange):
  cursor.execute(f"DELETE FROM echange WHERE id='{channel_echange}'")
  sqliteConnection.commit()
  return

#___________________________________________

def changer_mot(channel,dresseur,mot):
  cursor.execute(f"SELECT * FROM echange WHERE nom='{channel}'")
  record=list(cursor.fetchall()[0])
  cursor.execute(f"UPDATE echange SET mot{record.index(str(dresseur))-1}='{mot}' WHERE dresseur{record.index(str(dresseur))-1}='{dresseur}' AND nom='{channel}'")
  sqliteConnection.commit()
  cursor.execute(f"SELECT rarete FROM mots WHERE nom='{mot}'")
  return cursor.fetchall()[0][0]

#___________________________________________

def halfcomplete(channel):
  cursor.execute(f"SELECT halfcomplete FROM echange WHERE nom='{channel}'")
  return [False,True][cursor.fetchall()[0][0]]

def confirmer_mot(channel):
  cursor.execute(f"UPDATE echange SET halfcomplete=1 WHERE nom='{channel}'")
  sqliteConnection.commit()
  return

#___________________________________________

def dresseur1(dresseur):
  cursor.execute(f"SELECT nom FROM echange WHERE dresseur1='{dresseur}'")
  return [i[0] for i in cursor.fetchall()]

def dresseur2(dresseur):
  cursor.execute(f"SELECT id,nom,dresseur1 FROM echange WHERE dresseur2='{dresseur}'")
  return cursor.fetchall()

#___________________________________________

def origine(channel):
  cursor.execute(f"SELECT origine FROM echange WHERE nom='{channel}'")
  return int(cursor.fetchall()[0][0])

#___________________________________________

def changer_prefix(serveur,prefix):
  cursor.execute(f"UPDATE prefixes SET prefix='{prefix}' WHERE serveur='{serveur}'")
  sqliteConnection.commit()
  return (f"Le prefix des commandes est maintenant `{prefix}` sur ce serveur !")

#___________________________________________

def get_prefix(serveur):
  cursor.execute(f"SELECT prefix FROM prefixes WHERE serveur='{serveur}'")
  return cursor.fetchall()[0][0]

#___________________________________________

def ajouter_serveur(serveur):
  cursor.execute(f"INSERT OR IGNORE INTO prefixes('serveur','prefix') VALUES ('{serveur}','!')")
  sqliteConnection.commit()
  return

#___________________________________________

def pos_classement(dresseur):
  cursor.execute(f"SELECT COUNT(*) + 1 RowNum FROM dresseurs WHERE points > (SELECT points FROM dresseurs WHERE nom='{dresseur}');")
  return(cursor.fetchall()[0][0])

def classement(dresseur):
  cursor.execute("SELECT ID,nom,points FROM dresseurs ORDER BY points DESC LIMIT 10")
  record=[list(i) for i in cursor.fetchall()]
  r=0
  for dresseurs in [i[0] for i in record]:
    cursor.execute(f"SELECT COUNT(*) FROM mots WHERE dresseur='{dresseurs}'")
    record[r].append(cursor.fetchall()[0][0])
    r+=1
  #stats = nom,points,nombre de mots, position dans le classement
  cursor.execute(f"SELECT nom,points FROM dresseurs WHERE nom='{dresseur}'")
  stats=list(cursor.fetchall()[0])
  cursor.execute(f"SELECT COUNT(*) FROM mots WHERE dresseur=(SELECT id FROM dresseurs WHERE nom='{dresseur}')")
  stats.append(cursor.fetchall()[0][0])
  stats.append(pos_classement(dresseur))
  return stats,record

#___________________________________________

def cheatpoints(dresseur):
  cursor.execute(f"UPDATE dresseurs SET points=points+50 WHERE nom='{dresseur}'")
  sqliteConnection.commit()
  return("ggwp")

#___________________________________________

def ajouterscore(auteur, phrase):
  for mot in simp(phrase).split(" "):
    cursor.execute(f"UPDATE dresseurs SET points=points+(SELECT rarete FROM mots WHERE nom='{mot}') WHERE id=(SELECT dresseur FROM mots WHERE nom='{mot}') AND nom!='{auteur}'")
  sqliteConnection.commit()
  return

def close_db(): #en cas de problème
  sqliteConnection.close()
