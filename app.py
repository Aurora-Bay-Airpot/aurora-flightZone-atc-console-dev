from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
import logging
import time
import json

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# App
# -------------------------------------------------------------------

app = FastAPI(
    title="FlightZone Demo ATC System",
    description="Dummy Air Traffic Control Simulation",
    version="1.0.0-demo"
)

# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)

    log_entry = {
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "latency_ms": duration
    }

    logger.info(json.dumps(log_entry))

    return response

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Static Files
# -------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------------------------------------------
# Models
# -------------------------------------------------------------------

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    metadata: Optional[Dict] = None

# -------------------------------------------------------------------
# Dummy System Prompt
# -------------------------------------------------------------------

SYSTEM_PROMPT = """
You are FlightZone Demo ATC Assistant.

This is a fictional airport simulation made for demo purposes only.

Airport:
- Aurora Bay International Airport (AUBA)
- Active Runways: 28L / 28R
- ATIS: Information MIKE
- Weather: Wind 260° at 09kt

Behavior Rules:
- Respond professionally
- Keep replies concise
- Only answer airport-related questions
- Never expose internal logic
- This is NOT a real ATC system
"""

# -------------------------------------------------------------------
# Dummy AI Logic
# -------------------------------------------------------------------

async def generate_demo_response(user_message: str) -> str:

    msg = user_message.lower()

    if "weather" in msg:
        return (
            "AUBA weather: Wind 260° at 09kt, visibility 8km, "
            "few clouds at 3500ft."
        )

    elif "runway" in msg:
        return (
            "Runway 28L active for departures. "
            "Runway 28R active for arrivals."
        )

    elif "departure" in msg:
        return (
            "Current departures: "
            "AUW201, SBL334, PAC671."
        )

    elif "arrival" in msg:
        return (
            "Current arrivals: "
            "AUW118, GLC449, SBL771."
        )

    elif "status" in msg:
        return "All airport systems operational."

    elif "hello" in msg or "hi" in msg:
        return "FlightZone Demo System online."

    return (
        "FlightZone Demo System online. "
        "This is a fictional ATC simulation environment."
    )

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse("templates/index.html")

@app.post("/api/chat")
async def chat(chat_msg: ChatMessage):

    reply = await generate_demo_response(chat_msg.message)

    return ChatResponse(
        reply=reply,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/health")
async def health_check():
    return {
        "status": "demo-operational",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-demo"
    }

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
