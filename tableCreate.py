#import requests

#from init import *

import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pokedex", port=8889)
cursor = conn.cursor(buffered=True)


def initTables(cursor):
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon(
                id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                ref VARCHAR(11),
                nom VARCHAR(255),
                total VARCHAR(255),  
                hp VARCHAR(255), 
                attack VARCHAR(255), 
                defense VARCHAR(255), 
                sp_atk VARCHAR(255), 
                sp_def VARCHAR(255), 
                speed VARCHAR(255)
                );
            """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS type
            (
               id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
               nom VARCHAR(255)
            );
            """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS transformation (
                id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                nom_transformation VARCHAR(255)
            );
            """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon_types (
                id int(11) PRIMARY KEY AUTO_INCREMENT, 
                pokemon_id int NOT NULL, 
                type_id int NOT NULL, 
                FOREIGN KEY(pokemon_id) REFERENCES pokemon(id), 
                FOREIGN KEY(type_id) REFERENCES type(id)
            );
            """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon_transformations (
                id int(11) PRIMARY KEY AUTO_INCREMENT, 
                pokemon_id int NOT NULL, 
                transformation_id int NOT NULL, 
                FOREIGN KEY(pokemon_id) REFERENCES pokemon(id), 
                FOREIGN KEY(transformation_id) REFERENCES transformation(id)
            );
            """)
    cursor.execute("""SET FOREIGN_KEY_CHECKS=0""")
    cursor.execute("""TRUNCATE TABLE type""")
    cursor.execute("""TRUNCATE TABLE pokemon""")
    cursor.execute("""TRUNCATE TABLE transformation""")
    cursor.execute("""TRUNCATE TABLE pokemon_types""")
    cursor.execute("""TRUNCATE TABLE pokemon_transformations""")
    cursor.execute("""SET FOREIGN_KEY_CHECKS=1""")
    return cursor




cursor = initTables(cursor)

cursor.close()
conn.commit()
conn.close()