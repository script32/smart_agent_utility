import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.agents_config import create_kernel, create_agents
from app.skills.sql_skill import SqlSkill
from app.session_store import SessionStore

from semantic_kernel.agents import ChatHistoryAgentThread

# Variables globales
kernel = None
agent = None
session_store = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global kernel, agent, session_store

    kernel = await create_kernel()
    agent = await create_agents(kernel)
    sql_skill = SqlSkill()
    session_store = SessionStore(sql_skill.plugin.conn)

    yield  # Aquí continúa FastAPI después del inicio

    # Puedes poner lógica de cierre si la necesitas
    # por ejemplo: cerrar conexiones

# Inicializar FastAPI con Lifespan
app = FastAPI(
    title="SmartField Multi-Agent API",
    description="Agente orquestado con Semantic Kernel y Azure AI Foundry",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "SmartField Multi-Agent AI with Azure Foundry is running."}

@app.post("/preguntar")
async def preguntar(request: Request):
    try:
        body = await request.json()
        pregunta = body.get("pregunta", "").strip()
        session_id = body.get("session_id", "default")

        if not pregunta:
            return {"error": "Falta el campo 'pregunta'"}

        thread = session_store.load(session_id)
        response = await agent.get_response(messages=pregunta, thread=thread)
        session_store.save(session_id, thread)

        return {
            "respuesta": response.content,
            "session_id": session_id
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
