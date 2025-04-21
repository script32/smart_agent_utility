import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.filters import FunctionInvocationContext
from app.skills.sql_skill import SqlSkill
from app.skills.crew_skill import CrewSkill

load_dotenv()

# 🔍 Filtro opcional para logging de funciones invocadas
async def function_invocation_filter(context: FunctionInvocationContext, next):
    print(f"➡️ [{context.function.name}] called with: {context.arguments}")
    await next(context)
    print(f"⬅️ [{context.function.name}] result: {context.result.value}")


def create_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_filter("function_invocation", function_invocation_filter)
    return kernel


def create_agents(kernel: Kernel) -> ChatCompletionAgent:

    # 🧠 Crear instancia compartida del plugin SQL
    sql_skill = SqlSkill()
    crew_skill = CrewSkill()

    # ⚡ Agente de fallas eléctricas
    fault_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="FaultAgent",
        instructions="Respondes consultas sobre eventos eléctricos en la red. Usa SQLSkill para obtener datos de fallas.",
        plugins=[sql_skill]
    )

    # 👷 Agente de cuadrillas
    crew_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="CrewAgent",
        instructions="Entregas disponibilidad de cuadrillas en base a la comuna o eventos recientes.",
        plugins=[crew_skill]
    )

    # 🌍 Agente geoespacial
    geo_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="GeoAgent",
        instructions="Respondes consultas geográficas. Puedes ver qué líneas pasan por comunas, sectores afectados, etc.",
        plugins=[sql_skill]
    )

    # 📝 Agente redactor
    report_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="ReportAgent",        
        instructions="Transformas datos técnicos en explicaciones comprensibles para usuarios no técnicos.",
        plugins=[]  # No necesita SQL
    )

    # 🤖 Agente orquestador principal
    main_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="Orquestador",
        kernel=kernel,
        instructions="""
        Eres un agente orquestador. Interpreta la intención del usuario y delega al agente correcto:
        - FaultAgent: fallas eléctricas
        - CrewAgent: cuadrillas disponibles
        - GeoAgent: preguntas geoespaciales
        - ReportAgent: generar respuestas entendibles
        Puedes combinar agentes si es necesario.
        """,
        plugins=[fault_agent, crew_agent, geo_agent, report_agent]
    )

    return main_agent
