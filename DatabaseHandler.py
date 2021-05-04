import sqlite3
from sqlite3 import Error

class Database():
    def __init__(self, dbpath):
        """
        Input: self - The instance of the object containing the function being called
        Input: dbpath - string containing the path of the database to be opened
        Returns:None
        Purpose: When called it opens a connection to the database and stores the connection as a self variable
        """
        self.conn = self.__create_connection(dbpath)
        if self.conn:
            self.db = self.conn.cursor()
            self.conn.commit()

    def getTitles(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: list of tuples - A list of tuples which contain the name and Rid for every recipe as a pair
        Purpose: When it returns a list of titles for convenient insertion into a GUI element. The titles are paired with the Rid for convenient reference 
        to the associated recipe downstream
        """
        return self.db.execute("select Rid, name FROM recipes").fetchall()
    
    def getRecipe(self, Rid):
        """
        Input: self - The instance of the object containing the function being called
        Input: Rid - integer, The Rid of the recipe that has been requested.
        Returns: dictRecipe - A single dict containing the traits of a recipe and the associated value as a key-value pair, Ex "name":"ginger beer"
        Purpose: Returns the contents of the recipe indicated by the Rid in dictionary format.
        Dict keys: ["name":"Name of the recipe", "version":"The version number", "start":"Start date","end":"Ending date", "abv":"alcohol by volume", "OG":"Original gravity", "FG":"Final gravity", "volume":"Volume of the batch", "instructions":"Brewing instructions"]
        """
        recipe = self.db.execute("select name, version, start, end, abv, OG, FG, volume, instructions FROM recipes where Rid = ?", [Rid]).fetchall()[0]
        tags = ["name", "version", "start","end", "abv", "OG", "FG", "volume", "instructions"]
        dictRecipe = {}
        [dictRecipe.update({tags[index]:stat}) for index, stat in enumerate(recipe)]
        return dictRecipe

    def getIngredients(self, Rid):
        """
        Input: self - The instance of the object containing the function being called
        Input: Rid - integer, The Rid of the recipe that has been requested.
        Returns:list - A list of dicts containing the traits as keys with the assocaited value ina key value pair. Ex: "category":"yeast"
        Purpose: Returns the ingredients of the recipe indicated by the Rid in dictionary format.
        Dict keys: ["category":"The broad category the ingredient fits into", "name":"The name of the ingredient", "amount":"The quantity of the ingredients", "unit":"The associated unit for the quantity", "additionTime":"When in the proccess this ingredient was added", "state":"Used too indicate if the ingredient should be deleted, added, or merely updated when setorUpdateRecipe is called"]
        """
        keys = ["category", "name", "amount", "unit", "additionTime"]
        ingredientList = self.db.execute("SELECT  ingredients.category, ingredients.name, recipeIngredients.amount, recipeIngredients.unit, recipeIngredients.additionTime FROM recipeIngredients INNER JOIN ingredients ON recipeIngredients.ingid= ingredients.ingid WHERE Rid = ?", [Rid]).fetchall()
        ingredientld = []
        for item in ingredientList:
            cur = {}
            for index, key in enumerate(keys):
                cur.update({key:item[index]})
            cur.update({"state":"current"})
            ingredientld.append(cur)
        return ingredientld
    
    def setorUpdateRecipe(self, recipe, ingredients):
        """
        Input: self - The instance of the object containing the function being called
        Input: recipe - dictionary of key value pairs containg the traits and associated value to be updated
        Input: ingredients - a list of dictionaries with each entry being a separate ingredient. Whether an ingredient is updated, added or removed depends on if the value mapped to "state" is current, add or delete respectively. 
        Returns: Rid- The Rid for the recipe just set or updated
        Purpose: When called and passed a recipe + ingredient list it will either update an existing recipe if an entry is found with an identical name AND version, or update the existing recipe.
        
        """
        Rid = self.db.execute("Select Rid FROM recipes WHERE name = ? AND version = ?", (recipe["name"], recipe["version"])).fetchone()

        if Rid:
            Rid = Rid[0]
        else:
            recipe["version"] = self.nextversion(recipe["name"])
            Rid = self.__nextId()
            self.db.execute("INSERT INTO recipes (Rid) VALUES (?)", [Rid])


        for key in recipe:
            self.db.execute(r"UPDATE recipes SET {}=? WHERE Rid = ?".format(key), [recipe[key], Rid])

    
        for item in ingredients:
            #find the ingidid of the named ingredient
            ingid = self.db.execute("SELECT ingid FROM ingredients where lower(name) == ?", [item["name"].lower()]).fetchone()
            if not bool(ingid):
                self.db.execute("INSERT INTO ingredients (name, category) VALUES (?, ?)", (item["name"],item["category"]))
                ingid = self.db.execute("SELECT ingid FROM ingredients where lower(name) == ?", [item["name"].lower()]).fetchone()
           
            if(item["state"] == "current"):
                self.db.execute("UPDATE recipeIngredients SET amount = ?, unit =?, additionTime = ? WHERE Rid = ? AND ingid = ?", [item["amount"], item["unit"], item["additionTime"], Rid, ingid[0]])
            elif (item["state"] == "delete"):
                self.db.execute("DELETE FROM recipeIngredients WHERE Rid = ? AND ingid = ?", [Rid, ingid])
            elif (item["state"] == "add"):
                #print([Rid, ingid, item["amount"], item["unit"]])
                self.db.execute("INSERT INTO recipeIngredients (Rid, ingid, amount, unit, additionTime) VALUES (?,?,?,?,?)", [Rid, ingid[0], item["amount"], item["unit"], item["additionTime"]])
        self.conn.commit()

        return Rid

    def deleteRecipe(self, Rid):
        """
        Input: self - The instance of the object containing the function being called
        Input: Rid- The Rid for the recipe to be deleted from the database
        Returns: Nothing
        Purpose: When called and handed an Rid this function will remove the entry from the database
        
        """
        self.db.execute("DELETE FROM recipes WHERE Rid = ?", str(Rid))
        self.db.execute("DELETE FROM recipeIngredients WHERE Rid = ?", str(Rid))

    def __nextId(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: newid - integer value of the next available Rid
        Purpose: When called this function will return the next available sequential Rid
        
        """
        maxid = self.db.execute("SELECT max(Rid) FROM recipes").fetchone()[0]
        if not maxid:
            newid = 1
        else:
            newid = maxid + 1
        return newid

    def nextversion(self, name):
        """
        Input: self - The instance of the object containing the function being called
        Input: name- String, The name of the recipe for which we want to find the next open version number
        Returns: nextversion - integer, the next available version number
        Purpose: When called this function will return the next available sequential version number
        """
        maxversion = self.db.execute("SELECT max(version) FROM recipes WHERE name = ?", [name]).fetchone()[0]
        if not maxversion:
            nextversion = 1
        else:
            nextversion = maxversion + 1
        
        return nextversion
    
    def __create_connection(self, db_path):
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

    def newRecipe(self, name):
        """
        Input: self - The instance of the object containing the function being called
        Input: name- String, The name of the recipe we want to create
        Returns: Rid - Integer, the Rid for the newly created recipe
        Purpose: When called this function will create a new recipe entry with the given name and hadn back the associated Rid
        """
        recipe = {"name":name,"version":-1, "start":"","volume":"", "instructions":""}
        return self.setorUpdateRecipe(recipe, [])



if __name__ == '__main__':
    db = Database(r".\Brewing.db")
    print("init", db.getTitles())
    print("init", db.getRecipe(0))
    print("init", db.getIngredients(0))