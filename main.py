import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    print("button pressed")
    customtkinter.set_appearance_mode("light")
    
def setThemeBlue():
    customtkinter.set_default_color_theme("blue")
    render_ui()
    
def setThemeDarkBlue():
    customtkinter.set_default_color_theme("dark-blue")
    render_ui()
    
def setThemeGreen():
    customtkinter.set_default_color_theme("green")
    render_ui()
    
def setThemeRed():
    customtkinter.set_default_color_theme("./red.json")
    render_ui() 

# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
def render_ui():
    setThemeToBlueButton = customtkinter.CTkButton(master=app, text="Blue",command=setThemeBlue)
    setThemeToBlueButton.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

    setThemeToDarkBlueButton = customtkinter.CTkButton(master=app, text="Dark Blue", command=setThemeDarkBlue)
    setThemeToDarkBlueButton.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

    setThemeToGreenButton = customtkinter.CTkButton(master=app, text="Green", command=setThemeGreen)
    setThemeToGreenButton.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
    
    setThemeToRedButton = customtkinter.CTkButton(master=app, text="Red", command=setThemeRed)
    setThemeToRedButton.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)
    
render_ui()
app.mainloop()
