import tkinter as tk
import tkinter.ttk as ttk
import DatabaseHandler as Database
import editWindow



class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Input: self - The object containing the frame being called, parent - the parent window of this frame
        Output: None
        Purpose: Creates the main window
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.database = Database.Database(r".\Brewing.db")
        parent.title("BrewingDB")

        #handles making the recipe selection
        self.lb_selection = tk.Listbox(self, selectmode = "single")
        self.__refreshList()
        self.lb_selection.grid(row = 1, column = 0, sticky = "NESW")
        self.lb_selection.bind('<<ListboxSelect>>', self.__changeRecipe)

        #handles creation of recipe display box
        self.txt_recipe = tk.Text(self, height = 20, width = 50, wrap = tk.WORD)
        self.txt_recipe.grid(row = 1, column = 1,sticky = "NESW")
        self.txt_recipe.config(state="disabled")
        
        #configures the display box to be resizable
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(1, weight = 1)

        #creates a frame for holding the options button
        self.fr_options_bar = tk.Frame(self)
        self.fr_options_bar.grid(row = 0, column =0, columnspan = 2, sticky = "NESW")
        #Creates a copy button
        self.btn_copy = ttk.Button(master=self.fr_options_bar, text="Copy", command = self.__copy)
        self.btn_copy.pack(side = "left")
        #Creates an edit button
        self.btn_edit = ttk.Button(master=self.fr_options_bar, text="Edit", command = self.__edit)
        self.btn_edit.pack(side = "left")
        #Creates a delete button
        self.btn_delete = ttk.Button(master=self.fr_options_bar, text="Delete", command = self.__delete)
        self.btn_delete.pack(side = "left")

    def __refreshList(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns:None
        Purpose: When called it requests the titles of all recipes from the database and displays them in lb_selection (selection bar)
        """
        self.lb_selection.delete(0, tk.END)
        self.titleList = self.database.getTitles()
        [self.lb_selection.insert(tk.END, item[1]) for item in self.titleList]
        self.lb_selection.insert(tk.END, "New...")
    
    def __changeRecipe(self, event):
        """
        Input: self - The instance of the object containing the function being called
        Input: event - Virtual event causing __changeRecipe to be called
        Returns: None
        Purpose: When called it changes the recipe in txt_recipe to display the recipe currently selected in lb_selection.
        """
        selectionIndex = self.lb_selection.curselection()[0]
        if selectionIndex == (self.lb_selection.size()-1):
            self.__newRecipe()
            #self.editWindow = editWindow.editWindow(self, -1, self.database)
            return
        
        tags = ["","V ", "Start date: ","End date: ", "abv: ", "OG: ", "FG: ", "Batch size: ", "Instructions: "]
        recipe = self.database.getRecipe(self.titleList[selectionIndex][0])
        ingredients = self.database.getIngredients(self.titleList[selectionIndex][0])
        
        self.txt_recipe.config(state="normal")
        
        self.txt_recipe.delete("1.0", tk.END)
        [self.txt_recipe.insert(tk.END, ("{}{}\n".format(tags[index], recipe[key])) ) for index, key in enumerate(recipe) if recipe[key]]
        
        self.txt_recipe.insert(tk.END, "\n\nIngredients: \n" )
        for ingredient in ingredients:
            self.txt_recipe.insert(tk.END, "{}: {} {}{}\n".format(ingredient["category"].capitalize(), ingredient["name"], ingredient["amount"], ingredient["unit"]))

        self.txt_recipe.config(state="disabled")

    def __newRecipe(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: When called this function opens a dialogue window to get the name of the new recipe. If the Confirm button is pressed the internal function "confirm" closes the 
        dialogue window and send s requests to the database handler to create a record with the given recipe. This recipe is then opened in an edit window.
        """
        def confirm(name):
            Rid = self.database.newRecipe(name)
            self.editWindow = editWindow.editWindow(self, Rid, self.database)
            dia_name.destroy()
            self.__refreshList()
        
        dia_name = tk.Toplevel(self)
        
        fr_entry = tk.Frame(dia_name)
        la_dia = ttk.Label(fr_entry, text = "Enter new recipe name: ", padding = (0,10))
        ent_dia = ttk.Entry(fr_entry)
        la_dia.pack(side = tk.LEFT)
        ent_dia.pack(side = tk.LEFT)
        fr_entry.grid(row = 0, column = 0, columnspan = 2, padx=(10,10))

        
        btn_confirm = tk.Button(dia_name, text= "Confirm", command= lambda: confirm(ent_dia.get()))
        btn_confirm.grid(row =1, column = 0)
        btn_close = tk.Button(dia_name, text= "Close", command= dia_name.destroy)
        btn_close.grid(row =1, column = 1)

    def __edit(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: Get the currently selected index of lb_selection and translates that into an RID before calling a new instance of editwindow
        """
        selectionIndex = self.lb_selection.curselection()[0]
        if selectionIndex == (self.lb_selection.size()-1):
            return
        print(selectionIndex)
        self.editWindow = editWindow.editWindow(self, self.titleList[selectionIndex][0], self.database)
    
    def __copy(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: Duplicates the recipe currently selected in lb_selection 
        """
        selectionIndex = self.lb_selection.curselection()[0]
        
        if selectionIndex == (self.lb_selection.size()-1):
            return
        
        recipe = self.database.getRecipe(self.titleList[selectionIndex][0])
        recipe.update({"version":-1}) #set version to an impossible version number so there is a guarantee that it doesn't exactly match an existing records
        
        ingredients = self.database.getIngredients(self.titleList[selectionIndex][0])
        [ing.update({"state":"add"}) for ing in ingredients]
        
        self.database.setorUpdateRecipe(recipe,ingredients)
        self.__refreshList()
    
    def __delete(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: Deletes the recipe currently selected in lb_selection 
        """
        selectionIndex = self.lb_selection.curselection()[0]
        
        if selectionIndex == (self.lb_selection.size()-1):
            return
        print(self.titleList[selectionIndex][0])
        self.database.deleteRecipe(self.titleList[selectionIndex][0])
        self.__refreshList()




if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()