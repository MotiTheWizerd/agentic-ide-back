import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.core.di.registry import registry
from app.core.security import decode_token
from app.core.ws import ws_manager, WSMessage
from app.modules.execution.manager import ExecutionManager

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, token: str = Query(...)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        await ws.close(code=4001, reason="Invalid or expired token")
        return

    user_id = int(payload["sub"])
    await ws_manager.connect(user_id, ws)

    try:
        await ws_manager.send_to_user(
            user_id,
            WSMessage(type="connection.ready", data={"user_id": user_id}),
        )

        while True:
            message = await ws.receive()

            if message.get("type") == "websocket.disconnect":
                break

            text = message.get("text")
            if not text:
                continue

            try:
                raw = json.loads(text)
                msg = WSMessage(**raw)
            except Exception as e:
                logger.warning("WS bad message from user %d: %s", user_id, e)
                continue

            if msg.type == "ping":
                await ws_manager.send_to_user(
                    user_id, WSMessage(type="pong")
                )
            elif msg.type == "execution.start":
                exec_manager = registry.resolve(ExecutionManager)
                run_id = await exec_manager.run(
                    user_id=user_id,
                    flow_id=msg.data.get("flow_id", ""),
                    nodes=msg.data.get("nodes", []),
                    edges=msg.data.get("edges", []),
                    provider_id=msg.data.get("provider_id", ""),
                    trigger_node_id=msg.data.get("trigger_node_id"),
                    cached_outputs=msg.data.get("cached_outputs"),
                )
                await ws_manager.send_to_user(
                    user_id,
                    WSMessage(type="execution.started", data={"run_id": run_id}),
                )
            else:
                logger.info("WS recv from user %d: %s", user_id, msg.type)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.exception("WS error for user %d: %s", user_id, e)
    finally:
        ws_manager.disconnect(user_id, ws)
