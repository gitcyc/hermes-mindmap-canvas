import json
import os
import re
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

DATA_ROOT = Path(os.environ.get("DATA_DIR", "/data"))
MAP_DIR = DATA_ROOT / "mindmaps"
MAP_DIR.mkdir(parents=True, exist_ok=True)

APP_DIR = Path(__file__).parent
STATIC_DIR = APP_DIR / "static"

app = FastAPI(title="Hermes Mindmap Canvas")

connections: dict[str, list[WebSocket]] = {}


def safe_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9_-]+", "-", name)
    return name or "default"


def map_path(name: str) -> Path:
    return MAP_DIR / f"{safe_name(name)}.json"


def new_id(prefix: str = "node") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def default_map(name: str) -> dict[str, Any]:
    return {
        "id": safe_name(name),
        "title": name,
        "nodes": [
            {
                "id": "root",
                "label": name,
                "status": "doing",
                "notes": "",
                "x": 0,
                "y": 0,
            }
        ],
        "edges": [],
    }


def load_map(name: str) -> dict[str, Any]:
    p = map_path(name)
    if not p.exists():
        data = default_map(name)
        save_map(name, data)
        return data
    data = json.loads(p.read_text(encoding="utf-8"))
    data.setdefault("nodes", [])
    data.setdefault("edges", [])
    return data


