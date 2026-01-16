import asyncio
import threading
import tkinter as tk
import customtkinter as ctk
import websockets

class DrawingFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.send_callback = None
        self.last_x = None
        self.last_y = None

        self.label = ctk.CTkLabel(self, text="Shared Drawing Canvas")
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="white", width=700, height=500)
        self.canvas.pack(pady=20)

        self.canvas.bind("<B1-Motion>", self.local_draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_pos)

    def set_send_callback(self, func):
        self.send_callback = func

    def local_draw(self, event):
        x, y = event.x, event.y

        if self.last_x is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y,
                                    fill="black", width=3, capstyle="round", smooth=True)

            if self.send_callback:
                msg = f"DRAW {self.last_x} {self.last_y} {x} {y}"
                # Call the async callback in a thread-safe way
                asyncio.run_coroutine_threadsafe(
                    self.send_callback(msg), 
                    self.loop
                )

        self.last_x, self.last_y = x, y

    def remote_draw(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2,
                                fill="black", width=3, capstyle="round", smooth=True)

    def reset_pos(self, event):
        self.last_x = None
        self.last_y = None

    def set_loop(self, loop):
        self.loop = loop


async def client_listener(websocket, gui):
    """Listen for messages from the WebSocket server"""
    try:
        async for message in websocket:
            print("Received:", message)
            if message.startswith("DRAW"):
                _, x1, y1, x2, y2 = message.split()
                gui.remote_draw(float(x1), float(y1), float(x2), float(y2))
    except Exception as e:
        print("Client listener error:", e)


async def websocket_client(gui):
    """Maintain WebSocket connection"""
    uri = "ws://18.135.26.67:8001"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to relay server")
        
        # Set up the send callback
        async def send_data(msg):
            await websocket.send(msg)
        
        gui.set_send_callback(send_data)
        
        # Listen for incoming messages
        await client_listener(websocket, gui)


def run_async_loop(loop, coro):
    """Run the async event loop in a separate thread"""
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)


def start_client():
    root = ctk.CTk()
    root.title("Client Drawing App")

    frame = DrawingFrame(root)
    frame.pack(padx=20, pady=20)

    # Create a new event loop for the WebSocket thread
    loop = asyncio.new_event_loop()
    frame.set_loop(loop)

    # Start WebSocket client in a separate thread
    ws_thread = threading.Thread(
        target=run_async_loop, 
        args=(loop, websocket_client(frame)), 
        daemon=True
    )
    ws_thread.start()

    root.mainloop()


if __name__ == "__main__":
    start_client()