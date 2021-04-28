import tkinter as tk
import tempDatabaseHandler as Database



class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Input: self - The object containing the frame being called, parent - the parent window of this frame
        Output: None
        Purpose: Creates the window being used
        """
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.database = Database.Database()
        parent.title("Draft Recipe Selection window")

        #handles making the recipe selection
        self.lb_selection = tk.Listbox(self, selectmode = "single")
        self.__refreshList()
        self.lb_selection.grid(row = 1, column = 0, sticky = "NESW")
        self.lb_selection.bind('<<ListboxSelect>>', self.__changeRecipe)

        #handles creation of recipe display box
        self.txt_recipe = tk.Text(self, height = 20, width = 50)
        self.txt_recipe.grid(row = 1, column = 1,sticky = "NESW")
        self.txt_recipe.config(state="disabled")
        #configures the display box to be resizable
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(1, weight = 1)

        #creates a frame for holding the options button
        self.fr_options_bar = tk.Frame(self)
        self.fr_options_bar.grid(row = 0, column =0, columnspan = 2, sticky = "NESW")
        #Creates a copy button
        self.btn_copy = tk.Button(master=self.fr_options_bar, text="copy", command = self.__copy)
        self.btn_copy.pack(side = "left")
        #Creates an edit button
        self.btn_edit = tk.Button(master=self.fr_options_bar, text="edit", command = self.__edit)
        self.btn_edit.pack(side = "left")
        #Creates a delete button
        self.btn_delete = tk.Button(master=self.fr_options_bar, text="delete", command = self.__delete)
        self.btn_delete.pack(side = "left")

    def __refreshList(self):
        """
        Input: self - The instance of the object containing the function being called
        Returns:None
        Purpose: When called it requests the titles of all recipes from the database and displays them in lb_selection (selection bar)
        """
        [self.lb_selection.insert(tk.END, item) for item in self.database.getTitles()]
        self.lb_selection.insert(tk.END, "New...")
    
    def __changeRecipe(self, event):
        """
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: When called it displays the entry for the recipe currently selected in lb_selection to txt_recipe 
        """
        selectionIndex = self.lb_selection.curselection()[0]
        if selectionIndex == (self.lb_selection.size()-1):
            print("Open new recipe window")

        recipe = self.database.getRecipe(selectionIndex)
        
        self.txt_recipe.config(state="normal")
        self.txt_recipe.delete("1.0", tk.END)
        [self.txt_recipe.insert(tk.END, (key + ": " + recipe[key] + "\n") ) for key in recipe]
        self.txt_recipe.config(state="disabled")

    def __edit(self):
        """
        TODO - All parameters indicated are intended if not implemented
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: To open a new window for editing the recipe currently selected in lb_selection 
        """
        pass
    
    def __copy(self):
        """
        TODO - All parameters indicated are intended if not implemented
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: Duplicates the recipe currently selected in lb_selection 
        """
        pass
    
    def __delete(self):
        """
        TODO - All parameters indicated are intended if not implemented
        Input: self - The instance of the object containing the function being called
        Returns: None
        Purpose: Deletes the recipe currently selected in lb_selection 
        """
        pass

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()