from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from typing import Dict
from app.schemas.schemas import ChatSelection

router = APIRouter(prefix="/ws/chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections : Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket : WebSocket, room_id : int, user_id : int):
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    async def disconnect(self, room_id : int, user_id : int):
        if room_id in self.active_connections.keys and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message : str, room_id : int, sender_id : int):
        for user, connection in self.active_connections[room_id]:
            message_class = {
                "text" : message,
                "is_self" : user == sender_id
            }
            await connection.send_json(message_class)


manager = ConnectionManager()

@router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    username = websocket.query_params.get("username", f"User_{user_id}")
    await manager.connect(websocket=websocket, room_id=room_id, user_id=user_id)
    await manager.broadcast(f"{username} (ID: {user_id}) присоединился к чату.", room_id, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username} (ID: {user_id}): {data}", room_id, user_id)
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast(f"{username} (ID: {user_id}) покинул чат.", room_id, user_id)


@router.post("/join_chat")
async def join_chat(body : ChatSelection):
    return
