import requests

from bs4 import BeautifulSoup

import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
cursor = conn.cursor(buffered=True)

# connexion et récupération des données / parse du site

#response = requests.get("https://pokemondb.net/pokedex/all")
#html = str(response.content)

fichier = open("data_pokemon.html","r")
html = fichier.read()
fichier.close()

soup = BeautifulSoup(html, "html.parser")

tab = soup.find(id="pokedex")

for link in tab.find_all("tr"):
    tt = []
    x = 0
    type_ids = []
    for l in link.find_all("td"):


        if x == 1:
            if l.find_all("a"):
                nom = l.find_all("a")
                tt.append(nom[0].text)
            else:
                tt.append("")


        if x == 2:
            for type_poke in l.find_all("a"):

                nom_type = type_poke.text

                cursor.execute("SELECT id FROM type WHERE nom LIKE '"+nom_type+"%' ;")
                test_type = cursor.fetchone()

                if test_type == None:
                    cursor.execute("INSERT INTO type VALUES (0, '"+nom_type+"');")

                    type_ids.append(cursor.lastrowid)


        if x == 0 or x > 2:
            tt.append(l.text)

        x = x+1



    if len(tt) > 0 and tt[1] != "":
        cursor.execute("""INSERT INTO pokemon (ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", tt)
        pokemon_id = cursor.lastrowid
        for type_id in type_ids:
            print(type_id)
            cursor.execute("INSERT INTO pokemon_types VALUES (0, "+str(pokemon_id)+", "+str(type_id)+");")

cursor.close()
conn.commit()
conn.close()