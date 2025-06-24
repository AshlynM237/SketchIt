import customtkinter as ctk
from hint_manager import loadWords
import random
import customtkinter as ctk
import tkinter as tk
import json
import os

global player_name
player_name = ""
option_chosen = ""

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
        for F in (MainMenu, SettingsPage, GamePage, OptionPage, DrawingPage):
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

        gameTextBox=ctk.CTkTextbox(self, width=100, height = 20, corner_radius=0,activate_scrollbars = False) 
        gameTextBox.pack(pady=5)


        player_name = gameTextBox.get("1.0", "end").strip()
        gamePlayOneOnOne = ctk.CTkButton(self,text="Play one on one",  command=lambda: controller.show_frame("OptionPage"))
        gamePlayOneOnOne.pack(pady=5)
        
        gameCreateRoom = ctk.CTkButton(self,text="Create Room",  command=lambda: controller.show_frame("MainMenu"))
        gameCreateRoom.pack(pady=5)
        
        gameJoinRoom =ctk.CTkButton(self,text="Join Room",  command=lambda: controller.show_frame("MainMenu"))
        gameJoinRoom.pack(pady=5)
        
        gameBacktoMenu = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"))
        gameBacktoMenu.pack(pady=5)

class OptionPage(ctk.CTkFrame):
    def __init__(self, parent, controller,options=loadWords()):
        super().__init__(parent)
        self.controller = controller
        optionsCapacity = len(options)-1
        used = []

        ChoiceLabel=ctk.CTkLabel(self, text="Choose a word:")
        ChoiceLabel.pack(pady=5)


        for i in range(3):
            optionsCapacity = len(options)-1
            optionIndex = random.randint(0,optionsCapacity)
            optionName = options[optionIndex]

            used.append(optionName)
            if optionName in used:
                optionIndex = random.randint(0,optionsCapacity)
                optionName = options[optionIndex]

            options1 = ctk.CTkButton(self, text = optionName, command = lambda: controller.show_frame("DrawingPage"))
            options1.pack(pady=5)

class DrawingPage(ctk.CTkFrame):
    def __init__(self, parent, controller, logfile="drawing.jsonl"):
        super().__init__(parent)
        self.controller = controller

        # where we append segments
        self.logfile = os.path.abspath(logfile)

        # Button frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Clear", command=self.clear_canvas).pack(side="left")
        ctk.CTkButton(btn_frame, text="Print", command=self.print_points).pack(side="left")

        # Drawing canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # State
        self.last_x = None
        self.last_y = None
        self.points = []

        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move)

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_move(self, event):
        x, y = event.x, event.y
        seg = ((self.last_x, self.last_y), (x, y))
        # draw
        self.canvas.create_line(*seg[0], *seg[1], width=2, capstyle=tk.ROUND)
        # store in memory
        self.points.append(seg)
        # write to disk
        self._log_segment(seg)
        self.last_x, self.last_y = x, y

    def _log_segment(self, seg):
        line = json.dumps([list(seg[0]), list(seg[1])])
        with open(self.logfile, "a") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        # reset log file
        open(self.logfile, "w").close()

    def print_points(self):
        print("Drawing points:")
        for seg in self.points:
            print(seg)



if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
    app = DrawingPage()