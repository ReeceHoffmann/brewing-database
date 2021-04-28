class Database():
    def __init__(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns:None
        Purpose: When called it creates the dict containing the temporary data to be used
        """
        self.recipe = [{"Title":"Ginger beer", "yeast":"EC-118", "sugar":"Organic cane sugar 500g", "brewTime":"2 weeks", "instructions":"This is a longer string that can be used to check formatting of longer strings"},
            {"Title":"Amber ale","yeast":"s0-5", "sugar":"DME", "brewTime":"2 weeks", "instructions":"This is a longer string that can be used to check formatting of longer strings"}]
    def getTitles(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns:list - A list of strings containg the titles of every recipe in the database
        Purpose: When it returns a list of titles for convenient insertion into a GUI element
        """
        return [entry["Title"] for entry in self.recipe]
    def getRecipe(self, index):
        """
        Input: self - The instance of the object containing the function being called
        Returns:list - A list of dicts containing the the name of an element and the element as a key value pair
        Purpose: When called it returns the elements of the recipe for insertion into a GUI element
        """
        if index < len(self.recipe):
            return self.recipe[index]
        else:
            return []
    def setRecipe(self, recipe):
        """
        #TODO - All parameters indicated are intended if not implemented
        Input: self - The instance of the object containing the function being called, recipie, 
        Returns: Nothing
        Purpose: When called it returns the elements of the recipe for insertion into a GUI element
        """
        pass