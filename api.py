"""A basic (single function) API written using hug"""
import hug
import mysql.connector



@hug.get('/pokemon')
def pokemon_one(id):
    """afficher un pokemon"""
    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM pokemon WHERE id = %s""", (id, ))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return '{0}'.format(rows[0])

@hug.get('/pokemon/all')
def pokemon_all():
    """afficher l'ensemble des pokemons"""
    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM pokemon """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return '{0}'.format(rows)

@hug.post('/pokemon/add')
def pokemon_add(ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed):
    """Ajouter un pokemon"""
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
        cursor = conn.cursor()
        req = (ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed)
        cursor.execute("""INSERT INTO pokemon (ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", req)
        conn.commit()
        cursor.execute("""SELECT * FROM pokemon WHERE nom =%s""", (nom, ))
        pok = cursor.fetchone()
        cursor.close()
        conn.close()
        chaine = "vous avez bien ajouté le pokemon '"+str(pok[2])+"'"
    except mysql.connector.errors.IntegrityError:
        chaine = "Pokemon deja existant"
    finally:
        print()
    return str(chaine)

@hug.put('/pokemon/update')
def pokemon_update(ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed):
    """Mettre à jour un pokemon"""
    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
    cursor = conn.cursor()
    req = (ref, nom, total, hp, attack, defense, sp_atk, sp_def, speed, nom)
    cursor.execute("""UPDATE pokemon SET ref=%s, nom=%s, total=%s, hp=%s, attack=%s, defense=%s, sp_atk=%s, sp_def=%s, speed=%s WHERE nom=%s""", req)
    conn.commit()
    cursor.execute("""SELECT * FROM pokemon WHERE nom=%s""", (nom, ))
    f = cursor.fetchone()
    cursor.close()
    conn.close()
    return "Vous avez bien modifié le pokemon'"+str(f[2])+"'"

@hug.delete('/pokemon/delete')
def pokemon_delete(nom):
    """Supprimer un pokemon"""
    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM pokemon WHERE nom =%s""", (nom, ))
    conn.commit()
    cursor.execute("""SELECT count(id) FROM pokemon where nom=%s""", (nom, ))
    valeur = cursor.fetchone()
    if int(valeur[0]) == 0:
        chaine = "element supprime"
    else:
        chaine = "element non supprimé "

    cursor.close()
    conn.close()
    return str(chaine)