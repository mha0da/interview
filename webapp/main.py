from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel


app = FastAPI(
    title="Chat API",
    description="This is a simple API for chatting.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Message(BaseModel):
    content: str
    user: str
    room: str
    type: str


class ConnectionManager:

    def __init__(self):
        self.connections = dict()

    async def connect(self, websocket: WebSocket, room: str, username: str):
        """
        Add websocket connection to record list.

        Parameters:
        websocket (WebSocket): websocket created
        room (str): The chat room number
        username (str): The user name
        """
        key = room + "_" + username
        self.connections[key] = websocket
        await websocket.accept()

    async def disconnect(self, username: str, room: str, close_code: int):
        """
        Close websocket connection and delete it from connection records.

        Parameters:
        username (str): The user name
        room (str): The chat room number
        close_code (int): The code for closing websocket connection
        """
        key = room + "_" + username
        if key in self.connections.keys():
            await self.connections[key].close(close_code, "disconnection")
            del self.connections[key]
            message = Message(content=f"Member {username} Quit.", user=username, type="info", room=room)
            await self.broadcast(message)

    async def broadcast(self, message: Message):
        """
        Broadcast message to the clients within same chat room.

        Parameters:
        message (dict): The message sending to clients.
        """
        for k in self.connections.keys():
            if k.split("_")[0] == message.room:
                await self.connections[k].send_json(dict(message))


manager = ConnectionManager()


@app.get(
    "/",
    response_class=HTMLResponse,
    description="Login for collect user name and chat room number.",
)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")


@app.get(
    "/{room}/{username}",
    response_class=HTMLResponse,
    description="Chat room for group communication.",
)
async def chat(request: Request, room: str, username: str):
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"username": username, "room": room}
    )


@app.websocket("/ws/{room}/{username}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: str):
    key = room + "_" + username
    if key not in manager.connections.keys():
        await manager.connect(websocket, room, username)
        while True:
            try:
                data = await websocket.receive_json()
                message = Message(**data)
                await manager.broadcast(message)
            except WebSocketDisconnect:
                await manager.disconnect(username, room, 1006)


@app.get(
    "/disconnect/{room}/{username}", description="Disconnect websocket connection."
)
async def websocket_disconnect(username: str, room: str):
    await manager.disconnect(username, room, 1000)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
        ws_ping_interval=30.0,
    )
