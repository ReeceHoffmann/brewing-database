
"""
This script calls the database handler to make a new copy of the example recipe 

"""
import DatabaseHandler as database

if __name__ == '__main__':
    db = database.Database(r".\Brewing.db")
    ingredients = [{"name":"DAP", "category":"yeast nutrient", "amount":"4", "unit":"g", "additionTime":"", "state":"add"},\
                   {"name":"Yeast Hulls", "category":"yeast nutrient", "amount":"4", "unit":"g", "additionTime":"", "state":"add"},\
                   {"name":"EC-118", "category":"yeast", "amount":"1", "unit":"pack", "additionTime":"", "state":"add"},\
                   {"name":"Organic cane sugar", "category":"sugar", "amount":"500","additionTime":"", "unit":"g","state":"add"},\
                   {"name":"Lime", "category":"fruit","amount":"1","unit":"g","additionTime":"","state":"add"}] 
    recipe = {"name":"Ginger Beer","version":-1, "start":"2021-04-28", "end":"2021-05-21", "abv":"5.0", "volume":"1", "instructions":"Bring the water to a boil, wrap the grains in cheesecloth and place them in the boiling water to steep for 15 minutes. After steeping add lime juice and allow the mixture to cool to ~20C. Transfer to your fermentation vessel of choice and pitch the yeast"}
    db.setorUpdateRecipe(recipe, ingredients)