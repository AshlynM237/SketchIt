import customtkinter as ctk
import json
import os

CONFIG_PATH = "config/settings.json"

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.switch_callback = switch_callback
        self.theme_var = ctk.StringVar(value="blue")
        self.mode_var = ctk.StringVar(value="dark")
        self.volume_var = ctk.DoubleVar(value=0.5)

        ctk.CTkLabel(self, text="Settings").pack(pady=15)

        ctk.CTkLabel(self, text="Theme").pack()
        ctk.CTkOptionMenu(self, values=["blue", "green", "red"], variable=self.theme_var).pack(pady=5)

        ctk.CTkLabel(self, text="Appearance Mode").pack()
        ctk.CTkOptionMenu(self, values=["dark", "light"], variable=self.mode_var).pack(pady=5)

        ctk.CTkLabel(self, text="Volume").pack()
        ctk.CTkSlider(self, from_=0, to=1, variable=self.volume_var).pack(pady=10)

        ctk.CTkButton(self, text="Save", command=self.save_settings).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: self.switch_callback("matchmaking")).pack(pady=10)

    def save_settings(self):
        data = {
            "theme": self.theme_var.get(),
            "mode": self.mode_var.get(),
            "volume": self.volume_var.get()
        }
        os.makedirs("config", exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)
