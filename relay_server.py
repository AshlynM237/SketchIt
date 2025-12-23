import asyncio
import websockets

waiting = None
pairs = {}

async def handler(websocket):
    global waiting

    print("Client connected")

    if waiting is None:
        waiting = websocket
        print("Client is waiting for a partner")
    else:
        partner = waiting
        pairs[websocket] = partner
        pairs[partner] = websocket
        waiting = None
        print("Two clients matched")

        try:
            await websocket.send("MATCHED")
            await partner.send("MATCHED")
        except:
            pass

    try:
        async for msg in websocket:
            print("Received:", msg)

            if websocket in pairs:
                partner = pairs[websocket]
                try:
                    await partner.send(msg)
                except:
                    pass

    except Exception as e:
        print("Client error:", e)

    finally:
        print("Client disconnected")

        if waiting is websocket:
            waiting = None

        if websocket in pairs:
            partner = pairs[websocket]
            try:
                await partner.send("PARTNER_LEFT")
            except:
                pass

            del pairs[partner]
            del pairs[websocket]

        await websocket.close()


async def main():
    print("Matchmaking WebSocket running on port 8001")
    async with websockets.serve(handler, "0.0.0.0", 8001):
        await asyncio.Future()

asyncio.run(main())
