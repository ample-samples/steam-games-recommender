from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkComboBox, CTkOptionMenu

class Top_Bar(CTkFrame):
    def __init__(self, parent, label_text, button_text):
        super().__init__(master = parent)
        
        # set up grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,3), weight=0)
        self.grid_columnconfigure(2, weight=1)

        CTkEntry(self, placeholder_text="Enter library path").grid(row=0, column=0, pady=(10,0), padx=(5, 0))

        CTkButton(self, text="Save").grid(row=0, column=1, pady=(10,0))

        CTkLabel(self, text="").grid(row=0, column=2, pady=(10,0))

        sort_dropdown = CTkOptionMenu(self, values=["Sort by:", "Potential playtime", "Highest rated"])
        sort_dropdown.set("Sort by:")
        sort_dropdown.grid(row=0, column=3, pady=(10,0), padx=(0, 5))
