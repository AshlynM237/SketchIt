import tkinter as tk
import customtkinter as ctk
import sys
import os

# Add parent directory to path to import websocket_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from websocket_client import WebSocketClient

class DrawingFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback, websocket_client: WebSocketClient = None):
        super().__init__(master)
        self.switch_callback = switch_callback
        self.websocket_client = websocket_client

        self.label = ctk.CTkLabel(self, text="Draw the word shown below:")
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="white", width=700, height=500)
        self.canvas.pack(pady=20)

        self.last_x, self.last_y = None, None
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_pos)

        # Set up websocket callbacks if client is provided
        if self.websocket_client:
            self.websocket_client.set_on_draw(self.remote_draw)
            self.websocket_client.set_on_partner_left(self.on_partner_left)

        # Navigation buttons
        self.bottom = ctk.CTkFrame(self)
        self.bottom.pack(fill="x", pady=10)
        ctk.CTkButton(self.bottom, text="Back to Menu", command=self.go_back).pack(side="left", padx=5)
        ctk.CTkButton(self.bottom, text="Settings", command=lambda: self.switch_callback("settings")).pack(side="left", padx=5)
        ctk.CTkButton(self.bottom, text="Scores", command=lambda: self.switch_callback("scores")).pack(side="left", padx=5)

    def draw(self, event):
        """Handle local drawing and send to partner via websocket."""
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            # Draw locally
            self.canvas.create_line(self.last_x, self.last_y, x, y, 
                                   fill="black", width=3, capstyle="round", smooth=True)
            
            # Send drawing data to partner via websocket
            if self.websocket_client and self.websocket_client.is_connected() and self.websocket_client.is_matched():
                message = f"DRAW {self.last_x} {self.last_y} {x} {y}"
                self.websocket_client.send_message(message)
        
        self.last_x, self.last_y = x, y

    def remote_draw(self, x1, y1, x2, y2):
        """Handle remote drawing data received from partner."""
        # Draw on canvas (callback is scheduled in main thread via websocket_client)
        try:
            self.canvas.create_line(x1, y1, x2, y2, 
                                   fill="blue", width=3, 
                                   capstyle="round", smooth=True)
        except Exception as e:
            print(f"Error drawing remote line: {e}")

    def reset_pos(self, event):
        """Reset drawing position when mouse is released."""
        self.last_x, self.last_y = None, None

    def on_partner_left(self):
        """Handle partner disconnection."""
        # Show a message and return to matchmaking
        self.label.configure(text="Partner disconnected. Returning to menu...")
        self.after(2000, self.go_back)

    def go_back(self):
        """Return to matchmaking menu."""
        if self.websocket_client:
            self.websocket_client.disconnect()
        self.switch_callback("matchmaking", self.websocket_client)
