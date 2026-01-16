import customtkinter as ctk

class ScoresFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.switch_callback = switch_callback

        ctk.CTkLabel(self, text="🏆 Global High Scores", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        self.scores_list = ctk.CTkTextbox(self, width=400, height=300)
        self.scores_list.pack(pady=10)
        self.load_dummy_scores()

        ctk.CTkButton(self, text="Back", command=lambda: self.switch_callback("matchmaking")).pack(pady=10)

    def load_dummy_scores(self):
        dummy_data = [
            ("PlayerA", 1500),
            ("PlayerB", 1270),
            ("PlayerC", 990),
            ("PlayerD", 880),
            ("PlayerE", 750),
        ]
        self.scores_list.delete("1.0", "end")
        for name, score in dummy_data:
            self.scores_list.insert("end", f"{name:<15} {score}\n")
