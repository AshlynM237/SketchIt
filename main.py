import customtkinter as ctk

BUTTON_PADY=20
BUTTON_PADX=10
appearance_mode = "dark" # Modes: system (default), light, dark
color_theme = "blue" # Themes: blue (default), dark-blue, green
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

        self.frames = {}

        for F in (MainMenu, SettingsPage, GamePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

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

def change_color_mode(color):
    ctk.set_appearance_mode(color)

def change_theme_color(color):
    ctk.set_default_color_theme(color)

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        settingsLabel=ctk.CTkLabel(self, text="Settings")
        settingsLabel.pack(pady=5)
        
        colorThemeLabel=ctk.CTkLabel(self, text="Game Appearance")
        colorThemeLabel.pack(pady=5)

        lightModeButton = ctk.CTkButton(self, text="Light", command=lambda: change_color_mode("light"))
        lightModeButton.pack(pady=5)

        darkModeButton = ctk.CTkButton(self, text="Dark", command=lambda: change_color_mode("dark"))
        darkModeButton.pack(pady=5)

        buttonThemeLabel=ctk.CTkLabel(self, text="Color theme")
        buttonThemeLabel.pack(pady=5)

        setThemeBlueButton = ctk.CTkButton(self, text = "Blue", command=lambda: change_theme_color("blue"))
        setThemeBlueButton.pack(pady=5)
        setThemeGreenButton = ctk.CTkButton(self, text = "Green", command=lambda: change_theme_color("green"))
        setThemeGreenButton.pack(pady=5)
        setThemeDarkBlueButton = ctk.CTkButton(self, text = "Dark Blue", command=lambda: change_theme_color("dark-blue"))
        setThemeDarkBlueButton.pack(pady=5)


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
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()


# customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

# app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry("400x240")

# def button_function():
#     print("button pressed")
#     customtkinter.set_appearance_mode("light")
    
# def setThemeBlue():
#     customtkinter.set_default_color_theme("blue")
#     render_ui()
    
# def setThemeDarkBlue():
#     customtkinter.set_default_color_theme("dark-blue")
#     render_ui()
    
# def setThemeGreen():
#     customtkinter.set_default_color_theme("green")
#     render_ui()
    
# def setThemeRed():
#     customtkinter.set_default_color_theme("./red.json")
#     render_ui() 

# # # Use CTkButton instead of tkinter Button
# # button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# # button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
# def render_ui():
#     setThemeToBlueButton = customtkinter.CTkButton(master=app, text="Blue",command=setThemeBlue)
#     setThemeToBlueButton.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

#     setThemeToDarkBlueButton = customtkinter.CTkButton(master=app, text="Dark Blue", command=setThemeDarkBlue)
#     setThemeToDarkBlueButton.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

#     setThemeToGreenButton = customtkinter.CTkButton(master=app, text="Green", command=setThemeGreen)
#     setThemeToGreenButton.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
    
#     setThemeToRedButton = customtkinter.CTkButton(master=app, text="Red", command=setThemeRed)
#     setThemeToRedButton.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)
    
# render_ui()
# app.mainloop()
