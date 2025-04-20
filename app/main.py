from fastapi import FastAPI, Request
from app.sk_config import create_kernel
from semantic_kernel import KernelArguments

app = FastAPI()
kernel = create_kernel()

@app.post("/preguntar")
async def preguntar(request: Request):
    body = await request.json()
    funcion = body.get("funcion")  # Ej: "obtener_fallas_recientes"
    parametros = body.get("parametros", {})  # Ej: {"comuna": "Osorno"}

    if not funcion:
        return {"error": "Falta la función a invocar"}

    args = KernelArguments()
    for key, value in parametros.items():
        args[key] = value

    try:
        result = kernel.invoke("SQLSkill", funcion, arguments=args)
        return {"resultado": str(result)}
    except Exception as e:
        return {"error": str(e)}
