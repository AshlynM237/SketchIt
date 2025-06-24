import customtkinter as ctk
import tkinter as tk
import json
import os


class DrawApp(ctk.CTk):
    def __init__(self, logfile="drawing.jsonl"):
        super().__init__()
        self.title("Draw & Share")
        self.geometry("600x400")

        # where we append segments
        self.logfile = os.path.abspath(logfile)

        # Button frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Clear",
                      command=self.clear_canvas).pack(side="left")
        ctk.CTkButton(btn_frame, text="Print",
                      command=self.print_points).pack(side="left")

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
    app = DrawApp()
    app.mainloop()
