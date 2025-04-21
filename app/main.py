import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from semantic_kernel.agents import ChatHistoryAgentThread
from app.agents_config import create_kernel, create_agents

# Inicializar FastAPI
app = FastAPI(
    title="SmartField Multi-Agent API",
    description="Agente orquestado con Semantic Kernel 1.28+",
    version="1.0.0",
)

# Habilitar CORS (útil si haces pruebas desde frontends externos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear el kernel y los agentes
kernel = create_kernel()
agent = create_agents(kernel)
thread = ChatHistoryAgentThread()  # Conversación persistente

@app.get("/")
def root():
    return {"status": "SmartField Multi-Agent AI is running."}

@app.post("/preguntar")
async def preguntar(request: Request):
    try:
        body = await request.json()
        pregunta = body.get("pregunta", "").strip()

        if not pregunta:
            return {"error": "Falta el campo 'pregunta'"}

        # Obtener la respuesta del agente orquestador
        response = await agent.get_response(messages=pregunta, thread=thread)

        return {"respuesta": response.content}

    except Exception as e:
        return {"error": str(e)}

# Para ejecución local (opcional)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
