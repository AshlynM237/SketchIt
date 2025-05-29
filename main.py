import customtkinter as ctk

BUTTON_PADY=20
BUTTON_PADX=10
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SketchIt")
        self.geometry("600x400")

        # Container to hold all pages
        # CTkFrame is a customtkinter frame that can be used to create a container for other widgets
        self.container = ctk.CTkFrame(self)
        #fill="both": allows the container to fill the available space in both directions
        #expand=True: allows the container to expand to fill the available space
        # self.container.pack(fill="both", expand=True)
        self.container.grid(row=0,column=0)
        ctk.set_default_color_theme("green")
        
        self.build_frames()
        self.show_frame("MainMenu")
        
    def build_frames(self):
        #destroy old frames if there are any
        for frame in getattr(self,"frames",{}).values():
            frame.destroy()
            
        self.frames = {}
        for F in (MainMenu, SettingsPage, GamePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    def refresh_theme(self,apperance,color_theme):
        ctk.set_appearance_mode(apperance)
        ctk.set_default_color_theme(color_theme)
        self.build_frames()
        self.show_frame("SettingsPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def close(self):
        self.quit()


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Main Menu").grid(row=0,column=0,pady=BUTTON_PADY,padx=BUTTON_PADX)
        ctk.CTkButton(self, text="Start Game", command=lambda: controller.show_frame("GamePage")).grid(row=1,column=0,pady=BUTTON_PADY,padx=BUTTON_PADX)
        ctk.CTkButton(self, text="Settings", command=lambda: controller.show_frame("SettingsPage")).grid(row=2,column=0,pady=BUTTON_PADY,padx=BUTTON_PADX)
        ctk.CTkButton(self, text= "QUIT", command= controller.close).grid(row=3,column=0,pady=BUTTON_PADY,padx=BUTTON_PADX)

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        settingsLabel=ctk.CTkLabel(self, text="Settings")
        settingsLabel.pack(pady=5)
        
        colorThemeLabel=ctk.CTkLabel(self, text="Game Appearance")
        colorThemeLabel.pack(pady=5)
        
        apperanceSelection = ctk.StringVar(value='light')
        
        apperanceRadio1=ctk.CTkRadioButton(self, text="Light", variable=apperanceSelection, value='light')
        apperanceRadio1.pack(pady=5)
        
        apperanceRadio2=ctk.CTkRadioButton(self, text="Dark", variable=apperanceSelection, value="dark")
        apperanceRadio2.pack(pady=5)


        buttonThemeLabel=ctk.CTkLabel(self, text="Color theme")
        buttonThemeLabel.pack(pady=5)


        colorSelection = ctk.StringVar(value='colors')

        setThemeBlueButton=ctk.CTkRadioButton(self, text="Blue", variable=colorSelection, value='blue')
        setThemeBlueButton.pack(pady=5)
        setThemeGreenButton=ctk.CTkRadioButton(self, text="Green", variable=colorSelection, value='green')
        setThemeGreenButton.pack(pady=5)
        setThemeDarkBlueButton=ctk.CTkRadioButton(self, text="Dark Blue", variable=colorSelection, value='dark-blue')
        setThemeDarkBlueButton.pack(pady=5)
        
        saveChanges=ctk.CTkButton(self,text= "Save Changes",command=lambda: controller.refresh_theme(apperance=apperanceSelection.get(),
                                                                                                     color_theme= colorSelection.get()))
        saveChanges.pack(pady=5)
        


        backButton=ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainMenu"))
        backButton.pack(pady=5)
    

class GamePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Game Page").pack(pady=20)
        ctk.CTkButton(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
