import sqlite3
from sqlite3 import Error

"""
After user confirmation this script will delete and reinitilize an empty database for use with BrewingDatabase.py.
This script must be run before BrewingDatabase.py

"""
def make_db(db):
        """
        Input: db - ssqlite3 cursor object for the database to be reset
        Returns: Nothing
        Purpose:When called it drops
         """
        #Delete the current database
        ###################################
        try:
            db.execute(r"drop table recipes")
            db.execute(r"drop table recipeIngredients")
            db.execute(r"drop table ingredients")
        except:
            print("delete failed")
        ###################################

        sql_create_recipe_table = """ CREATE TABLE IF NOT EXISTS recipes (
                                            Rid integer NOT NULL PRIMARY KEY,
                                            name text,
                                            version integer,
                                            start TEXT,
                                            end TEXT,
                                            volume INT,
                                            instructions text,
                                            abv float(3, 2),
                                            OG INT(4),
                                            FG INT(4),
                                            UNIQUE (name, version)
                                        ); """

        sql_create_ingredient_table = """ CREATE TABLE IF NOT EXISTS ingredients (
                                                        ingid integer NOT NULL PRIMARY KEY,
                                                        name text NOT NULL,
                                                        category text
                                                    ); """

        sql_create_ingredients_in_recipe_table = """ CREATE TABLE IF NOT EXISTS recipeIngredients (
                                                        inid integer NOT NULL PRIMARY KEY,
                                                        Rid integer,
                                                        ingid integer, 
                                                        amount FLOAT,
                                                        unit TEXT,
                                                        additionTime TEXT,
                                                        FOREIGN KEY(Rid) REFERENCES recipes(Rid),
                                                        FOREIGN KEY(ingid) REFERENCES ingredients(ingid)
                                                    ); """      
        
        db.execute(sql_create_recipe_table)
        db.execute(sql_create_ingredient_table)
        db.execute(sql_create_ingredients_in_recipe_table)



def create_connection(db_path):
    """
        Input: db_path - string containing a path to the database
        Returns: conn- Connection to the database specifed by the path
        Purpose: When called it creates a connection to the database specifed in db_path
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)
    return conn


if __name__ == '__main__':
    confirmation = input("This program will wipe the database, are you sure? (Y/N)")

    if not confirmation == "Y":
        print("Wipe canceled, terminating")
        quit()
    print("Reinitilizing database")
    
    conn = create_connection(r".\Brewing.db")
    if conn:
        db = conn.cursor()
        make_db(db)
        conn.commit()
    print("Database reset!")