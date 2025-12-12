import customtkinter as ctk
import threading
import sys
import os

# Add parent directory to path to import websocket_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from websocket_client import WebSocketClient

class MatchmakingFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback, websocket_client: WebSocketClient = None):
        super().__init__(master)
        self.switch_callback = switch_callback
        self.websocket_client = websocket_client
        self.matchmaking_active = False

        ctk.CTkLabel(self, text="Welcome to SketchIt!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        ctk.CTkLabel(self, text="Find a player and start drawing!", font=ctk.CTkFont(size=16)).pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=10)

        self.matchmaking_button = ctk.CTkButton(self, text="Start Matchmaking", command=self.start_matchmaking)
        self.matchmaking_button.pack(pady=10)
        
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_matchmaking, state="disabled")
        self.cancel_button.pack(pady=5)

        ctk.CTkButton(self, text="Settings", command=lambda: self.switch_callback("settings")).pack(pady=5)
        ctk.CTkButton(self, text="High Scores", command=lambda: self.switch_callback("scores")).pack(pady=5)
        ctk.CTkButton(self, text="How to Play", command=lambda: self.switch_callback("instructions")).pack(pady=5)

    def start_matchmaking(self):
        """Start the matchmaking process."""
        if not self.websocket_client:
            # Create websocket client if not provided
            self.websocket_client = WebSocketClient()
        
        # Set up callbacks
        self.websocket_client.set_on_matched(self.on_matched)
        self.websocket_client.set_on_connection_error(self.on_connection_error)
        self.websocket_client.set_on_partner_left(self.on_partner_left)
        
        # Update UI
        self.status_label.configure(text="Connecting to server...")
        self.matchmaking_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.matchmaking_active = True
        
        # Connect to websocket
        self.websocket_client.connect()
        
        # Check connection status
        threading.Thread(target=self.check_connection_status, daemon=True).start()

    def check_connection_status(self):
        """Periodically check connection status and update UI."""
        import time
        max_wait = 5  # Wait up to 5 seconds for connection
        waited = 0
        
        while self.matchmaking_active and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
            if self.websocket_client.is_connected():
                self.status_label.after(0, lambda: self.status_label.configure(text="Waiting for another player..."))
                break
        
        if not self.websocket_client.is_connected() and self.matchmaking_active:
            self.status_label.after(0, lambda: self.status_label.configure(text="Connection failed. Please try again."))
            self.matchmaking_button.after(0, lambda: self.matchmaking_button.configure(state="normal"))
            self.cancel_button.after(0, lambda: self.cancel_button.configure(state="disabled"))
            self.matchmaking_active = False

    def on_matched(self):
        """Called when a match is found."""
        if self.matchmaking_active:
            self.status_label.after(0, lambda: self.status_label.configure(text="Match found! Starting game..."))
            self.matchmaking_button.after(0, lambda: self.matchmaking_button.configure(state="normal"))
            self.cancel_button.after(0, lambda: self.cancel_button.configure(state="disabled"))
            self.matchmaking_active = False
            
            # Switch to drawing frame after a short delay
            self.after(1000, lambda: self.switch_callback("drawing", self.websocket_client))

    def on_connection_error(self, error: str):
        """Called when there's a connection error."""
        if self.matchmaking_active:
            self.status_label.after(0, lambda: self.status_label.configure(text=f"Connection error: {error}"))
            self.matchmaking_button.after(0, lambda: self.matchmaking_button.configure(state="normal"))
            self.cancel_button.after(0, lambda: self.cancel_button.configure(state="disabled"))
            self.matchmaking_active = False

    def on_partner_left(self):
        """Called when the partner disconnects."""
        self.status_label.after(0, lambda: self.status_label.configure(text="Partner disconnected. Returning to matchmaking..."))
        # Could switch back to matchmaking or show a message

    def cancel_matchmaking(self):
        """Cancel the matchmaking process."""
        self.matchmaking_active = False
        if self.websocket_client:
            self.websocket_client.disconnect()
        self.status_label.configure(text="Matchmaking cancelled.")
        self.matchmaking_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
