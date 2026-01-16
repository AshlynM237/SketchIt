import asyncio
import threading
import websockets
from typing import Optional, Callable


class WebSocketClient:
    """WebSocket client for matchmaking and real-time drawing communication."""
    
    def __init__(self, uri: str = "ws://18.135.26.67:8001"):
        self.uri = uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self.connected = False
        self.matched = False
        
        # Callbacks
        self.on_matched: Optional[Callable] = None
        self.on_draw: Optional[Callable] = None
        self.on_partner_left: Optional[Callable] = None
        self.on_connection_error: Optional[Callable] = None
        
    def set_on_matched(self, callback: Callable):
        """Set callback for when a match is found."""
        self.on_matched = callback
    
    def set_on_draw(self, callback: Callable):
        """Set callback for when drawing data is received."""
        self.on_draw = callback
    
    def set_on_partner_left(self, callback: Callable):
        """Set callback for when partner disconnects."""
        self.on_partner_left = callback
    
    def set_on_connection_error(self, callback: Callable):
        """Set callback for connection errors."""
        self.on_connection_error = callback
    
    async def _connect(self):
        """Internal connection method."""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            print("Connected to relay server")
            
            # Listen for messages
            async for message in self.websocket:
                await self._handle_message(message)
                
        except Exception as e:
            print(f"WebSocket error: {e}")
            self.connected = False
            if self.on_connection_error:
                self._run_callback(self.on_connection_error, str(e))
        finally:
            self.connected = False
            if self.websocket:
                try:
                    await self.websocket.close()
                except:
                    pass
    
    async def _handle_message(self, message: str):
        """Handle incoming messages from the server."""
        print(f"Received: {message}")
        
        if message == "MATCHED":
            self.matched = True
            if self.on_matched:
                self._run_callback(self.on_matched)
        elif message == "PARTNER_LEFT":
            self.matched = False
            if self.on_partner_left:
                self._run_callback(self.on_partner_left)
        elif message.startswith("DRAW"):
            # Handle drawing data: DRAW x1 y1 x2 y2
            parts = message.split()
            if len(parts) == 5:
                try:
                    x1, y1, x2, y2 = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                    if self.on_draw:
                        self._run_callback(self.on_draw, x1, y1, x2, y2)
                except ValueError:
                    print(f"Invalid DRAW message format: {message}")
        # Handle other message types (chat, game state, etc.) here if needed
    
    def _run_callback(self, callback: Callable, *args):
        """Run a callback in the main thread safely."""
        if callback:
            try:
                # Schedule callback to run in main thread using after_idle
                # This ensures tkinter operations are thread-safe
                import tkinter as tk
                try:
                    root = tk._default_root
                    if root and root.winfo_exists():
                        if args:
                            root.after_idle(lambda cb=callback, a=args: cb(*a))
                        else:
                            root.after_idle(callback)
                    else:
                        # Fallback: call directly (may work if already in main thread)
                        if args:
                            callback(*args)
                        else:
                            callback()
                except (AttributeError, RuntimeError):
                    # Fallback if tkinter root not available
                    if args:
                        callback(*args)
                    else:
                        callback()
            except Exception as e:
                print(f"Callback error: {e}")
    
    async def send(self, message: str):
        """Send a message through the WebSocket."""
        if self.websocket and self.connected:
            try:
                await self.websocket.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                self.connected = False
    
    def send_message(self, message: str):
        """Thread-safe method to send a message."""
        if self.loop and self.connected:
            asyncio.run_coroutine_threadsafe(self.send(message), self.loop)
    
    def _run_loop(self):
        """Run the asyncio event loop in a separate thread."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect())
    
    def connect(self):
        """Start the WebSocket connection in a separate thread."""
        if not self.connected and (self.thread is None or not self.thread.is_alive()):
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
    
    def disconnect(self):
        """Disconnect from the WebSocket."""
        self.connected = False
        if self.loop:
            # Schedule close in the event loop
            if self.websocket:
                asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
    
    def is_connected(self) -> bool:
        """Check if connected to the server."""
        return self.connected
    
    def is_matched(self) -> bool:
        """Check if matched with another player."""
        return self.matched

