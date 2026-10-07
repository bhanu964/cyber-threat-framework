from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent 
from backend.database import init_database
from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel

from backend.devices import (
    register_device,
    get_devices,
    get_device,
    update_heartbeat,
)

from backend.events import (
    create_event,
    get_events,
    clear_events,
)

app = FastAPI(
    title="Cross-Platform Cyber Threat Framework",
    version="0.1.0"
)

init_database()

@app.get("/dashboard")
def dashboard():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/victim")
def victim():
    return FileResponse(BASE_DIR / "frontend" / "victim.html")

@app.get("/")
def root():
    return {
        "status": "online",
        "node": "CONTROL-MAC",
        "lab_mode": True,
        "message": "Cyber Threat Framework Control Node is online"
    }


@app.get("/api/status")
def status():
    return {
        "status": "online",
        "node": "CONTROL-MAC",
        "lab_mode": True
    }

class DeviceRegistration(BaseModel):
    device_id: str
    platform: str
    role: str = "victim"


@app.post("/api/devices/register")
def register(device: DeviceRegistration):
    return register_device(
        device.device_id,
        device.platform,
        device.role
    )


@app.get("/api/devices")
def devices():
    return get_devices()


@app.get("/api/devices/{device_id}")
def device(device_id: str):
    return get_device(device_id)


@app.post("/api/devices/{device_id}/heartbeat")
def heartbeat(device_id: str):
    return update_heartbeat(device_id)

class EventRequest(BaseModel):
    event_type: str
    source: str
    target: str | None = None
    severity: str = "info"
    message: str = ""


@app.post("/api/events")
def create_security_event(event: EventRequest):
    return create_event(
        event.event_type,
        event.source,
        event.target,
        event.severity,
        event.message,
    )


@app.get("/api/events")
def events():
    return get_events()


@app.delete("/api/events")
def delete_events():
    return clear_events()