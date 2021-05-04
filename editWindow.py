import tkinter as tk
import tkinter.ttk as ttk
import DatabaseHandler as database

class editWindow(tk.Toplevel):
    def __init__(self, parent, Rid, database, *args, **kwargs):
        """
        Input: self - The object containing the frame being called
        Input: parent - The parent window
        Input: Rid - The Rid of the recipe to be edited 
        Returns: None
        Purpose: Creates an opens the editing window with fields populated as approriate 
        """
        tk.Toplevel.__init__(self, parent, *args, **kwargs) 
        
        self.database = database
        
        
        self.recipe = database.getRecipe(Rid)
        self.title("Edit - " + self.recipe["name"])

       
        
        ### Make the options menu
        self.fr_options = ttk.Frame(self, relief = "raised", padding=1)
        self.fr_options.grid(row = 0, column = 0, sticky = "NESW")
        self.rowconfigure(0, weight = 1)
        self.lbl_addIngredient = ttk.Label(self.fr_options, text = "Add Ingredients:", font = ("Times", "12"))
        self.lbl_addIngredient.pack()

        self.ent_category = self.makeLabelEntry(self.fr_options, "Category: ", {}, None, frameside = tk.TOP, width = 15)
        self.ent_ingName = self.makeLabelEntry(self.fr_options, "Name: ", {}, None, frameside = tk.TOP, width = 15)

        self.btn_add = ttk.Button(self.fr_options, text= "Add", command = self.add)
        self.btn_add.pack()

        

        self.btn_close = ttk.Button(self.fr_options, text= "Close", command = self.destroy)
        self.btn_close.pack(side= tk.BOTTOM, anchor = "s", pady = (5, 5))

        self.btn_save = ttk.Button(self.fr_options, text= "Save", command = self.save)
        self.btn_save.pack(side= tk.BOTTOM, anchor = "s", pady = (40, 0))
        ### Done making options menu

        keys = ["name", "start","end", "abv", "OG", "FG", "volume", "instructions"]
        tags = ["", "Start date: ","End date: ", "abv: ", "OG: ", "FG: ", "Batch size: ", "Instructions: "]
        self.entrys = {}

       
        self.fr_recipe = ttk.Frame(self)
        
        self.fr_recipe.grid(row = 0, column = 1, sticky = "EW")
        self.columnconfigure(1, weight =1)
        
        ttk.Label(self.fr_recipe, text = self.recipe["name"] + " V" +str(self.recipe["version"]), font = ("times", "20", "bold")).pack()

        keys =  ["start", "end"]
        tags = ["Start date: ", "End date: "]
        self.makeLabelEntrys(self.fr_recipe, self.recipe, keys, tags)

        keys =  ["abv", "OG", "FG", "volume"]
        tags = ["abv: ", "OG: ", "FG: ", "Volume: "]
        self.makeLabelEntrys(self.fr_recipe, self.recipe, keys, tags)

        self.ingredientList = database.getIngredients(Rid)
        self.makeIngredientList(self.ingredientList)

        fr_instuctions = ttk.LabelFrame(self.fr_recipe, text = "Instructions")
        fr_instuctions.pack(side = tk.TOP, expand = "TRUE", fill = "both")
        self.txt_instructions = tk.Text(fr_instuctions, wrap = tk.WORD)
        self.txt_instructions.insert(tk.END, self.recipe["instructions"])
        self.txt_instructions.pack(expand = "true", fill = "both")

    def makeLabelEntrys(self, parent, recDict, keys, tags,  width = 10, labelside= tk.LEFT):
        """
        Input: self - The object containing the frame being called
        Input: parent - The parent window
        Input: recDict - dictionary containing the values to be put into the entrys
        Input: keys - List of string keys for the dictinary values that need to be shown
        Input: tags - List of strings that are formatted for display
        Input: width - The size of box to make for each entry
        Input: labelside - The side of the entry box where the label should be placed
        Returns: None
        Purpose: Loops through the provided list and hands the name and value to makeLabelEntry to generate the label-entry composite widget. The entry frames are saved in 
        self.entrys.update for simple access later while reading the data.
        """
        fr_section = ttk.Frame(parent)
        for index, key in enumerate(keys):
            cur_entry = self.makeLabelEntry(fr_section, tags[index], recDict, key, width= width, labelside = labelside)
            self.entrys.update({key:cur_entry})
        fr_section.pack(pady = 5, padx = 5)

    def makeLabelEntry(self, parent, name, recDict, key, width = 10, labelside = tk.LEFT, frameside= tk.LEFT):
        """
        Input: self - The object containing the frame being called
        Input: parent - The parent window
        Input: recDict - dictionary containing the values to be put into the entrys
        Input: key - String, the key for the value to be placed put into the display box
        Input: tags - String that is formatted for display
        Input: width - The width of the entry box
        Input: labelside - The side of the entry box where the label should be placed
        Returns: cur_entry - The newly created Entry widget
        Purpose: Creates a frame holding a label widget with the correct String and an entry field prepopulated as appropriate
        """
        cur_frame = ttk.Frame(parent, padding = 5)
        cur_frame.pack(side = frameside)
        cur_label = ttk.Label(cur_frame, text = name)
        cur_label.pack(side = labelside)
        cur_entry = ttk.Entry(cur_frame, width= width)
        try:
            if recDict[key]:
                cur_entry.insert(1, str(recDict[key]))
        except KeyError:
            pass
        cur_entry.pack()
        return cur_entry
     
    def makeIngredientList(self, ingredients):
        """
        Input: self - The object containing the frame being called
        Input: ingredients - List of dictionarys containing the ingredient to be written to the GUI
        Returns: Nothing
        Purpose: Loops through all the ingredients and calls addIngredient to create composite widgets for each ingredient
        """
        self.IngredientFrameList = []
        self.fr_ingredients = ttk.Frame(self.fr_recipe)
        self.fr_ingredients.pack(expand = "TRUE", fill = "both")
        for ingredient in ingredients:
            newFramDict = self.addIngredient(self.fr_ingredients, ingredient)
            self.IngredientFrameList.append(newFramDict)


    def addIngredient(self, parent, ingredient):
        """
        Input: self - The object containing the frame being called, parent - the parent window of this frame
        Input: parent - The parent window
        Input: ingredient - A dictionary containing the ingredient to be written to the GUI
        Returns: currentFrameDict - A dictionary containing the widgets entry widgets for each category of the ingredient
        Purpose: Creates a frame holding a label and entry widgets as needed with the correct strings prepopulated as appropriate.
        """
        currentFrameDict = {}
        fr_curIngredient = ttk.Frame(self.fr_ingredients)
        fr_curIngredient.pack()
        lb_category = ttk.Label(fr_curIngredient, text = "{}: {}".format(ingredient["category"].capitalize(), ingredient["name"]), width = 25)
        lb_category.grid(row = 1, column = 0, padx = 15, sticky = "E")

        alias = ["Amount", "Unit", "Addition time"]
        for index, key in enumerate(["amount", "unit", "additionTime"]):
            lb_cur = ttk.Label(fr_curIngredient, text= alias[index] + ": ")
            lb_cur.grid(row = 1, column = 2*index+1, padx = 10)
            ent_cur = ttk.Entry(fr_curIngredient, width = 10)
            if(ingredient[key]):
                ent_cur.insert(1, ingredient[key])
            ent_cur.grid(row = 1, column = 2*index +2 )
            currentFrameDict.update({key:ent_cur})
        fr_curIngredient.columnconfigure(0, weight = 1, minsize = 20)
        
        currentFrameDict.update({"frame":fr_curIngredient})

        bt_delete = ttk.Button(fr_curIngredient, text= "Del", width = 4, command = self.deleteIngredient(ingredient, currentFrameDict))
        bt_delete.grid(row = 1, column = 2*index+3)
        
        return currentFrameDict

    def deleteIngredient(self, ingredient, frameDict):
        """
        Input: self - The object containing the frame being called
        Input: ingredient - The ingredient dictionary for the ingredient to be deleted
        Input: frameDict - The frame dictionary for the frame to be deleted
        Returns: delete - Function, the function to be executed upon the delete button being pressed
        Purpose: Permits the creation of frame specifc deletion functions in a procedural manner
        """
        def delete():
            state = ingredient["state"]
            if (state == "add"):
                ingredient.clear()
            else:
                ingredient["state"] = "delete"
            frameDict["frame"].destroy()
        return delete

    def add(self):
        """
        Input: self - The object containing the frame being called
        Returns: Nothing
        Purpose: Reads and clears the two entry box for adding an ingredient to the list. After reading the ingredient name and label it adds it to the list.
        """
        name = self.ent_ingName.get()
        category = self.ent_category.get()
        if name and category:
            newIngredient = {"name":name, "category":category, "state":"add", "amount":0, "unit":"", "additionTime":""}
            self.ingredientList.append(newIngredient)
            newFrameDict = self.addIngredient(self.fr_ingredients, newIngredient)
            self.IngredientFrameList.append(newFrameDict)

    def save(self):
        """
        Input: self - The object containing the frame being called
        Returns: Nothing
        Purpose: Reads the data from all of the entry feilds and updates the respective lsits before calling setorUpdateRecipe() to insert the new information into the database.
        """
        for key in ["start","end", "abv", "OG", "FG", "volume"]:
            self.recipe[key] = self.entrys[key].get()
        self.recipe["instructions"] = self.txt_instructions.get("1.0", tk.END)

        for index, ingredient in enumerate(self.ingredientList):
            if not ingredient:
                self.ingredientList.pop(index)
                self.IngredientFrameList.pop(index)
                continue
            if ingredient["state"] == "add" or ingredient["state"] == "current":
                for key in ["unit", "amount"]:
                    ingredient[key] = self.IngredientFrameList[index][key].get()
        
        self.database.setorUpdateRecipe(self.recipe, self.ingredientList)    


        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ParentWindow")
    test = editWindow(root, 1, database.Database(r".\Brewing.db"))
    root.mainloop()