import asyncio
import websockets
import threading
import queue

# Queue to store messages
message_queue = queue.Queue()

# Function to simulate message producer
def message_producer():
    while True:
        message = input("Enter a message to send (or 'exit' to quit): ")
        if message == 'exit':
            break
        message_queue.put(message)

# WebSocket server coroutine
async def websocket_server(websocket, path):
    while True:
        try:
            # Wait for messages in the queue
            message = message_queue.get()
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            break

# Starting the WebSocket server
async def start_server():
    server = await websockets.serve(websocket_server, 'localhost', 8765)
    await server.wait_closed()

# Starting the message producer thread
producer_thread = threading.Thread(target=message_producer)
producer_thread.start()

# Running the event loop for the WebSocket server
asyncio.get_event_loop().run_until_complete(start_server())
