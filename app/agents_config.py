import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.filters import FunctionInvocationContext

from app.skills.sql_skill import SqlSkill
from app.skills.crew_skill import CrewSkill
from app.skills.foundry_skill import FoundryAgentPlugin


load_dotenv()

async def function_invocation_filter(context: FunctionInvocationContext, next):
    print(f"⬆️ [{context.function.name}] called with: {context.arguments}")
    await next(context)
    print(f"⬇️ [{context.function.name}] result: {context.result.value}")

async def create_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_filter("function_invocation", function_invocation_filter)
    return kernel

async def create_agents(kernel: Kernel) -> ChatCompletionAgent:
    # === Local Agents ===
    sql_skill = SqlSkill()
    crew_skill = CrewSkill()
    foundry_plugin = FoundryAgentPlugin()

    fault_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="FaultAgent",
        instructions="""You answer questions about electrical events and faults. Use SQLSkill.

        - If the `reportar_falla_por_direccion` function is successfully executed, respond with a clear confirmation like "Your fault has been successfully registered".
        - If the address is not found, suggest the user verify the street name.
        - Avoid mentioning technical issues if the functions return successfully.
        """,
        plugins=[sql_skill]
    )

    crew_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="CrewAgent",
        instructions="You provide information about crews. Use CrewSkill.",
        plugins=[crew_skill]
    )

    geo_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="GeoAgent",
        instructions="You answer geographic queries. Use SQLSkill.",
        plugins=[sql_skill]
    )

    report_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="ReportAgent",
        instructions="You write clear explanations based on technical data.",
        plugins=[]
    )
 
    # === Main Orchestrator Agent ===
    main_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        kernel=kernel,
        name="Orquestador",
        instructions="""
        You are an orchestrator agent that routes questions to the following agents:
        - FaultAgent: electrical faults and outage information
        - CrewAgent: available or assigned crews
        - GeoAgent: geographic analysis and affected areas
        - ReportAgent: user-friendly explanations
        - FoundryAgent: regulatory or advanced technical context
        """,
        plugins=[fault_agent, crew_agent, geo_agent, report_agent, foundry_plugin]
    )

    return main_agent