def save_map(name: str, data: dict[str, Any]) -> None:
    p = map_path(name)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def find_node(data: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    for node in data.get("nodes", []):
        if node.get("id") == node_id:
            return node
    return None


def count_children(data: dict[str, Any], parent_id: str) -> int:
    return sum(1 for e in data.get("edges", []) if e.get("source") == parent_id)


def add_node(data: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    label = op.get("label") or op.get("title")
    if not label:
        raise HTTPException(status_code=400, detail="add_node requires label")

    parent_id = op.get("parent_id") or op.get("parent") or "root"
    parent = find_node(data, parent_id)

    node_id = op.get("id") or new_id("node")
    if find_node(data, node_id):
        node_id = new_id("node")

    if parent:
        idx = count_children(data, parent_id)
        x = int(op.get("x", parent.get("x", 0) + 300))
        y = int(op.get("y", parent.get("y", 0) + (idx * 110) - 80))
    else:
        x = int(op.get("x", 300))
        y = int(op.get("y", 0))

    node = {
        "id": node_id,
        "label": str(label),
        "status": op.get("status", "todo"),
        "notes": op.get("notes", ""),
        "x": x,
        "y": y,
    }
    data.setdefault("nodes", []).append(node)

    if parent:
        edge_id = op.get("edge_id") or f"edge-{parent_id}-{node_id}"
        data.setdefault("edges", []).append(
            {
                "id": edge_id,
                "source": parent_id,
                "target": node_id,
                "label": op.get("edge_label", ""),
            }
        )

    return node


def update_node(data: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    node_id = op.get("id") or op.get("node_id")
    if not node_id:
        raise HTTPException(status_code=400, detail="update_node requires id")

    node = find_node(data, node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"node not found: {node_id}")

    known_fields = ["label", "status", "notes", "x", "y", "priority", "type", "owner", "source", "attachments"]
    for key in known_fields:
        if key in op:
            node[key] = op[key]

    return node


def delete_node(data: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    node_id = op.get("id") or op.get("node_id")
    if not node_id:
        raise HTTPException(status_code=400, detail="delete_node requires id")
    if node_id == "root":
        raise HTTPException(status_code=400, detail="cannot delete root")

    before = len(data.get("nodes", []))
    data["nodes"] = [n for n in data.get("nodes", []) if n.get("id") != node_id]
    data["edges"] = [
        e
        for e in data.get("edges", [])
        if e.get("source") != node_id and e.get("target") != node_id
    ]

    return {"deleted": before - len(data["nodes"])}


def connect_nodes(data: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    source = op.get("source")
    target = op.get("target")
    if not source or not target:
        raise HTTPException(status_code=400, detail="connect_nodes requires source and target")
    if not find_node(data, source):
        raise HTTPException(status_code=404, detail=f"source not found: {source}")
    if not find_node(data, target):
        raise HTTPException(status_code=404, detail=f"target not found: {target}")

    edge = {
        "id": op.get("id") or f"edge-{source}-{target}-{uuid.uuid4().hex[:4]}",
        "source": source,
        "target": target,
        "label": op.get("label", ""),
    }
    data.setdefault("edges", []).append(edge)
    return edge


def auto_layout(data: dict[str, Any]) -> dict[str, Any]:
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    children: dict[str, list[str]] = {}
    for e in data.get("edges", []):
        children.setdefault(e["source"], []).append(e["target"])

    levels: dict[str, int] = {"root": 0}
    queue = ["root"]
    while queue:
        current = queue.pop(0)
        for child in children.get(current, []):
            if child not in levels:
                levels[child] = levels[current] + 1
                queue.append(child)

    by_level: dict[int, list[str]] = {}
    for node_id in nodes:
        level = levels.get(node_id, 0)
        by_level.setdefault(level, []).append(node_id)

    for level, ids in by_level.items():
        for i, node_id in enumerate(ids):
            nodes[node_id]["x"] = level * 320
            nodes[node_id]["y"] = i * 120 - (len(ids) - 1) * 60

    return {"layout": "done"}


def build_tree(data: dict[str, Any]) -> dict[str, Any]:
    nodes_by_id = {n["id"]: n for n in data.get("nodes", [])}
    children_map: dict[str, list[str]] = {}
    for e in data.get("edges", []):
        children_map.setdefault(e["source"], []).append(e["target"])
    return nodes_by_id, children_map


def render_markdown(nodes_by_id, children_map, node_id, depth=0) -> str:
    node = nodes_by_id.get(node_id)
    if not node:
        return ""
    indent = "  " * depth
    line = f"{indent}- {node.get('label', node_id)}"
    status = node.get("status")
    if status:
        line += f" [{status}]"
    priority = node.get("priority")
    if priority:
        line += f" priority:{priority}"
    ntype = node.get("type")
    if ntype:
        line += f" type:{ntype}"
    owner = node.get("owner")
    if owner:
        line += f" owner:{owner}"
    notes = node.get("notes", "").strip()
    if notes:
        note_preview = notes[:80].replace("\n", " ")
        line += f" — {note_preview}"
    lines = [line]
    for child_id in children_map.get(node_id, []):
        child_lines = render_markdown(nodes_by_id, children_map, child_id, depth + 1)
        if child_lines:
            lines.append(child_lines)
    return "\n".join(lines)


def export_markdown(data: dict[str, Any]) -> str:
    title = data.get("title", "Mindmap")
    nodes_by_id, children_map = build_tree(data)
    lines = [f"# {title}\n"]
    for child_id in children_map.get("root", []):
        lines.append(render_markdown(nodes_by_id, children_map, child_id, 0))
    return "\n".join(lines)


def apply_op(data: dict[str, Any], op: dict[str, Any]) -> Any:
    action = op.get("op") or op.get("action")

    if action == "reset":
        title = op.get("title") or data.get("title") or "hermes"
        root_label = op.get("root_label") or title
        data.clear()
        data.update(default_map(title))
        data["nodes"][0]["label"] = root_label
        return {"reset": True}

    if action == "add_node":
        return add_node(data, op)

    if action == "batch_add":
        parent_id = op.get("parent_id") or op.get("parent") or "root"
        result = []
        for item in op.get("nodes", []):
            if isinstance(item, str):
                child_op = {"op": "add_node", "parent_id": parent_id, "label": item}
            else:
                child_op = dict(item)
                child_op.setdefault("op", "add_node")
                child_op.setdefault("parent_id", parent_id)
            result.append(add_node(data, child_op))
        return result

    if action == "update_node":
        return update_node(data, op)

    if action == "set_status":
        op["status"] = op.get("status", "todo")
        return update_node(data, op)

    if action == "delete_node":
        return delete_node(data, op)

    if action == "connect_nodes":
        return connect_nodes(data, op)

    if action == "layout":
        return auto_layout(data)

    raise HTTPException(status_code=400, detail=f"unknown op: {action}")


async def broadcast(name: str, data: dict[str, Any]) -> None:
    payload = json.dumps({"type": "update", "map": data}, ensure_ascii=False)
    alive = []
    for ws in connections.get(name, []):
        try:
            await ws.send_text(payload)
            alive.append(ws)
        except Exception:
            pass
    connections[name] = alive


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health():
    return {"ok": True, "service": "hermes-mindmap-canvas"}


@app.get("/api/maps")
async def list_maps():
    maps = []
    for p in MAP_DIR.glob("*.json"):
        maps.append(p.stem)
    if not maps:
        load_map("hermes")
        maps.append("hermes")
    return {"maps": sorted(maps)}


@app.get("/api/maps/{name}")
async def get_map(name: str):
    return load_map(name)


@app.post("/api/maps/{name}/ops")
async def post_op(name: str, op: dict[str, Any]):
    name = safe_name(name)
    data = load_map(name)

    result = apply_op(data, op)
    save_map(name, data)
    await broadcast(name, data)

    return {"ok": True, "result": result, "map": data}


@app.get("/api/maps/{name}/export/markdown")
async def export_map_markdown(name: str):
    data = load_map(name)
    md = export_markdown(data)
    return PlainTextResponse(content=md, media_type="text/markdown")


@app.websocket("/ws/maps/{name}")
async def websocket_map(ws: WebSocket, name: str):
    name = safe_name(name)
    await ws.accept()
    connections.setdefault(name, []).append(ws)

    data = load_map(name)
    await ws.send_text(json.dumps({"type": "update", "map": data}, ensure_ascii=False))

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        if name in connections:
            connections[name] = [x for x in connections[name] if x is not ws]


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
