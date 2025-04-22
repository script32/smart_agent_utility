
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.filters import FunctionInvocationContext
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings
from azure.identity.aio import DefaultAzureCredential

from app.skills.sql_skill import SqlSkill
from app.skills.crew_skill import CrewSkill

load_dotenv()


async def create_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_filter("function_invocation", function_invocation_filter)
    return kernel


async def create_agents(kernel: Kernel) -> ChatCompletionAgent:
    # Agentes internos con plugins locales
    sql_skill = SqlSkill()
    crew_skill = CrewSkill()

    fault_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="FaultAgent",
        instructions="Respondes consultas sobre eventos eléctricos. Usa SQLSkill para obtener datos.",
        plugins=[sql_skill]
    )

    crew_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="CrewAgent",
        instructions="Entregas disponibilidad de cuadrillas por comuna o ubicación. Usa CrewSkill.",
        plugins=[crew_skill]
    )

    geo_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="GeoAgent",
        instructions="Respondes consultas geográficas (líneas, comunas, zonas críticas).",
        plugins=[sql_skill]
    )

    report_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="ReportAgent",
        instructions="Redactas respuestas claras y explicativas para usuarios no técnicos.",
        plugins=[]
    )

    # Agente remoto desde Azure AI Foundry
    credential = DefaultAzureCredential()
    client = await AzureAIAgent.create_client(credential=credential)
    agent_definition = await client.agents.get_agent(os.getenv("AZURE_AI_FOUNDATION_AGENT_ID"))

    foundry_agent = AzureAIAgent(
        client=client,
        definition=agent_definition,
    )

    # Agente orquestador
    main_agent = ChatCompletionAgent(
        name="Orquestador",
        kernel=kernel,
        service=AzureChatCompletion(),
        instructions="""
Eres un agente orquestador. Recibes preguntas generales y decides cuál agente especializado debe responder:
- FaultAgent: para fallas eléctricas
- CrewAgent: para cuadrillas o asignaciones operativas
- GeoAgent: para temas geográficos o cobertura
- ReportAgent: para redactar explicaciones
- FoundryAgent: para normativa, procedimientos eléctricos o contexto técnico avanzado
""",
        plugins=[]
    )

    main_agent.add_chat_participant("FaultAgent", fault_agent)
    main_agent.add_chat_participant("CrewAgent", crew_agent)
    main_agent.add_chat_participant("GeoAgent", geo_agent)
    main_agent.add_chat_participant("ReportAgent", report_agent)
    main_agent.add_chat_participant("FoundryAgent", foundry_agent)

    return main_agent


# Logging de funciones invocadas (opcional)
async def function_invocation_filter(context: FunctionInvocationContext, next):
    print(f"➡️ [{context.function.name}] called with: {context.arguments}")
    await next(context)
    print(f"⬅️ [{context.function.name}] result: {context.result.value}")
