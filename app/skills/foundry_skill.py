from typing import Annotated
from dotenv import load_dotenv
import os
from semantic_kernel.functions import kernel_function
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.contents import AuthorRole
from azure.identity.aio import DefaultAzureCredential

class FoundryAgentPlugin:

    @kernel_function(description="See the Azure AI Foundry remote agent for regulatory and technical context.")
    async def consultar_foundry(self, pregunta: Annotated[str, "Query for Foundry Agent"]) -> Annotated[str, "Remote agent response"]:
        load_dotenv()
        
        settings = AzureAIAgentSettings.create()

        async with (
            DefaultAzureCredential() as creds,
            AzureAIAgent.create_client(credential=creds) as client,
        ):
            
            agent_definition = await client.agents.create_agent(
                model=settings.model_deployment_name,
            )

            agent_definition = await client.agents.get_agent(os.getenv("AZURE_AI_FOUNDATION_AGENT_ID"))

            agent = AzureAIAgent(
                client=client,
                definition=agent_definition
            )

            thread: AzureAIAgentThread = None

            try:
                async for response in agent.invoke(messages=pregunta, thread=thread):
                    if response.role != AuthorRole.TOOL:
                        return response.content
                    thread = response.thread
            finally:
                await thread.delete() if thread else None
