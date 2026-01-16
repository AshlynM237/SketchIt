import customtkinter as ctk
from frames.matchmaking_frame import MatchmakingFrame
from frames.drawing_frame import DrawingFrame
from frames.settings_frame import SettingsFrame
from frames.scores_frame import ScoresFrame
from frames.instructions_frame import InstructionsFrame
from websocket_client import WebSocketClient

class SketchItApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SketchIt!")
        self.geometry("900x700")

        # Create websocket client instance to be shared across frames
        self.websocket_client = WebSocketClient()

        self.current_frame = None
        self.switch_frame("matchmaking")

    def switch_frame(self, name, websocket_client=None):
        """Switch to a different frame. Optionally pass websocket_client."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Use provided websocket_client or the app's instance
        ws_client = websocket_client if websocket_client is not None else self.websocket_client

        frame_classes = {
            "matchmaking": MatchmakingFrame,
            "drawing": DrawingFrame,
            "settings": SettingsFrame,
            "scores": ScoresFrame,
            "instructions": InstructionsFrame
        }

        FrameClass = frame_classes[name]
        
        # Pass websocket_client to frames that need it
        if name in ["matchmaking", "drawing"]:
            self.current_frame = FrameClass(self, switch_callback=self.switch_frame, websocket_client=ws_client)
        else:
            self.current_frame = FrameClass(self, switch_callback=self.switch_frame)
        
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)


if __name__ == "__main__":
    app = SketchItApp()
    app.mainloop()
